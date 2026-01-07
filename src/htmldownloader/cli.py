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
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, urldefrag

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


ASSET_ATTRS = [
    ("img", "src"),
    ("img", "data-src"),
    ("source", "srcset"),
    ("link", "href"),
]


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


def build_index_html(toc_items: List[Tuple[str, str]], document_filename: str = "document.html") -> str:
    lis = []
    for title, href in toc_items:
        href = (href or "").strip()
        _, frag = urldefrag(href)
        if frag:
            target = f"{document_filename}#{frag}"
        elif href.startswith("#"):
            target = f"{document_filename}{href}"
        else:
            target = document_filename
        lis.append(f'<li><a href="{target}">{escape_html(title)}</a></li>')

    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Indice</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; line-height: 1.4; }}
    ul {{ padding-left: 18px; }}
    li {{ margin: 6px 0; }}
  </style>
  
</head>
<body>
  <h1>Indice</h1>
  <p><a href="{document_filename}">Apri documento completo</a></p>
  <ul>{''.join(lis)}</ul>
</body>
</html>
"""


def minimal_readable_wrapper(inner_html: str, title: str = "Documento (offline)") -> str:
    css = """
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; line-height: 1.45; }
    img { max-width: 100%; height: auto; }
    table { border-collapse: collapse; max-width: 100%; overflow-x: auto; display: block; }
    td, th { border: 1px solid #ddd; padding: 6px 8px; }
    pre, code { white-space: pre-wrap; }
    """
    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{escape_html(title)}</title>
  <style>{css}</style>
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

    def __init__(self, from_url: str, out_dir: Path, session: requests.Session):
        self.from_url = from_url
        self.out_dir = out_dir
        self.session = session

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

    TOC_SELECTORS = ["nav", "[role='navigation']", "aside", "#contents", ".contents", ".toc"]
    CONTENT_SELECTORS = ["main", "[role='main']", "article", ".document", ".content", "#content"]

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

    def _auto_scroll(self, page, settle_ms: int = 200, step_px: int = 1600, max_rounds: int = 200) -> None:
        last_height = 0
        stable = 0
        for _ in range(max_rounds):
            try:
                height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
            except Exception:
                break
            if height == last_height:
                stable += 1
            else:
                stable = 0
            if stable >= 4:
                break
            last_height = height
            page.evaluate(f"() => window.scrollBy(0, {step_px})")
            page.wait_for_timeout(settle_ms)
        try:
            page.evaluate("() => window.scrollTo(0, 0)")
        except Exception:
            pass

    def _toc_from_html(self, toc_html: str) -> List[Tuple[str, str]]:
        soup = BeautifulSoup(toc_html, "lxml")
        out: List[Tuple[str, str]] = []
        seen = set()
        for a in soup.find_all("a"):
            title = " ".join(a.get_text(" ", strip=True).split())
            href = (a.get("href") or "").strip()
            if not title or not href:
                continue
            full = normalize_url(href, self.from_url)
            key = (title, full)
            if key in seen:
                continue
            seen.add(key)
            out.append((title, full))
        return out

    def run(self) -> None:
        recorder = NetworkImageRecorder(self.out_dir)

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

            # Scroll to force lazy images
            self._auto_scroll(page)

            toc_html = self._pick_best_outerhtml(page, self.TOC_SELECTORS)
            content_html = self._pick_best_outerhtml(page, self.CONTENT_SELECTORS)
            if not content_html:
                content_html = page.evaluate("() => document.body.outerHTML")

            browser.close()

        # Parse and prepare doc
        content_soup = BeautifulSoup(content_html, "lxml")
        ensure_heading_ids(content_soup)

        # Belt & suspenders: download image URLs visible in HTML as well
        html_asset_urls = iter_asset_urls(content_soup, self.from_url)
        for u in sorted(html_asset_urls):
            # only images needed
            # (if you want to keep other assets too, remove this if)
            if not u.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
                pass
            lp = local_path_for_url(u, self.out_dir)
            if not lp.exists():
                download_one(self.session, u, lp)

        # Rewrite references to local
        rewrite_asset_links_inplace(content_soup, self.from_url, self.out_dir)

        # Output document with minimal style
        doc_html = minimal_readable_wrapper(str(content_soup), title="Documento (offline)")
        (self.out_dir / "document.html").write_text(doc_html, encoding="utf-8")

        # Build index: prefer TOC, fallback to headings
        toc_pairs: List[Tuple[str, str]] = []
        if toc_html:
            toc_pairs = self._toc_from_html(toc_html)

        if not toc_pairs:
            # fallback from headings
            for h in content_soup.find_all(["h1", "h2"]):
                t = " ".join(h.get_text(" ", strip=True).split())
                hid = h.get("id")
                if t and hid:
                    toc_pairs.append((t, f"#{hid}"))
                if len(toc_pairs) >= 250:
                    break

        (self.out_dir / "index.html").write_text(build_index_html(toc_pairs), encoding="utf-8")

        print(f"[i] Captured images via network: {len(recorder.saved)} (failed: {len(recorder.failed)})")


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

    def run(self) -> None:
        host, scope_dir_url = self._scope()

        index_soup = self._fetch_soup(self.from_url)

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

        # Build unified doc with robust anchors
        doc = BeautifulSoup("", "lxml")
        container = doc.new_tag("div")
        container["id"] = "offline-doc"
        doc.append(container)

        toc: List[Tuple[str, str]] = []

        for i, (url, psoup) in enumerate(pages, start=1):
            title = self._page_title(psoup)
            anchor = f"page-{i}"
            toc.append((title, f"#{anchor}"))

            sec = doc.new_tag("section")
            sec["id"] = anchor
            h1 = doc.new_tag("h1")
            h1.string = title
            sec.append(h1)

            main = self._extract_main(psoup)
            sec.append(BeautifulSoup(str(main), "lxml"))
            container.append(sec)

        ensure_heading_ids(doc)

        # Download assets from all pages
        asset_urls: Set[str] = set()
        for url, psoup in pages:
            asset_urls |= iter_asset_urls(psoup, url)

        for u in tqdm(sorted(asset_urls), desc="Downloading assets", unit="file"):
            lp = local_path_for_url(u, self.out_dir)
            if not lp.exists():
                download_one(self.session, u, lp)

        # Rewrite to local
        rewrite_asset_links_inplace(doc, scope_dir_url, self.out_dir)

        # Output
        doc_html = minimal_readable_wrapper(str(doc), title="Documento (offline)")
        (self.out_dir / "document.html").write_text(doc_html, encoding="utf-8")
        (self.out_dir / "index.html").write_text(build_index_html(toc), encoding="utf-8")


# ----------------------------
# Main
# ----------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-url", required=True)
    ap.add_argument("--to-dir", required=True)
    ap.add_argument("--user-agent", default="Mozilla/5.0 (X11; Linux x86_64) htmldownloader/1.0")
    args = ap.parse_args()

    from_url = args.from_url.strip()
    out_dir = Path(args.to_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": args.user_agent})

    registry = DownloaderRegistry()
    registry.register(DocumentViewerDownloader)
    registry.register(DoxygenExportDownloader)

    dl_cls = registry.detect(from_url, session)
    downloader = dl_cls(from_url, out_dir, session)

    print(f"[i] Using downloader: {downloader.name}")
    downloader.run()

    print("[ok] Saved:")
    print(f"  - {out_dir / 'index.html'}")
    print(f"  - {out_dir / 'document.html'}")
    print(f"  - {out_dir / 'assets'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
