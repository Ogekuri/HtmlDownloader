#!/usr/bin/env python3
"""
htmldownloader.py

Downloader offline multi-formato per:
1) TI "document-viewer" (JS app)  -> usa Playwright + cattura immagini dal network
2) "doxygen-export" (sito statico) -> crawler interno + unione pagine

Output in --to-dir:
- document.html  : documento offline (stile minimo, leggibile)
- index.html     : indice con link alle sezioni nel documento
- assets/        : risorse scaricate (immagini principalmente, ma anche css/js/font dove utile)

Install:
  pip install requests beautifulsoup4 lxml tqdm playwright
  playwright install chromium

Uso:
  python htmldownloader.py --from-url "https://www.ti.com/document-viewer/am6442/datasheet" --to-dir ./out
  python htmldownloader.py --from-url "https://software-dl.ti.com/.../index.html" --to-dir ./out2
"""

from __future__ import annotations

import argparse
import mimetypes
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, urldefrag, unquote

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ----------------------------
# Shared helpers
# ----------------------------

def safe_filename(path: str) -> str:
    path = (path or "").strip()
    path = re.sub(r"[<>:\"|?*\x00-\x1F]", "_", path)
    path = path.replace("\\", "_")
    return path


def is_http_url(s: str) -> bool:
    try:
        u = urlparse(s)
        return u.scheme in ("http", "https")
    except Exception:
        return False


def normalize_url(u: str, base: str) -> str:
    u = (u or "").strip()
    if not u:
        return u
    if u.startswith(("data:", "mailto:", "javascript:", "blob:")):
        return u
    return urljoin(base, u)


def ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def local_path_for_url(asset_url: str, out_dir: Path) -> Path:
    """
    Map URL -> out_dir/assets/<host>/<path> (with query fingerprint if present)
    """
    u = urlparse(asset_url)
    host = safe_filename(u.netloc or "nohost")
    p = u.path if u.path else "/index"
    if p.endswith("/"):
        p += "index"
    p = safe_filename(p.lstrip("/"))

    if u.query:
        q = safe_filename(re.sub(r"[^a-zA-Z0-9]+", "_", u.query))[:80]
        root, ext = os.path.splitext(p)
        p = f"{root}__q_{q}{ext or ''}"

    return out_dir / "assets" / host / p


def download_one(session: requests.Session, url: str, dest: Path, timeout: int = 60) -> bool:
    ensure_parent(dest)
    try:
        with session.get(url, stream=True, timeout=timeout, allow_redirects=True) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 128):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception:
        return False


def escape_html(s: str) -> str:
    return (s.replace("&", "&amp;")
              .replace("<", "&lt;")
              .replace(">", "&gt;")
              .replace('"', "&quot;")
              .replace("'", "&#39;"))


@dataclass
class TocNode:
    title: str
    href: str
    children: List["TocNode"] = field(default_factory=list)


def ensure_heading_ids(soup: BeautifulSoup) -> None:
    used: Set[str] = set()
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        hid = h.get("id")
        text = " ".join(h.get_text(" ", strip=True).split())
        if not hid and text:
            base = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
            if base:
                cand = base
                i = 2
                while cand in used:
                    cand = f"{base}-{i}"
                    i += 1
                h["id"] = cand
                hid = cand
        if hid:
            used.add(hid)


def strip_styles(soup: BeautifulSoup) -> None:
    """Remove external stylesheets, inline styles, and style tags."""
    for link in list(soup.find_all("link", rel=lambda v: v and "stylesheet" in v)):
        link.decompose()
    for style in list(soup.find_all("style")):
        style.decompose()
    for tag in soup.find_all(True):
        if tag.has_attr("style"):
            del tag["style"]


def toc_from_headings(soup: BeautifulSoup) -> List[TocNode]:
    nodes: List[TocNode] = []
    stack: List[Tuple[int, TocNode]] = []
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        hid = h.get("id")
        if not hid:
            continue
        title = " ".join(h.get_text(" ", strip=True).split())
        if not title:
            continue
        level = int(h.name[1])
        node = TocNode(title=title, href=f"#{hid}")
        while stack and stack[-1][0] >= level:
            stack.pop()
        if stack:
            stack[-1][1].children.append(node)
        else:
            nodes.append(node)
        stack.append((level, node))
    return nodes


def toc_from_nav_html(toc_html: str, base_url: str) -> List[TocNode]:
    soup = BeautifulSoup(toc_html, "lxml")

    def parse_list(list_el) -> List[TocNode]:
        items: List[TocNode] = []
        for li in list_el.find_all("li", recursive=False):
            link = li.find("a")
            if not link:
                # Check for title-only elements (e.g., <li class="toc-title">)
                if "toc-title" in li.get("class", []) or li.get("id") == "doc-lister":
                    title = " ".join(li.get_text(" ", strip=True).split())
                    if title:
                        # Create a node without href (will be rendered as plain text)
                        node = TocNode(title=title, href="#")
                        items.append(node)
                continue
            title = " ".join(link.get_text(" ", strip=True).split())
            href = normalize_url(link.get("href") or "", base_url)
            if not title or not href:
                continue
            node = TocNode(title=title, href=href)
            child_lists = li.find_all(["ul", "ol"], recursive=False)
            for cl in child_lists:
                node.children.extend(parse_list(cl))
            items.append(node)
        return items

    top_lists = soup.find_all(["ul", "ol"], recursive=False)
    if not top_lists:
        # fallback: attempt with any list if no top-level found
        top_lists = soup.find_all(["ul", "ol"])
    out: List[TocNode] = []
    if top_lists:
        # Process only the first list to avoid duplicates from multiple nav structures
        out.extend(parse_list(top_lists[0]))
    return out


ASSET_ATTRS = [
    ("img", "src"),
    ("img", "data-src"),
    ("source", "srcset"),
    ("link", "href"),
]


class Logger:
    """Minimal stdout logger with gating for verbose/debug output."""

    def __init__(self, verbose: bool = False, debug: bool = False):
        self.verbose_enabled = bool(verbose or debug)
        self.debug_enabled = bool(debug)

    def info(self, msg: str) -> None:
        print(msg)

    def verbose(self, msg: str) -> None:
        if self.verbose_enabled:
            print(msg)

    def debug(self, msg: str) -> None:
        if self.debug_enabled:
            print(msg)

    def check(self, msg: str) -> None:
        if self.verbose_enabled or self.debug_enabled:
            print(msg)


def iter_asset_urls(soup: BeautifulSoup, page_url: str) -> Set[str]:
    urls: Set[str] = set()

    for tag_name, attr in ASSET_ATTRS:
        for t in soup.find_all(tag_name):
            v = t.get(attr)
            if not v:
                continue
            if attr == "srcset":
                parts = [p.strip().split(" ")[0] for p in v.split(",") if p.strip()]
                for p in parts:
                    u = normalize_url(p, page_url)
                    if is_http_url(u):
                        urls.add(u)
            else:
                u = normalize_url(v, page_url)
                if is_http_url(u):
                    urls.add(u)

    # inline background-image url(...)
    bg_re = re.compile(r"url\(([^)]+)\)")
    for t in soup.find_all(style=True):
        style = t.get("style") or ""
        for m in bg_re.finditer(style):
            raw = m.group(1).strip().strip("'\"")
            u = normalize_url(raw, page_url)
            if is_http_url(u):
                urls.add(u)

    return urls


def rewrite_asset_links_inplace(soup: BeautifulSoup, base_url: str, out_dir: Path) -> None:
    def to_rel(u: str) -> str:
        u2 = normalize_url(u, base_url)
        if not is_http_url(u2):
            return u
        lp = local_path_for_url(u2, out_dir)
        return lp.relative_to(out_dir).as_posix()

    for tag_name, attr in ASSET_ATTRS:
        for t in soup.find_all(tag_name):
            v = t.get(attr)
            if not v:
                continue
            if attr == "srcset":
                parts = []
                for seg in (v or "").split(","):
                    seg = seg.strip()
                    if not seg:
                        continue
                    bits = seg.split()
                    url_part = bits[0]
                    rest = " ".join(bits[1:])
                    parts.append(f"{to_rel(url_part)}{(' ' + rest) if rest else ''}")
                t[attr] = ", ".join(parts)
            else:
                t[attr] = to_rel(v)

    bg_re = re.compile(r"url\(([^)]+)\)")
    for t in soup.find_all(style=True):
        style = t.get("style") or ""
        def repl(m):
            raw = m.group(1).strip().strip("'\"")
            return f"url('{to_rel(raw)}')"
        t["style"] = bg_re.sub(repl, style)


def build_toc_html(
    toc_items: List[TocNode],
    document_filename: str = "document.html",
    target_frame: str = "doc",
) -> str:
    def resolved_href(href: str) -> str:
        href = (href or "").strip()
        _, frag = urldefrag(href)
        if frag:
            return f"{document_filename}#{frag}"
        if href.startswith("#"):
            return f"{document_filename}{href}"
        return document_filename

    def render_nodes(nodes: List[TocNode]) -> str:
        if not nodes:
            return ""
        items = []
        for n in nodes:
            href = resolved_href(n.href)
            children_html = render_nodes(n.children)
            items.append(
                f"<li><a target=\"{escape_html(target_frame)}\" href=\"{href}\">{escape_html(n.title)}</a>{children_html}</li>"
            )
        return f"<ul>{''.join(items)}</ul>"
    toc_html = render_nodes(toc_items)

    return f"""<!doctype html>
<html lang="it">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>TOC</title>
    <style>
        body {{ font-family: sans-serif; margin: 1rem; }}
        h1 {{ margin-top: 0; font-size: 1.4rem; }}
    </style>
</head>
<body>
    <h1>TOC</h1>
    {toc_html}
</body>
</html>
"""


def build_frameset_index(toc_filename: str = "toc.html", document_filename: str = "document.html") -> str:
    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Indice e documento</title>
</head>
<frameset cols="28%,*">
  <frame src="{toc_filename}" name="toc" />
  <frame src="{document_filename}" name="doc" />
  <noframes>
    <body>
      <p>Il browser non supporta i frame. Apri <a href="{toc_filename}">toc</a> e <a href="{document_filename}">documento</a>.</p>
    </body>
  </noframes>
</frameset>
</html>
"""


def minimal_readable_wrapper(inner_html: str, title: str = "Documento (offline)") -> str:
    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{escape_html(title)}</title>
</head>
<body>
{inner_html}
</body>
</html>
"""


# ----------------------------
# Downloader framework
# ----------------------------

class BaseDownloader:
    name: str = "base"

    def __init__(self, from_url: str, out_dir: Path, session: requests.Session, logger: Optional[Logger] = None):
        self.from_url = from_url
        self.out_dir = out_dir
        self.session = session
        self.log = logger or Logger()

    @classmethod
    def matches_url(cls, url: str) -> bool:
        return False

    @classmethod
    def probe_html(cls, url: str, html: str) -> bool:
        return False

    def run(self) -> None:
        raise NotImplementedError


class DownloaderRegistry:
    def __init__(self):
        self._classes: List[type[BaseDownloader]] = []

    def register(self, downloader_cls: type[BaseDownloader]) -> None:
        self._classes.append(downloader_cls)

    def detect(self, url: str, session: requests.Session) -> type[BaseDownloader]:
        url_matches = [c for c in self._classes if c.matches_url(url)]
        if len(url_matches) == 1:
            return url_matches[0]

        html = ""
        try:
            r = session.get(url, timeout=30, allow_redirects=True)
            r.raise_for_status()
            html = r.text[:2_000_000]
        except Exception:
            pass

        html_matches = [c for c in self._classes if html and c.probe_html(url, html)]
        if len(html_matches) == 1:
            return html_matches[0]

        if html_matches:
            return html_matches[0]
        if url_matches:
            return url_matches[0]
        raise RuntimeError("Impossibile determinare il tipo di downloader per questa URL.")


# ----------------------------
# Document-viewer (TI) downloader
# ----------------------------

def guess_ext_from_content_type(ct: str) -> str:
    ct = (ct or "").split(";")[0].strip().lower()
    if not ct:
        return ""
    ext = mimetypes.guess_extension(ct) or ""
    if ct in ("text/javascript", "application/javascript"):
        return ".js"
    if ct == "text/css":
        return ".css"
    if ct.startswith("image/") and not ext:
        return "." + ct.split("/", 1)[1]
    return ext


class NetworkImageRecorder:
    """
    Capture ALL image responses loaded by the browser (TI viewer loads many images lazily / via CSS).
    We only care about images because you said style isn't important; this also keeps assets smaller.
    """
    def __init__(self, out_dir: Path):
        self.out_dir = out_dir
        self.saved: Dict[str, Path] = {}
        self.failed: Set[str] = set()

    def attach(self, page):
        def on_response(resp):
            try:
                url = resp.url
                if not is_http_url(url):
                    return
                ct = (resp.headers.get("content-type") or "").lower()
                if not ct.startswith("image/"):
                    return
                if url in self.saved or url in self.failed:
                    return

                lp = local_path_for_url(url, self.out_dir)
                if not lp.suffix:
                    ext = guess_ext_from_content_type(ct)
                    if ext:
                        lp = lp.with_suffix(ext)

                ensure_parent(lp)
                body = resp.body()
                with open(lp, "wb") as f:
                    f.write(body)
                self.saved[url] = lp
            except Exception:
                try:
                    self.failed.add(resp.url)
                except Exception:
                    pass

        page.on("response", on_response)


class DocumentViewerDownloader(BaseDownloader):
    name = "document-viewer"

    TOC_SELECTORS = ["#viewer_navTree", "nav", "[role='navigation']", "aside", "#contents", ".contents", ".toc"]
    CONTENT_SELECTORS = [
        "ti-library-viewer-content-area",  # TI's actual content area component
        ".viewer-content",  # Content area class
        ".content-area",  # Alternative content class
        "#loadContentArea",  # TI's content loading area
        ".cardWrapper",  # Card wrapper containing document sections
        "main:not(.viewer-sidebar)", "[role='main']:not(.viewer-sidebar)", 
        "article", ".document", ".content:not(.tab-slider-content)", "#content"
    ]
    TOC_SCROLL_SELECTORS = ["nav", "[role='navigation']", "#contents", ".contents", ".toc"]

    @classmethod
    def matches_url(cls, url: str) -> bool:
        u = urlparse(url)
        return ("ti.com" in u.netloc) and ("/document-viewer/" in u.path)

    @classmethod
    def probe_html(cls, url: str, html: str) -> bool:
        h = html.lower()
        return "document-viewer" in h

    def _pick_best_outerhtml(self, page, selectors: List[str]) -> Optional[str]:
        best = None
        best_score = -1
        for sel in selectors:
            try:
                handles = page.query_selector_all(sel)
            except Exception:
                continue
            for h in handles:
                try:
                    txt = (h.inner_text() or "").strip()
                    score = len(txt)
                    if score > best_score:
                        best_score = score
                        best = h
                except Exception:
                    continue
        if not best:
            return None
        try:
            return best.evaluate("el => el.outerHTML")
        except Exception:
            return None

    def _expand_full_toc(self, page, max_rounds: int = 10, settle_ms: int = 400) -> None:
        selectors = [
            "button[aria-expanded='false']",
            "[role='treeitem'] > button[aria-expanded='false']",
            "button:has-text('Expand all')",
            "button:has-text('Expand')",
            ".expand",
            ".chevron",
        ]

        for i in range(max_rounds):
            try:
                clicked = page.evaluate(
                    "(selectors) => {\n"
                    "  let c = 0;\n"
                    "  selectors.forEach(sel => {\n"
                    "    document.querySelectorAll(sel).forEach(btn => {\n"
                    "      const aria = btn.getAttribute('aria-expanded');\n"
                    "      if (aria === 'true') return;\n"
                    "      btn.click();\n"
                    "      c += 1;\n"
                    "    });\n"
                    "  });\n"
                    "  return c;\n"
                    "}",
                    selectors,
                )
            except Exception:
                clicked = 0

            try:
                remaining = page.evaluate(
                    "(selectors) => {\n"
                    "  let r = 0;\n"
                    "  selectors.forEach(sel => { r += document.querySelectorAll(sel).length; });\n"
                    "  return r;\n"
                    "}",
                    [selectors[0], selectors[1]],
                )
            except Exception:
                remaining = 0

            self.log.verbose(f"[verbose] toc-expand round={i+1} clicked={clicked} remaining={remaining}")
            page.wait_for_timeout(settle_ms)

            if clicked == 0 and remaining == 0:
                break

    def _scroll_toc_container(self, page, step_px: int = 900, max_rounds: int = 40, settle_ms: int = 200) -> None:
        for sel in self.TOC_SCROLL_SELECTORS:
            try:
                info = page.evaluate(
                    "(sel) => { const el = document.querySelector(sel); if (!el) return null; return {h: el.scrollHeight, c: el.clientHeight}; }",
                    sel,
                )
            except Exception:
                info = None
            if not info or not info.get("c"):
                continue

            last_pos = -1
            stable = 0
            for i in range(max_rounds):
                try:
                    pos = page.evaluate(
                        "(sel) => { const el = document.querySelector(sel); if (!el) return -1; return el.scrollTop; }",
                        sel,
                    )
                except Exception:
                    break
                try:
                    page.evaluate(
                        "(sel, step) => { const el = document.querySelector(sel); if (!el) return; el.scrollBy(0, step); }",
                        sel,
                        step_px,
                    )
                except Exception:
                    break
                page.wait_for_timeout(settle_ms)
                if pos == last_pos:
                    stable += 1
                else:
                    stable = 0
                last_pos = pos
                if stable >= 3:
                    break
            try:
                page.evaluate("(sel) => { const el = document.querySelector(sel); if (el) el.scrollTo(0, 0); }", sel)
            except Exception:
                pass

    def _find_scroll_container(self, page):
        best = None
        best_area = -1
        for sel in self.CONTENT_SELECTORS:
            try:
                handles = page.query_selector_all(sel)
            except Exception:
                continue
            for h in handles:
                try:
                    info = h.evaluate(
                        "el => {\n"
                        "  const cs = getComputedStyle(el);\n"
                        "  return {\n"
                        "    scrollHeight: el.scrollHeight,\n"
                        "    clientHeight: el.clientHeight,\n"
                        "    clientWidth: el.clientWidth,\n"
                        "    overflowY: cs.overflowY,\n"
                        "  };\n"
                        "}"
                    )
                except Exception:
                    continue
                if not info or not info.get("clientHeight"):
                    continue
                scroll_h = info.get("scrollHeight", 0)
                client_h = info.get("clientHeight", 0)
                if scroll_h <= client_h + 10:
                    continue
                area = info.get("clientWidth", 0) * client_h
                if area > best_area:
                    best_area = area
                    best = h
        if best:
            return best

        try:
            handle = page.evaluate_handle(
                "() => {\n"
                "  const els = Array.from(document.querySelectorAll('*'));\n"
                "  let best = null;\n"
                "  let bestArea = 0;\n"
                "  for (const el of els) {\n"
                "    const cs = getComputedStyle(el);\n"
                "    const oy = cs.overflowY;\n"
                "    const scrollable = (oy === 'auto' || oy === 'scroll' || oy === 'overlay') && el.scrollHeight > el.clientHeight + 10;\n"
                "    if (!scrollable) continue;\n"
                "    const r = el.getBoundingClientRect();\n"
                "    const area = Math.max(0, r.width) * Math.max(0, r.height);\n"
                "    if (area > bestArea) { bestArea = area; best = el; }\n"
                "  }\n"
                "  return best;\n"
                "}"
            )
            element = handle.as_element() if handle else None
            return element
        except Exception:
            return None

    def _auto_scroll_element(
        self,
        page,
        element,
        settle_ms: int,
        step_px: int,
        max_rounds: int,
        stable_rounds: int,
        label: str,
    ) -> bool:
        try:
            info = element.evaluate(
                "el => ({ scrollHeight: el.scrollHeight, clientHeight: el.clientHeight })"
            )
        except Exception:
            return False
        if not info or info.get("scrollHeight", 0) <= info.get("clientHeight", 0) + 10:
            return True

        last_height = -1
        last_scroll_top = -1
        stable = 0
        for i in range(max_rounds):
            try:
                metrics = element.evaluate(
                    "el => ({ scrollHeight: el.scrollHeight, scrollTop: el.scrollTop, clientHeight: el.clientHeight })"
                )
            except Exception:
                return False
            height = metrics.get("scrollHeight", 0)
            scroll_top = metrics.get("scrollTop", 0)
            client_h = metrics.get("clientHeight", 0)
            if i == 0:
                self.log.verbose(f"[verbose] auto-scroll start ({label})")
            if height == last_height:
                stable += 1
            else:
                stable = 0
            if i % 8 == 0:
                self.log.verbose(f"[verbose] auto-scroll round={i+1} height={height} stable={stable} ({label})")
            if stable >= stable_rounds:
                self.log.verbose(f"[verbose] auto-scroll stop round={i+1} stable={stable} height={height} ({label})")
                break
            if scroll_top == last_scroll_top and (scroll_top + client_h >= height - 2):
                self.log.verbose(f"[verbose] auto-scroll stop round={i+1} bottom reached ({label})")
                break
            last_height = height
            last_scroll_top = scroll_top
            try:
                element.evaluate("(el, step) => { el.scrollBy(0, step); }", step_px)
            except Exception:
                return False
            page.wait_for_timeout(settle_ms)

        try:
            element.evaluate("el => { el.scrollTop = el.scrollHeight; }")
            page.wait_for_timeout(settle_ms * 2)
            element.evaluate("el => { el.scrollTop = 0; }")
        except Exception:
            pass
        return True

    def _auto_scroll(self, page, settle_ms: int = 300, step_px: int = 1400, max_rounds: int = 320, stable_rounds: int = 6) -> None:
        scroll_el = self._find_scroll_container(page)
        if scroll_el and self._auto_scroll_element(
            page,
            scroll_el,
            settle_ms=settle_ms,
            step_px=step_px,
            max_rounds=max_rounds,
            stable_rounds=stable_rounds,
            label="container",
        ):
            return

        try:
            page.evaluate("() => window.scrollTo(0, 0)")
        except Exception:
            pass

        last_height = -1
        stable = 0
        for i in range(max_rounds):
            try:
                height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
                client_h = page.evaluate("() => Math.max(document.body.clientHeight, document.documentElement.clientHeight, window.innerHeight)")
            except Exception:
                break
            if height <= client_h + 10:
                return
            if i == 0:
                self.log.verbose("[verbose] auto-scroll start")
            if height == last_height:
                stable += 1
            else:
                stable = 0
            if i % 8 == 0:
                self.log.verbose(f"[verbose] auto-scroll round={i+1} height={height} stable={stable}")
            if stable >= stable_rounds:
                self.log.verbose(f"[verbose] auto-scroll stop round={i+1} stable={stable} height={height}")
                break
            last_height = height
            page.evaluate(f"() => window.scrollBy(0, {step_px})")
            page.wait_for_timeout(settle_ms)

        try:
            page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(settle_ms * 2)
            page.evaluate("() => window.scrollTo(0, 0)")
        except Exception:
            pass

    def _collect_cards_from_container(
        self,
        page,
        container,
        settle_ms: int = 200,
        step_ratio: float = 0.9,
        stable_rounds: int = 6,
        max_rounds: int = 400,
    ) -> Dict[str, str]:
        cards: Dict[str, str] = {}
        last_height = -1
        last_scroll_top = -1
        stable = 0

        for _ in range(max_rounds):
            try:
                batch = container.evaluate(
                    "el => {\n"
                    "  const primary = el.querySelectorAll('.documentSection[data-url]');\n"
                    "  const nodes = primary.length ? Array.from(primary) : Array.from(el.querySelectorAll('[data-url]'));\n"
                    "  return nodes.map(node => ({\n"
                    "    url: node.getAttribute('data-url') || '',\n"
                    "    html: node.outerHTML || ''\n"
                    "  }));\n"
                    "}"
                )
            except Exception:
                break

            for item in batch or []:
                url = (item.get("url") or "").strip()
                html = item.get("html") or ""
                if url and html and url not in cards:
                    cards[url] = html

            try:
                metrics = container.evaluate(
                    "el => ({ scrollTop: el.scrollTop, clientHeight: el.clientHeight, scrollHeight: el.scrollHeight })"
                )
            except Exception:
                break

            scroll_top = metrics.get("scrollTop", 0)
            client_h = metrics.get("clientHeight", 0)
            height = metrics.get("scrollHeight", 0)

            if height == last_height:
                stable += 1
            else:
                stable = 0

            if stable >= stable_rounds:
                break
            if scroll_top == last_scroll_top and (scroll_top + client_h >= height - 2):
                break

            last_height = height
            last_scroll_top = scroll_top

            step = int(client_h * step_ratio) if client_h else 0
            if step <= 0:
                break
            try:
                container.evaluate(
                    "(el, step) => { el.scrollTop = Math.min(el.scrollTop + step, el.scrollHeight); }",
                    step,
                )
            except Exception:
                break
            page.wait_for_timeout(settle_ms)

        return cards

    def _best_card_for_fragment(self, cards: Dict[str, str], fragment: str) -> Optional[Tuple[str, str]]:
        frag = unquote((fragment or "").lstrip("#").strip())
        if not frag:
            return None
        frag_l = frag.lower()
        frag_parts = [p for p in frag_l.split("/") if p]
        if frag_l not in frag_parts:
            frag_parts.insert(0, frag_l)
        match_parts = [p for p in frag_parts if len(p) >= 8] or frag_parts

        def score_value(val: str) -> int:
            if not val:
                return 0
            v = unquote(val).lower()
            if v == frag_l:
                return 100
            if frag_l and frag_l in v:
                return 80
            matched = [part for part in match_parts if part and part in v]
            if matched and len(matched) == len(match_parts):
                return 70
            if matched:
                return 40
            return 0

        best_url = None
        best_score = 0
        for url in cards:
            if not self._fragment_matches_url(fragment, url):
                continue
            _, frag_val = urldefrag(url)
            target = frag_val or url
            score = score_value(target)
            if score > best_score:
                best_score = score
                best_url = url

        if best_url and best_score > 0:
            return best_url, cards[best_url]
        return None

    def _fragment_matches_url(self, fragment: str, data_url: str) -> bool:
        frag = unquote((fragment or "").lstrip("#").strip()).lower()
        if not frag or not data_url:
            return False
        parts = [p for p in frag.split("/") if p]
        if frag not in parts:
            parts.insert(0, frag)
        parts = [p for p in parts if len(p) >= 8] or parts
        _, frag_val = urldefrag(data_url)
        target = unquote(frag_val or data_url).lower()
        return all(part in target for part in parts)

    def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]:
        return toc_from_nav_html(toc_html, self.from_url)

    @staticmethod
    def _iter_nodes(nodes: List[TocNode]) -> Iterable[TocNode]:
        for n in nodes:
            yield n
            yield from DocumentViewerDownloader._iter_nodes(n.children)

    @staticmethod
    def _first_numeric_index(nodes: List[TocNode]) -> Optional[int]:
        for i, n in enumerate(nodes):
            title = (n.title or "").strip().lower()
            if title.startswith("1 "):
                return i
        return None

    @staticmethod
    def _trim_toc_nodes(nodes: List[TocNode]) -> List[TocNode]:
        """Trim TOC for display: start from first "1 " entry, drop trailing IMPORTANT NOTICE."""
        if not nodes:
            return []

        trimmed = list(nodes)
        start_idx = DocumentViewerDownloader._first_numeric_index(trimmed)
        if start_idx is not None:
            trimmed = trimmed[start_idx:]

        if trimmed and DocumentViewerDownloader._is_important_notice_label(trimmed[-1].title):
            trimmed = trimmed[:-1]

        return trimmed if trimmed else list(nodes)

    @staticmethod
    def _first_toc_entry_title(nodes: List[TocNode]) -> Optional[str]:
        for node in nodes:
            title = (node.title or "").strip()
            if title:
                return title
        return None

    @staticmethod
    def _is_important_notice_label(title: Optional[str]) -> bool:
        text = (title or "").strip().lower()
        return text.startswith("important notice")

    @staticmethod
    def _is_important_notice_section(section_html: str) -> bool:
        soup = BeautifulSoup(section_html, "lxml")
        heading = soup.find(re.compile(r"^h[1-6]$"))
        if heading and DocumentViewerDownloader._is_important_notice_label(heading.get_text(" ", strip=True)):
            return True
        flat_text = " ".join(soup.get_text(" ", strip=True).split()).lower()
        return "important notice and disclaimer" in flat_text

    @staticmethod
    def _select_section_nodes(nodes: List[TocNode]) -> List[TocNode]:
        """
        Choose the slice of TOC nodes to download: from first title starting with
        "1 " through the last occurrence of "IMPORTANT NOTICE" (inclusive). If
        missing, fall back to the full list.
        """
        flat = list(DocumentViewerDownloader._iter_nodes(nodes))
        if not flat:
            return []

        start_idx = DocumentViewerDownloader._first_numeric_index(flat)
        if start_idx is None:
            start_idx = 0

        end_idx = None
        for i in range(len(flat) - 1, -1, -1):
            if DocumentViewerDownloader._is_important_notice_label(flat[i].title):
                end_idx = i
                break

        if end_idx is None or end_idx < start_idx:
            end_idx = len(flat) - 1

        return flat[start_idx : end_idx + 1]

    def _dedup_toc_nodes_by_href(self, nodes: List[TocNode]) -> List[TocNode]:
        """Merge duplicate TOC nodes by normalized href within same parent level."""

        def dedup_list(items: List[TocNode]) -> List[TocNode]:
            seen: Dict[str, TocNode] = {}  # Scope seen to this level only
            out: List[TocNode] = []
            for n in items:
                key = (n.href or "").strip().lower()
                # Recursively deduplicate children first
                n.children = dedup_list(n.children)
                if key:
                    existing = seen.get(key)
                    if existing:
                        # Merge children and prefer the more descriptive/structured title
                        existing_children_before = len(existing.children)
                        existing.children.extend(n.children)
                        if len(n.children) > existing_children_before:
                            existing.title = n.title
                        elif len(n.title or "") > len(existing.title or ""):
                            existing.title = n.title
                        continue
                    seen[key] = n
                out.append(n)
            return out

        return dedup_list(nodes)

    def _is_section_scrollable(self, page, viewport_multiplier: float = 2.0) -> bool:
        """
        Verifica se la sezione attuale ha contenuto sufficiente per permettere scroll.
        Una sezione è considerata scrollable se scrollHeight è almeno (viewport_multiplier * clientHeight).
        Default: almeno 2x l'altezza del viewport.
        """
        try:
            result = page.evaluate(
                f"() => {{\n"
                f"  const body = document.body;\n"
                f"  const html = document.documentElement;\n"
                f"  const scrollH = Math.max(body.scrollHeight, html.scrollHeight);\n"
                f"  const clientH = Math.max(body.clientHeight, html.clientHeight, window.innerHeight);\n"
                f"  return scrollH > (clientH * {viewport_multiplier});\n"
                f"}}"
            )
            return bool(result)
        except Exception:
            return False

    def _remove_toc_elements(self, soup: BeautifulSoup) -> None:
        """
        Remove TOC/navigation elements from captured content to prevent
        contamination of document.html with navigation tree.
        """
        # Remove by tag name (TI custom components)
        toc_tag_names = [
            "ti-library-viewer-side-bar",
            "ti-library-viewer-tab-bar",
            "ti-library-viewer-command-bar",
        ]
        for tag_name in toc_tag_names:
            for elem in list(soup.find_all(tag_name)):
                elem.decompose()
        
        # Remove by selector
        toc_selectors = [
            "#viewer_navTree",  # Main navigation tree
            ".viewer-sidebar",  # Sidebar container
            "#ti_library_viewer_contents",  # TOC contents section
            ".tiLibrary-tabs",  # Tab bar
            ".tab-slider",  # Tab slider navigation
            "#doc-lister",  # Document lister title (captured separately)
            ".toc_hierarchy",  # TOC hierarchy container
            ".mininav",  # Mini navigation controls
            "[data-lid='ti-library-viewer-side-bar']",  # TOC by data attribute
            "[data-lid='ti-library-viewer-tab-bar']",  # Tab bar by data attribute
            "[data-lid='ti-library-viewer-toc']",  # TOC by data attribute
            "[data-lid='ti-library-viewer-command-bar']",  # Command bar
        ]
        for sel in toc_selectors:
            for elem in list(soup.select(sel)):
                elem.decompose()

    def _extract_fragment_only(self, soup: BeautifulSoup, fragment: str) -> BeautifulSoup:
        """Return soup narrowed to the element matching the fragment id/name, if present (case-insensitive)."""
        frag = unquote((fragment or "").lstrip("#").strip())
        if not frag:
            return soup

        frag_l = frag.lower()
        frag_parts = [p for p in frag_l.split("/") if p]
        if frag_l not in frag_parts:
            frag_parts.insert(0, frag_l)

        def score_value(val: str) -> int:
            if not val:
                return 0
            v = unquote(val).lower()
            if v == frag_l:
                return 100
            if frag_l and frag_l in v:
                return 80
            score = 0
            for part in frag_parts:
                if part == frag_l:
                    continue
                if v == part:
                    score = max(score, 60)
                elif part and part in v:
                    score = max(score, 40)
            return score

        def pick_best_section(elements):
            best = None
            best_score = 0
            best_len = None
            for el in elements:
                data_url = el.get("data-url") or ""
                score = score_value(data_url)
                if score <= 0:
                    continue
                text_len = len(el.get_text(" ", strip=True))
                if score > best_score or (score == best_score and (best_len is None or text_len < best_len)):
                    best = el
                    best_score = score
                    best_len = text_len
            return best

        # Prefer a single documentSection card that matches the fragment to avoid duplicated parent cards.
        candidates = soup.select(".documentSection[data-url]") or soup.find_all(attrs={"data-url": True})
        best_section = pick_best_section(candidates)
        if best_section:
            narrowed = BeautifulSoup("", "lxml")
            narrowed.append(BeautifulSoup(str(best_section), "lxml"))
            return narrowed

        def matches_fragment(el) -> bool:
            if not el:
                return False
            el_id = el.get("id")
            if el_id and (el_id.lower() == frag_l or el_id.lower() in frag_parts):
                return True
            el_name = el.get("name")
            if el_name and (el_name.lower() == frag_l or el_name.lower() in frag_parts):
                return True
            data_url = el.get("data-url") or ""
            if data_url and score_value(data_url) > 0:
                return True
            return False

        target = None
        for el in soup.find_all(True):
            if matches_fragment(el):
                target = el
                break

        if not target:
            return soup

        chosen = target
        parent_section = target.find_parent(attrs={"data-url": True})
        if parent_section:
            chosen = parent_section
        else:
            for ancestor in target.parents:
                if ancestor is soup:
                    break
                if ancestor.name in ("section", "div", "article"):
                    data_url = ancestor.get("data-url") or ""
                    if ancestor.get("id") or score_value(data_url) > 0:
                        chosen = ancestor
                        break

        narrowed = BeautifulSoup("", "lxml")
        narrowed.append(BeautifulSoup(str(chosen), "lxml"))
        return narrowed

    def _wait_for_fragment(self, page, fragment: str, timeout_ms: int = 8000) -> bool:
        frag = unquote((fragment or "").lstrip("#").strip())
        if not frag:
            return True
        frag_l = frag.lower()
        frag_parts = [p for p in frag_l.split("/") if p]
        if frag_l not in frag_parts:
            frag_parts.insert(0, frag_l)

        js = (
            "(frag, fragLower, parts) => {\n"
            "  const norm = (s) => (s || '').toLowerCase();\n"
            "  const matches = (val) => {\n"
            "    const v = norm(val);\n"
            "    if (!v) return false;\n"
            "    if (v === fragLower || v.includes(fragLower)) return true;\n"
            "    for (const p of parts) {\n"
            "      if (p && (v === p || v.includes(p))) return true;\n"
            "    }\n"
            "    return false;\n"
            "  };\n"
            "  if (document.getElementById(frag) || document.getElementById(fragLower)) return true;\n"
            "  const named = document.getElementsByName(frag);\n"
            "  if (named && named.length) return true;\n"
            "  const els = document.querySelectorAll('[data-url], [id], [name]');\n"
            "  for (const el of els) {\n"
            "    const elId = el.getAttribute('id');\n"
            "    if (elId && (norm(elId) === fragLower || parts.includes(norm(elId)))) return true;\n"
            "    const elName = el.getAttribute('name');\n"
            "    if (elName && (norm(elName) === fragLower || parts.includes(norm(elName)))) return true;\n"
            "    if (matches(el.getAttribute('data-url'))) return true;\n"
            "  }\n"
            "  return false;\n"
            "}\n"
        )

        try:
            page.wait_for_function(js, frag, frag_l, frag_parts, timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False
        except Exception:
            return False

    def _click_toc_link(self, page, fragment: str) -> bool:
        frag = unquote((fragment or "").lstrip("#").strip())
        if not frag:
            return False
        try:
            return bool(page.evaluate(
                "(frag) => {\n"
                "  const links = Array.from(document.querySelectorAll('a'));\n"
                "  const target = links.find(a => (a.getAttribute('href') || '').includes(frag));\n"
                "  if (!target) return false;\n"
                "  target.scrollIntoView({ block: 'center' });\n"
                "  target.click();\n"
                "  return true;\n"
                "}\n",
                frag,
            ))
        except Exception:
            return False

    def run(self) -> None:
        recorder = NetworkImageRecorder(self.out_dir)
        self.log.debug("[debug] document-viewer: recorder attached")

        def make_anchor(raw_fragment: str, title: str, used: Set[str]) -> str:
            base = (raw_fragment or title or "sezione").strip()
            base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower() or "sezione"
            cand = base
            i = 2
            while cand in used:
                cand = f"{base}-{i}"
                i += 1
            used.add(cand)
            return cand

        def normalize_text(value: str) -> str:
            value = (value or "").strip()
            value = re.sub(r"\s+", " ", value)
            return value.lower()

        def strip_ti_disclaimer(section_html: str) -> str:
            soup = BeautifulSoup(section_html, "lxml")
            section = soup.find("section")
            if not section:
                return section_html

            disclaimer_tag = None
            for candidate in section.find_all(["p", "div"]):
                text = " ".join(candidate.get_text(" ", strip=True).split()).strip().lower()
                if text.startswith("ti provides technical and reliability data"):
                    disclaimer_tag = candidate
                    break

            if not disclaimer_tag:
                return section_html

            for sibling in list(disclaimer_tag.find_next_siblings()):
                sibling.decompose()
            disclaimer_tag.decompose()
            return str(section)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(90_000)

            recorder.attach(page)

            try:
                page.goto(self.from_url, wait_until="networkidle")
            except PlaywrightTimeoutError:
                page.goto(self.from_url, wait_until="domcontentloaded")

            page.wait_for_timeout(2000)

            # Expand navigation tree (with repeated passes and scroll in TOC) to capture full TOC
            for _ in range(3):
                self._expand_full_toc(page)
                self._scroll_toc_container(page)
            self._expand_full_toc(page)

            toc_html = self._pick_best_outerhtml(page, self.TOC_SELECTORS)
            if not toc_html:
                try:
                    toc_html = page.evaluate("() => { const nav = document.querySelector('nav'); return nav ? nav.outerHTML : null; }")
                except Exception:
                    toc_html = None

            if toc_html:
                self.log.check("[check] TOC HTML catturata dalla pagina")
            else:
                self.log.debug("[debug] Nessuna TOC HTML catturata, si useranno le intestazioni")

            # Also capture doc-lister title if present (TI pages have this as a separate element)
            doc_title_html = None
            try:
                doc_title_html = page.evaluate("() => { const el = document.querySelector('#doc-lister'); return el ? el.outerHTML : null; }")
            except Exception:
                pass

            content_html = self._pick_best_outerhtml(page, self.CONTENT_SELECTORS)
            if not content_html:
                content_html = page.evaluate("() => document.body.outerHTML")

            initial_content_html = content_html or ""
            content_soup = BeautifulSoup(initial_content_html, "lxml")
            ensure_heading_ids(content_soup)

            toc_nodes: List[TocNode] = []
            if toc_html:
                toc_nodes = self._toc_tree_from_html(toc_html)

            # Prepend doc title if captured separately
            if doc_title_html:
                title_soup = BeautifulSoup(doc_title_html, "lxml")
                title_text = " ".join(title_soup.get_text(" ", strip=True).split())
                if title_text and title_text not in str(toc_nodes):
                    title_node = TocNode(title=title_text, href=self.from_url)
                    toc_nodes.insert(0, title_node)

            if not toc_nodes:
                self.log.verbose("[verbose] TOC fallback: building from headings")
                toc_nodes = toc_from_headings(content_soup)

            pre_trim_title_text = self._first_toc_entry_title(toc_nodes)

            section_nodes = self._select_section_nodes(toc_nodes)
            display_toc_nodes = self._trim_toc_nodes(toc_nodes)

            if not section_nodes:
                section_nodes = toc_nodes

            if not display_toc_nodes:
                display_toc_nodes = section_nodes

            clean_display_toc_nodes: List[TocNode] = []
            cleaned_title: Optional[str] = None
            if display_toc_nodes:
                clean_display_toc_nodes = self._dedup_toc_nodes_by_href(display_toc_nodes)
                cleaned_title = self._first_toc_entry_title(clean_display_toc_nodes)

            title_text: Optional[str] = pre_trim_title_text or cleaned_title
            used_ids: Set[str] = set()
            section_plan: List[Tuple[str, str, str, str]] = []  # (full_url_with_fragment, anchor, title, fragment)
            section_to_toc_node: Dict[int, TocNode] = {}  # Map section index to TOC node
            url_to_anchor: Dict[str, str] = {}  # Map section URL -> anchor kept in document
            frag_to_anchor: Dict[str, str] = {}  # Map normalized fragment -> chosen anchor

            for node in section_nodes:
                raw_href = node.href or ""
                full_href = normalize_url(raw_href, self.from_url) if raw_href else self.from_url
                base_url, frag = urldefrag(full_href)
                if not base_url:
                    base_url = self.from_url

                frag_norm = (frag or "").lstrip("#").strip().lower()

                # Choose/reuse anchor for this fragment (regardless of whether it will be downloaded)
                anchor = None
                if frag_norm and frag_norm in frag_to_anchor:
                    anchor = frag_to_anchor[frag_norm]

                section_url = full_href if frag else base_url

                # Reuse anchor for repeated section URLs so TOC always points to a kept section
                if section_url in url_to_anchor:
                    anchor = anchor or url_to_anchor[section_url]
                    node.href = f"#{anchor}"
                    continue

                if not anchor:
                    anchor = make_anchor(frag, node.title, used_ids)
                    if frag_norm:
                        frag_to_anchor[frag_norm] = anchor

                node.href = f"#{anchor}"
                url_to_anchor[section_url] = anchor

                # For TI document-viewer, the fragment determines which content is loaded
                # Use the full URL with fragment to ensure unique content per section
                section_idx = len(section_plan)
                section_plan.append((section_url, anchor, node.title, frag))
                section_to_toc_node[section_idx] = node

            if not section_plan:
                self.log.verbose("[verbose] No TOC sections detected; using full document")
                section_plan.append((self.from_url, make_anchor("", "documento", used_ids), "Documento", ""))

            if not title_text and section_plan:
                title_text = (section_plan[0][2] or "").strip()
            title_text = title_text or "Documento"

            self.log.debug(f"[debug] Planned {len(section_plan)} sections from TOC")

            scroll_container = self._find_scroll_container(page)
            cards_by_url: Dict[str, str] = {}
            if scroll_container:
                try:
                    scroll_container.evaluate("el => { el.scrollTop = 0; }")
                except Exception:
                    pass
                cards_by_url = self._collect_cards_from_container(page, scroll_container)
                self.log.debug(f"[debug] Collected {len(cards_by_url)} cards from scroll container")
                if cards_by_url and len(cards_by_url) < max(3, len(section_plan) // 2):
                    self.log.debug("[debug] Card cache incomplete; falling back to per-section load")
                    cards_by_url = {}
            else:
                self._auto_scroll(page)

            sections_html: List[str] = []
            seen_card_urls: Dict[str, str] = {}
            # Download all deduplicated sections (skip scrollability filtering)
            first_scrollable_idx = 0

            # Download sections starting from the first scrollable one
            for section_idx, (section_url, anchor, title, raw_fragment) in enumerate(
                section_plan[first_scrollable_idx:], start=first_scrollable_idx
            ):
                self.log.verbose(f"[verbose] Fetching section {section_idx+1}/{len(section_plan)} -> {section_url}")
                section_html = None
                card_url = None
                from_cache = False

                if cards_by_url:
                    card_match = self._best_card_for_fragment(cards_by_url, raw_fragment)
                    if card_match:
                        card_url, section_html = card_match
                        if card_url in seen_card_urls:
                            existing_anchor = seen_card_urls[card_url]
                            node = section_to_toc_node.get(section_idx)
                            if node:
                                node.href = f"#{existing_anchor}"
                            continue
                        seen_card_urls[card_url] = anchor
                        from_cache = True

                if not section_html:
                    fragment_ready = False
                    if self._click_toc_link(page, raw_fragment):
                        page.wait_for_timeout(500)
                        fragment_ready = self._wait_for_fragment(page, raw_fragment, timeout_ms=12000)

                    if not fragment_ready:
                        try:
                            page.goto(section_url, wait_until="domcontentloaded")
                        except PlaywrightTimeoutError:
                            try:
                                page.goto(section_url, wait_until="networkidle")
                            except Exception:
                                pass
                        page.wait_for_timeout(500)
                        fragment_ready = self._wait_for_fragment(page, raw_fragment, timeout_ms=12000)

                    if fragment_ready:
                        self._auto_scroll(page, settle_ms=150, step_px=1200, max_rounds=60, stable_rounds=3)

                    section_html = self._pick_best_outerhtml(page, self.CONTENT_SELECTORS)
                    if not section_html:
                        try:
                            section_html = page.evaluate("() => document.body.outerHTML")
                        except Exception:
                            section_html = ""

                section_soup = BeautifulSoup(section_html or "", "lxml")
                self._remove_toc_elements(section_soup)  # Remove TOC/navigation before processing
                section_soup = self._extract_fragment_only(section_soup, raw_fragment)
                if section_idx == 0 and title:
                    expected = normalize_text(title)
                    section_text = normalize_text(section_soup.get_text(" ", strip=True))
                    if expected and expected not in section_text:
                        fallback_soup = BeautifulSoup(initial_content_html, "lxml")
                        self._remove_toc_elements(fallback_soup)
                        fallback_section = self._extract_fragment_only(fallback_soup, raw_fragment)
                        fallback_text = normalize_text(fallback_section.get_text(" ", strip=True))
                        if expected and expected not in fallback_text:
                            first_card = fallback_soup.select_one(".documentSection[data-url]")
                            if first_card:
                                alt = BeautifulSoup("", "lxml")
                                alt.append(BeautifulSoup(str(first_card), "lxml"))
                                fallback_section = alt
                                fallback_text = normalize_text(fallback_section.get_text(" ", strip=True))
                        if expected and expected in fallback_text:
                            self.log.debug("[debug] Fallback to initial content for first section")
                            section_soup = fallback_section
                ensure_heading_ids(section_soup)

                if not from_cache:
                    if not card_url:
                        first_card = section_soup.find(attrs={"data-url": True})
                        if first_card:
                            card_url = (first_card.get("data-url") or "").strip()
                    if card_url and not self._fragment_matches_url(raw_fragment, card_url):
                        card_url = None
                    if card_url:
                        if card_url in seen_card_urls:
                            existing_anchor = seen_card_urls[card_url]
                            node = section_to_toc_node.get(section_idx)
                            if node:
                                node.href = f"#{existing_anchor}"
                            continue
                        seen_card_urls[card_url] = anchor

                asset_urls = iter_asset_urls(section_soup, section_url)
                for u in sorted(asset_urls):
                    lp = local_path_for_url(u, self.out_dir)
                    if not lp.exists():
                        download_one(self.session, u, lp)

                self.log.debug(f"[debug] Section assets: {len(asset_urls)} from {section_url}")

                rewrite_asset_links_inplace(section_soup, section_url, self.out_dir)
                strip_styles(section_soup)

                wrapper = BeautifulSoup("", "lxml")
                section_tag = wrapper.new_tag("section")
                section_tag["id"] = anchor
                if title and not section_soup.find(["h1", "h2", "h3"]):
                    heading = wrapper.new_tag("h2")
                    heading.string = title
                    section_tag.append(heading)
                inner_html = section_soup.body.decode_contents() if section_soup.body else str(section_soup)
                inner_soup = BeautifulSoup(inner_html, "lxml")
                container = inner_soup.body or inner_soup
                for child in list(container.children):
                    section_tag.append(child)

                sections_html.append(str(section_tag))

            browser.close()
            if sections_html:
                if self._is_important_notice_section(sections_html[-1]):
                    sections_html.pop()
                else:
                    sections_html[-1] = strip_ti_disclaimer(sections_html[-1])

        self.log.check("[check] Generating document.html")
        body_parts = []
        if title_text:
            body_parts.append(f"<p class=\"document-title\">{escape_html(title_text)}</p>")
        body_parts.extend(sections_html)
        doc_html = minimal_readable_wrapper("\n".join(body_parts), title="Documento (offline)")
        doc_soup = BeautifulSoup(doc_html, "lxml")
        ensure_heading_ids(doc_soup)
        toc_from_doc = toc_from_headings(doc_soup)
        toc_for_output = clean_display_toc_nodes if clean_display_toc_nodes else toc_from_doc
        (self.out_dir / "document.html").write_text(str(doc_soup), encoding="utf-8")
        self.log.check("[check] Generating toc.html")
        (self.out_dir / "toc.html").write_text(
            build_toc_html(toc_for_output, document_filename="document.html", target_frame="doc"),
            encoding="utf-8",
        )
        self.log.check("[check] Generating index.html")
        (self.out_dir / "index.html").write_text(
            build_frameset_index(toc_filename="toc.html", document_filename="document.html"),
            encoding="utf-8",
        )

        self.log.check(f"[check] Captured images via network: {len(recorder.saved)} (failed: {len(recorder.failed)})")


# ----------------------------
# Doxygen-export downloader
# ----------------------------

class DoxygenExportDownloader(BaseDownloader):
    name = "doxygen-export"

    @classmethod
    def matches_url(cls, url: str) -> bool:
        u = urlparse(url)
        # TI export path typically contains /exports/ and ends with index.html
        return ("/exports/" in u.path and url.lower().endswith(".html")) or ("doxygen" in u.path.lower())

    @classmethod
    def probe_html(cls, url: str, html: str) -> bool:
        h = html.lower()
        return ("name=\"generator\"" in h and "doxygen" in h) or ("dynsections.js" in h)

    def _scope(self) -> Tuple[str, str]:
        u = urlparse(self.from_url)
        host = u.netloc
        path = u.path
        dir_path = path.rsplit("/", 1)[0] + "/" if "/" in path else "/"
        scope_dir_url = f"{u.scheme}://{u.netloc}{dir_path}"
        return host, scope_dir_url

    def _fetch_soup(self, url: str) -> BeautifulSoup:
        r = self.session.get(url, timeout=60, allow_redirects=True)
        r.raise_for_status()
        return BeautifulSoup(r.text, "lxml")

    def _is_in_scope(self, url: str, host: str, scope_dir_url: str) -> bool:
        if not is_http_url(url):
            return False
        u = urlparse(url)
        if u.netloc != host:
            return False
        return url.startswith(scope_dir_url)

    def _page_title(self, soup: BeautifulSoup) -> str:
        t = soup.find("title")
        if t and t.get_text(strip=True):
            return t.get_text(strip=True)
        h1 = soup.find("h1")
        if h1:
            return " ".join(h1.get_text(" ", strip=True).split())
        return "Page"

    def _extract_main(self, soup: BeautifulSoup) -> BeautifulSoup:
        main = soup.select_one("#doc-content")
        if not main:
            main = soup.select_one("div.contents") or soup.select_one("main") or soup.body
        frag = BeautifulSoup("", "lxml")
        wrapper = frag.new_tag("div")
        wrapper["class"] = "page-content"
        wrapper.append(BeautifulSoup(str(main), "lxml"))
        frag.append(wrapper)
        return frag

    def _links_to_html_pages(self, soup: BeautifulSoup, page_url: str, host: str, scope_dir_url: str) -> Set[str]:
        out: Set[str] = set()
        for a in soup.find_all("a"):
            href = (a.get("href") or "").strip()
            if not href:
                continue
            full = normalize_url(href, page_url)
            full, _ = urldefrag(full)
            if full.lower().endswith(".html") and self._is_in_scope(full, host, scope_dir_url):
                out.add(full)
        return out

    def _build_toc(self, doc: BeautifulSoup) -> List[TocNode]:
        nodes: List[TocNode] = []
        container = doc.select_one("#offline-doc")
        if not container:
            return nodes

        for sec in container.find_all("section", recursive=False):
            title_el = sec.find("h1")
            title = " ".join(title_el.get_text(" ", strip=True).split()) if title_el else "Pagina"
            href = f"#{sec.get('id')}" if sec.get("id") else "#"
            page_node = TocNode(title=title or "Pagina", href=href)

            child_nodes: List[TocNode] = []
            stack: List[Tuple[int, TocNode]] = []
            for h in sec.find_all(re.compile(r"^h[2-6]$")):
                hid = h.get("id")
                if not hid:
                    continue
                h_title = " ".join(h.get_text(" ", strip=True).split())
                if not h_title:
                    continue
                level = int(h.name[1])
                node = TocNode(title=h_title, href=f"#{hid}")
                while stack and stack[-1][0] >= level:
                    stack.pop()
                if stack:
                    stack[-1][1].children.append(node)
                else:
                    child_nodes.append(node)
                stack.append((level, node))

            page_node.children = child_nodes
            nodes.append(page_node)

        return nodes

    def run(self) -> None:
        host, scope_dir_url = self._scope()

        index_soup = self._fetch_soup(self.from_url)

        self.log.debug("[debug] doxygen-export: starting crawl")

        # Crawl pages
        MAX_PAGES = 250
        queue: List[str] = [urldefrag(self.from_url)[0]]
        seen: Set[str] = set()
        pages: List[Tuple[str, BeautifulSoup]] = []

        while queue and len(seen) < MAX_PAGES:
            url = queue.pop(0)
            if url in seen:
                continue
            seen.add(url)
            try:
                psoup = self._fetch_soup(url)
            except Exception:
                continue
            pages.append((url, psoup))
            for nxt in sorted(self._links_to_html_pages(psoup, url, host, scope_dir_url)):
                if nxt not in seen and (len(queue) + len(seen) < MAX_PAGES):
                    queue.append(nxt)

        self.log.debug(f"[debug] doxygen-export: crawled {len(pages)} pages (limit {MAX_PAGES})")

        # Build unified doc with robust anchors
        doc = BeautifulSoup("", "lxml")
        container = doc.new_tag("div")
        container["id"] = "offline-doc"
        doc.append(container)

        for i, (url, psoup) in enumerate(pages, start=1):
            title = self._page_title(psoup)
            anchor = f"page-{i}"

            sec = doc.new_tag("section")
            sec["id"] = anchor
            h1 = doc.new_tag("h1")
            h1.string = title
            sec.append(h1)

            main = self._extract_main(psoup)
            sec.append(BeautifulSoup(str(main), "lxml"))
            container.append(sec)

            self.log.verbose(f"[verbose] Aggiunta sezione {anchor} -> {title}")

        ensure_heading_ids(doc)

        toc_nodes = self._build_toc(doc)
        self.log.verbose(f"[verbose] TOC generata con {len(toc_nodes)} voci di primo livello")

        # Download assets from all pages
        asset_urls: Set[str] = set()
        for url, psoup in pages:
            asset_urls |= iter_asset_urls(psoup, url)

        for u in tqdm(sorted(asset_urls), desc="Downloading assets", unit="file"):
            lp = local_path_for_url(u, self.out_dir)
            if not lp.exists():
                download_one(self.session, u, lp)

        self.log.debug(f"[debug] Assets totali scaricati o riusati: {len(asset_urls)}")

        # Rewrite to local
        rewrite_asset_links_inplace(doc, scope_dir_url, self.out_dir)

        # Remove stylesheet references and inline styles
        strip_styles(doc)

        # Output
        self.log.check("[check] Generating document.html")
        doc_html = minimal_readable_wrapper(str(doc), title="Documento (offline)")
        (self.out_dir / "document.html").write_text(doc_html, encoding="utf-8")
        self.log.check("[check] Generating toc.html")
        (self.out_dir / "toc.html").write_text(
            build_toc_html(toc_nodes, document_filename="document.html", target_frame="doc"),
            encoding="utf-8",
        )
        self.log.check("[check] Generating index.html")
        (self.out_dir / "index.html").write_text(
            build_frameset_index(toc_filename="toc.html", document_filename="document.html"),
            encoding="utf-8",
        )


# ----------------------------
# Main
# ----------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-url", required=True)
    ap.add_argument("--to-dir", required=True)
    ap.add_argument("--user-agent", default="Mozilla/5.0 (X11; Linux x86_64) htmldownloader/1.0")
    ap.add_argument("--verbose", action="store_true", help="Stampa avanzamento download e check")
    ap.add_argument("--debug", action="store_true", help="Abilita log dettagliati e include il verbose")
    return ap


def main() -> int:
    ap = build_arg_parser()
    args = ap.parse_args()

    from_url = args.from_url.strip()
    out_dir = Path(args.to_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    logger = Logger(verbose=bool(args.verbose or args.debug), debug=bool(args.debug))

    session = requests.Session()
    session.headers.update({"User-Agent": args.user_agent})

    registry = DownloaderRegistry()
    registry.register(DocumentViewerDownloader)
    registry.register(DoxygenExportDownloader)

    dl_cls = registry.detect(from_url, session)
    downloader = dl_cls(from_url, out_dir, session, logger=logger)

    logger.info(f"[i] Using downloader: {downloader.name}")
    downloader.run()

    logger.info("[ok] Saved:")
    logger.info(f"  - {out_dir / 'toc.html'}")
    logger.info(f"  - {out_dir / 'index.html'}")
    logger.info(f"  - {out_dir / 'document.html'}")
    logger.info(f"  - {out_dir / 'assets'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
