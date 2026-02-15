# __init__.py | Python | 12L | 0 symbols | 2 imports | 1 comments
> Path: `/home/ogekuri/HtmlDownloader/src/htmldownloader/__init__.py`
> Punto di ingresso del pacchetto per l'automazione HtmlDownloader. Questo file espone metadati leggeri e una riesportazione comoda del punto di ingresso CLI `main`, cosi i chiamanti possono usare `f...

## Imports
```
from .version import __version__
from .cli import main  # riesportazione del punto di ingresso CLI
```


---

# __main__.py | Python | 7L | 0 symbols | 2 imports | 1 comments
> Path: `/home/ogekuri/HtmlDownloader/src/htmldownloader/__main__.py`
> Consente l'esecuzione dello strumento come modulo.

## Imports
```
from .cli import main
import sys
```


---

# cli.py | Python | 4763L | 184 symbols | 21 imports | 196 comments
> Path: `/home/ogekuri/HtmlDownloader/src/htmldownloader/cli.py`
> htmldownloader.py Downloader offline multi-formato per: ...

## Imports
```
from __future__ import annotations
import argparse
import mimetypes
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, urldefrag, unquote
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import uuid
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from .version import __version__
import re
import re
from bs4 import NavigableString
```

## Definitions

- var `GITHUB_API_TIMEOUT_S = 1` (L47)
### fn `def _parse_version_tuple(v: str) -> Optional[Tuple[int, ...]]` `priv` (L50-63)
L53> `return None`
L57> `return None`
L59> `return tuple(int(p) for p in v.split("."))`
L61> `return None`

### fn `def _is_version_newer(latest: str, current: str) -> bool` `priv` (L64-74)
L68> `return False`
L72> `return latest_t > current_t`

### fn `def _get_latest_version_from_github(owner: str, repo: str) -> Optional[str]` `priv` (L75-97)
L86> `return None`
L89> `return None`
L93> `return tag if _parse_version_tuple(tag) else None`
L95> `return None`

### fn `def check_for_new_version(program: str, current_version: str) -> None` (L98-113)
L99-102> Check GitHub releases for a newer version. Any failure is treated as "no update" and produces no output.
L106> `return`

### fn `def safe_filename(path: str) -> str` (L119-125)
L116> ----------------------------
L123> `return path`

### fn `def positive_int(value: str) -> int` (L126-135)
L130> `raise argparse.ArgumentTypeError("deve essere un intero") from exc`
L132> `raise argparse.ArgumentTypeError("deve essere un intero positivo")`
L133> `return parsed`

### fn `def is_http_url(s: str) -> bool` (L136-143)
L139> `return u.scheme in ("http", "https")`
L141> `return False`

### fn `def normalize_url(u: str, base: str) -> str` (L144-152)
L147> `return u`
L149> `return u`
L150> `return urljoin(base, u)`

### fn `def ensure_parent(p: Path) -> None` (L153-156)

### fn `def local_path_for_url(asset_url: str, out_dir: Path) -> Path` (L157-175)
L158-160> Map URL -> out_dir/assets/<host>/<path> (with query fingerprint if present)
L173> `return out_dir / "assets" / host / p`

### fn `def download_one(` (L176-177)

### fn `def escape_html(s: str) -> str` (L192-201)
L193> `return (`

### class `class TocNode` `@dataclass` (L203-208)

### fn `def limit_toc_nodes(nodes: List[TocNode], max_entries: Optional[int]) -> List[TocNode]` (L209-229)
L210> Tronca la TOC alle prime ``max_entries`` voci in visita pre-order.
L212> `return nodes`
L225> `return out`
L227> `return trim_list(nodes)`

### fn `def trim_list(items: List[TocNode]) -> List[TocNode]` (L216-226)
L225> `return out`

### fn `def ensure_heading_ids(soup: BeautifulSoup) -> None` (L230-248)

### fn `def strip_styles(soup: BeautifulSoup) -> None` (L249-261)
L250> Remove external stylesheets, inline styles, style tags, and class attributes.

### fn `def toc_from_headings(soup: BeautifulSoup) -> List[TocNode]` (L262-283)
L281> `return nodes`

### fn `def toc_from_nav_html(toc_html: str, base_url: str) -> List[TocNode]` (L284-321)
L292> Check for title-only elements (e.g., <li class="toc-title">)
L296> Create a node without href (will be rendered as plain text)
L309> `return items`
L313> fallback: attempt with any list if no top-level found
L317> Process only the first list to avoid duplicates from multiple nav structures
L319> `return out`

### fn `def parse_list(list_el) -> List[TocNode]` (L287-310)
L292> Check for title-only elements (e.g., <li class="toc-title">)
L296> Create a node without href (will be rendered as plain text)
L309> `return items`

### fn `def nav_outline_from_html(nav_html: str) -> str` (L322-361)
L323> Produce a deterministic, ASCII outline from the expanded nav tree HTML.
L330> `return clean.replace(" ", "_")`
L334> `return "*"`
L336> `return "o"`
L337> `return "#"`
L359> `return "\n".join(lines)`

### fn `def norm_text(t: str) -> str` (L328-331)
L330> `return clean.replace(" ", "_")`

### fn `def bullet(depth: int) -> str` (L332-338)
L334> `return "*"`
L336> `return "o"`
L337> `return "#"`

### fn `def walk_ul(ul, depth: int) -> None` (L339-355)

- var `ASSET_ATTRS = [` (L362)
- var `HEADING_TAG_RE = re.compile(r"^h[1-6]$")` (L369)
### class `class Logger` (L372-394)
- fn `def __init__(self, verbose: bool = False, debug: bool = False)` `priv` (L375-378) L373> Minimal stdout logger with gating for verbose/debug output.
- fn `def info(self, msg: str) -> None` (L379-381)
- fn `def verbose(self, msg: str) -> None` (L382-385)
- fn `def debug(self, msg: str) -> None` (L386-389)
- fn `def check(self, msg: str) -> None` (L390-394)

### class `class UpgradeAction(argparse.Action)` : argparse.Action (L395-418)
- fn `def __call__(` `priv` (L396-401)

### class `class VersionedArgumentParser(argparse.ArgumentParser)` : argparse.ArgumentParser (L419-443)
- fn `def __init__(self, *args, version: str = "", **kwargs)` `priv` (L426-429) L420> ArgumentParser that appends the program version to the usage line. The version string is appended...
- fn `def format_usage(self) -> str` (L430-443)
  L433> `return s`
  L434> Append version to the first line of the usage (preserve trailing parts)
  L437> `return s`
  L441> `return first + rest`

### fn `def iter_asset_urls(soup: BeautifulSoup, page_url: str) -> Set[str]` (L444-475)
L463> inline background-image url(...)
L473> `return urls`

### fn `def rewrite_asset_links_inplace(` (L476-477)

### fn `def to_rel(u: str) -> str` (L479-485)
L482> `return u`
L484> `return lp.relative_to(out_dir).as_posix()`

### fn `def repl(m)` (L509-512)
L511> `return f"url('{to_rel(raw)}')"`

- var `ALLOWED_EXTERNAL_LINK_SCHEMES = {` (L516)
### fn `def normalize_document_links_inplace(soup: BeautifulSoup, logger: Optional[Logger]) -> None` (L524-651)
L525-533> Normalize <a href> links inside document.html. Allowed outcomes: - External links with explicit scheme (http/https/ftp/ftps) - In-document anchors of the form #<id> where <id> exists in the document Any other href is either rewritten to an in-document anchor (if the fragment exists) or made non-clickable by removing the href attribute.
L536> `return`
L538> Index document ids case-insensitively
L570> Direct in-document anchor
L584> Normalize casing
L594> Unknown fragment → drop href
L607> External link with explicit scheme
L612> Attempt to rewrite any URL-with-fragment to a local in-doc anchor
L632> No fragment and not an allowed external scheme → drop href

### fn `def build_toc_html(` (L652-655)

### fn `def resolved_href(href: str) -> str` (L657-665)
L661> `return f"{document_filename}#{frag}"`
L663> `return f"{document_filename}{href}"`
L664> `return document_filename`

### fn `def render_nodes(nodes: List[TocNode]) -> str` (L666-677)
L668> `return ""`
L676> `return f"<ul>{''.join(items)}</ul>"`

### fn `def build_frameset_index(` (L699-700)
L680> return f"""<!doctype html>
L681> <html lang="it">
L682> <head>
L683> <meta charset="utf-8"/>
L684> ...

### fn `def minimal_readable_wrapper(` (L722-723)
L702> return f"""<!doctype html>
L703> <html lang="it">
L704> <head>
L705> <meta charset="utf-8"/>
L706> ...

### class `class BaseDownloader` (L744-943)
L741> ----------------------------
L887> Prune TOC entries at depth >=7 and remove heading prefixes from TOC links and document headings.
L899> Process toc.html
L906> Prune TOC at depth >=7
L924> root ul depth 1, li depth 2
L926> Clean heading prefixes from TOC links
L933> Process document.html
L938> Clean heading prefixes from headings
L943> If we pruned deep TOC entries, demote their corresponding headings in document.html.
- fn `def __init__(` `priv` (L747-755)
- fn `def matches_url(cls, url: str) -> bool` (L787-789)
  L788> `return False`
- fn `def probe_html(cls, url: str, html: str) -> bool` (L791-793)
  L792> `return False`
- fn `def run(self) -> None` (L794-796)
  L795> `raise NotImplementedError`
- fn `def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]` `priv` (L797-799)
  L798> `return toc_from_nav_html(toc_html, self.from_url)`
- fn `def post_process(self) -> None` (L800-809)
  L801> Execute post-processing pipeline to verify generated files.
  L808> `raise`
- fn `def _verify_toc_consistency(self) -> None` `priv` (L810-857)
  L811-812> Verify that each link in toc.html points to an existing anchor in document.html and that the link text matches the heading text in document.html.
  L816> `return`
  L821> Find all links in TOC
  L835> Find corresponding element in document.html
  L843> Check if it's a heading and text matches
- fn `def _verify_toc_depth(self) -> None` `priv` (L858-885)
  L859> Verify the maximum depth of the TOC and warn if it exceeds 6 levels.
  L862> `return`
  L868> `return current_depth`
  L874> `return max_d`
- fn `def get_max_depth(ul, current_depth=0)` (L866-875)
  L868> `return current_depth`
  L874> `return max_d`
- fn `def href_fragment_id(href: str) -> str` (L892-898)
  L895> `return ""`
  L897> `return (frag or "").strip()`
- fn `def prune_ul(ul, depth)` (L910-923)

### fn `def _prune_toc_and_clean_headings(self) -> None` `priv` (L886-975)
L887> Prune TOC entries at depth >=7 and remove heading prefixes from TOC links and document headings.
L895> `return ""`
L897> `return (frag or "").strip()`
L899> Process toc.html
L906> Prune TOC at depth >=7
L924> root ul depth 1, li depth 2
L926> Clean heading prefixes from TOC links
L933> Process document.html
L938> Clean heading prefixes from headings
L943> If we pruned deep TOC entries, demote their corresponding headings in document.html.
L944> A heading is associated to a pruned TOC entry if:
L945> - the heading id is referenced by a pruned TOC href, OR
L946> - the heading is contained in a div/section whose id is referenced by a pruned TOC href.

### fn `def _deduplicate_toc_entries(self) -> None` `priv` (L976-1034)
L977-985> Remove TOC entries that point to an anchor already referenced earlier. The function processes `toc.html` in reading (pre-order) order. When an entry is found that references a fragment already seen, the entry is removed and any child <li> elements (if present) are promoted to the current parent list at the same position, preserving order. Processing continues at the promoted child (or next sibling) as described in the requirement.
L988> `return`
L995> `return ""`
L997> `return (frag or "").strip().lower()`
L1001> `return`
L1003> Use TocNode representation for safer manipulation: parse TOC to TocNode
L1004> objects, process them in reading order and rebuild HTML from nodes.
L1013> promote children: process children and extend at this level
L1021> process children recursively
L1025> `return out`
L1027> Build TocNode list from the captured TOC HTML and process with the
L1028> TocNode-based algorithm, then rebuild the TOC HTML deterministically.

### fn `def href_fragment_id(href: str) -> str` (L992-998)
L995> `return ""`
L997> `return (frag or "").strip().lower()`

### fn `def process_nodes(nodes: List[TocNode], seen: Set[str]) -> List[TocNode]` (L1005-1026)
L1003> Use TocNode representation for safer manipulation: parse TOC to TocNode
L1013> promote children: process children and extend at this level
L1021> process children recursively
L1025> `return out`

### fn `def _enforce_toc_headings(self) -> None` `priv` (L1035-1137)
L1036-1043> Convert to bold uppercase the headings (h1-h6) that are NOT referenced by toc.html. A heading is considered referenced if: - its own id is referenced by a toc.html href, OR - it is contained in a div/section whose id is referenced by a toc.html href. If referenced, verify the heading level matches the TOC nesting level and correct hx accordingly.
L1047> `return`
L1055> `return ""`
L1057> `return (frag or "").strip()`
L1059> Map fragment id -> toc depth (depth = number of UL ancestors)
L1076> `return 1`
L1078> `return 6`
L1079> `return depth_i`
L1090> `return pid_l`
L1091> `return ""`
L1093> Process headings in document.html
L1111> Not referenced: convert to bold uppercase non-heading
L1120> Referenced: correct heading level based on TOC depth.
L1121> For container-based references, correct only the first heading inside that container
L1122> to avoid flattening internal structure.
L1135> Write back document.html

### fn `def href_fragment_id(href: str) -> str` (L1052-1058)
L1055> `return ""`
L1057> `return (frag or "").strip()`

### fn `def clamp_heading_level(depth: int) -> int` (L1070-1080)
L1076> `return 1`
L1078> `return 6`
L1079> `return depth_i`

### fn `def find_referenced_container_id(h) -> str` (L1081-1092)
L1090> `return pid_l`
L1091> `return ""`

### fn `def _test_toc_headings(self) -> None` `priv` (L1138-1310)
L1135> Write back document.html
L1139> Verifica finale: TOC e heading devono essere coerenti e allo stesso livello.
L1143> `return`
L1152> `return ""`
L1154> `return (frag or "").strip()`
L1161> `return max(1, min(6, value))`
L1177> `return`
L1282> `return ""`
L1286> `return preview`
L1307> `raise ValueError("test_toc_headings: " + "; ".join(issues))`

### fn `def href_fragment_id(href: str) -> str` (L1149-1155)
L1152> `return ""`
L1154> `return (frag or "").strip()`

### fn `def clamp_heading_level(depth: int) -> int` (L1156-1162)
L1161> `return max(1, min(6, value))`

### fn `def summarize(items: List[str]) -> str` (L1280-1287)
L1282> `return ""`
L1286> `return preview`

### fn `def fix_heading_ref_position(self) -> None` (L1311-1453)
L1312-1319> Sposta gli id referenziati dalla TOC sugli heading h1..h6. Se un fragment `#...` in toc.html punta a un contenitore (div/section/...), e quel contenitore contiene almeno un heading h1..h6, allora l'id viene spostato sul primo heading contenuto e rimosso dal contenitore. Al termine, tutti gli href della TOC devono puntare a heading (h1..h6).
L1324> `return`
L1347> `return`
L1349> Build an index of ids in the document (case-insensitive).
L1393> Remove id from the container and assign the TOC fragment id to the heading.
L1401> Try to preserve the old heading id by moving it to the container,
L1402> but only if it does not collide with another element.
L1413> Re-index after modifications and ensure all TOC href fragments point to headings.
L1450> `raise ValueError("fix_heading_ref_position: " + "; ".join(issues))`

### fn `def fix_heading_numbering(self) -> None` (L1454-1569)
L1455-1462> Normalizza il numbering di TOC e heading in base alla struttura della TOC. Operazioni: 1) Rimuove prefissi numerici pre-esistenti (es: "1 ", "1.", "1.2 ", "1.2.") da toc.html (testo dei link) e da document.html (heading h1..h6). 2) Se non e' attivo --disable-numbering, aggiunge una numerazione coerente con posizione e livello nella TOC sia in toc.html sia nei relativi heading.
L1470> `return`
L1472> Matches: "1 ", "1.", "1.2 ", "1.2.", "1.2.3 ", "1.2.3.", ...
L1476> `return " ".join((text or "").split())`
L1479> `return normalize_ws(numbering_prefix_re.sub("", normalize_ws(text)))`
L1488> Phase 1: remove existing numbering from all TOC link texts
L1494> Phase 1: remove existing numbering from all headings in the document
L1503> `return`
L1505> Build numbering from TOC structure (depth inferred from UL nesting)
L1509> `return ""`
L1511> `return (frag or "").strip()`
L1525> Maintain counters per depth
L1544> Apply numbering to corresponding headings (by fragment id)

### fn `def normalize_ws(text: str) -> str` (L1475-1477)
L1472> Matches: "1 ", "1.", "1.2 ", "1.2.", "1.2.3 ", "1.2.3.", ...
L1476> `return " ".join((text or "").split())`

### fn `def strip_numbering_prefix(text: str) -> str` (L1478-1480)
L1479> `return normalize_ws(numbering_prefix_re.sub("", normalize_ws(text)))`

### fn `def set_flat_text(tag, text: str) -> None` (L1481-1484)

### fn `def href_fragment_id(href: str) -> str` (L1506-1512)
L1505> Build numbering from TOC structure (depth inferred from UL nesting)
L1509> `return ""`
L1511> `return (frag or "").strip()`

### fn `def _clean_document_style(self) -> None` `priv` (L1570-1585)
L1571> Remove all style references from document.html and toc.html.
L1572> Process document.html
L1579> Process toc.html

### fn `def _add_document_style(self) -> None` `priv` (L1586-1616)
L1587-1591> Add border lines to tables and images in document.html by injecting CSS styles. Images that are not inside a table receive a border with the same thickness as table borders (1px solid black).
L1594> `return`
L1598> Check if there are any tables or images in the document
L1602> `return`
L1604> Create or find the head element
L1612> `return`
L1614> Create style tag with table border CSS and image border CSS

### fn `def _normalize_document_links(self) -> None` `priv` (L1631-1645)
L1632-1637> Normalize all <a href> links in document.html. Allowed links: - External URLs with explicit scheme (http/https/ftp/ftps) - In-document anchors (#id) where id exists in document.html
L1640> `return`

### fn `def _remove_unused_images(self) -> None` `priv` (L1646-1682)
L1647> Remove image files under assets/ that are not referenced in HTML files.
L1650> `return`
L1652> Read HTML contents to search references
L1675> If neither the relative path nor the basename appear in the HTML, delete

### fn `def _remove_unused_assets(self) -> None` `priv` (L1683-1716)
L1684-1688> Remove asset files under assets/ that are not referenced in document.html. The check is performed only against document.html contents and considers both the relative path from the output directory and the plain filename.
L1691> `return`
L1709> If neither the relative path nor the basename appear in document.html, delete

### fn `def _normalize_image_position(self) -> None` `priv` (L1717-1771)
L1718> Move images from nested asset subdirs to the root of `assets/` adding a uuid suffix and update HTML refs.
L1721> `return`
L1729> Collect image files under assets recursively
L1733> skip files already in the root of assets
L1744> ensure unique
L1760> Update references in HTML files

### fn `def _clean_assets_tree(self) -> None` `priv` (L1772-1789)
L1773> Remove empty directories under assets/ starting from leaves.
L1776> `return`
L1778> Walk directories bottom-up and try to remove empty ones
L1779> Use sorted(reverse=True) to attempt children before parents
L1783> rmdir only if empty
L1787> not empty or cannot remove, ignore

### fn `def _remove_empty_assets_root(self) -> None` `priv` (L1790-1829)
L1787> not empty or cannot remove, ignore
L1791-1797> Remove the top-level `assets/` directory if it is empty. This runs after `_clean_assets_tree` and will delete the `assets` directory only if there are no files and no non-empty subdirectories remaining. Logs a verbose message when removed and a debug message if removal fails.
L1800> `return`
L1802> Check for any files or non-empty directories under assets
L1805> if any file exists, or any directory that contains something, mark
L1806> as non-empty
L1812> if dir contains any children, it's non-empty
L1821> `return`

### class `class DownloaderRegistry` (L1830-1862)
- fn `def __init__(self)` `priv` (L1831-1833)
- fn `def register(self, downloader_cls: type[BaseDownloader]) -> None` (L1834-1836)
- fn `def detect(self, url: str, session: requests.Session) -> type[BaseDownloader]` (L1837-1862)
  L1840> `return url_matches[0]`
  L1852> `return html_matches[0]`
  L1855> `return html_matches[0]`
  L1857> `return url_matches[0]`
  L1858> `raise RuntimeError(`

### fn `def guess_ext_from_content_type(ct: str) -> str` (L1868-1881)
L1865> ----------------------------
L1871> `return ""`
L1874> `return ".js"`
L1876> `return ".css"`
L1878> `return "." + ct.split("/", 1)[1]`
L1879> `return ext`

### class `class NetworkImageRecorder` (L1882-1924)
- fn `def __init__(self, out_dir: Path)` `priv` (L1888-1892) L1883> Capture ALL image responses loaded by the browser (TI viewer loads many images lazily / via CSS)....
- fn `def attach(self, page)` (L1893-1924)
  L1898> `return`
  L1901> `return`
  L1903> `return`
- fn `def on_response(resp)` (L1894-1921)
  L1898> `return`
  L1901> `return`
  L1903> `return`

### class `class DocumentViewerDownloader(BaseDownloader)` : BaseDownloader (L1925-2124)
L1938> TI's actual content area component
L1939> Content area class
L1940> Alternative content class
L1941> TI's content loading area
L1942> Card wrapper containing document sections
- var `TOC_SELECTORS = [` (L1928)
- var `CONTENT_SELECTORS = [` (L1937)
- var `TOC_SCROLL_SELECTORS = [` (L1950)
- fn `def matches_url(cls, url: str) -> bool` (L1959-1962)
  L1961> `return ("ti.com" in u.netloc) and ("/document-viewer/" in u.path)`
- fn `def probe_html(cls, url: str, html: str) -> bool` (L1964-1967)
  L1966> `return "document-viewer" in h`
- fn `def _pick_best_outerhtml(self, page, selectors: List[str]) -> Optional[str]` `priv` (L1968-1991)
  L1986> `return None`
  L1988> `return best.evaluate("el => el.outerHTML")`
  L1990> `return None`
- fn `def _expand_full_toc(` `priv` (L1992-1993)
- fn `def _scroll_toc_container(` `priv` (L2044-2045)

### fn `def _find_scroll_container(self, page)` `priv` (L2092-2150)
L2126> `return best`
L2147> `return element`
L2149> `return None`

### fn `def _auto_scroll_element(` `priv` (L2151-2159)

### fn `def _auto_scroll(` `priv` (L2219-2225)

### fn `def _collect_cards_from_container(` `priv` (L2284-2291)

### fn `def _best_card_for_fragment(` `priv` (L2357-2358)

### fn `def score_value(val: str) -> int` (L2369-2383)
L2371> `return 0`
L2374> `return 100`
L2376> `return 80`
L2379> `return 70`
L2381> `return 40`
L2382> `return 0`

### fn `def _fragment_matches_url(self, fragment: str, data_url: str) -> bool` `priv` (L2400-2411)
L2403> `return False`
L2410> `return all(part in target for part in parts)`

### fn `def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]` `priv` (L2412-2414)
L2413> `return toc_from_nav_html(toc_html, self.from_url)`

### fn `def _iter_nodes(nodes: List[TocNode]) -> Iterable[TocNode]` `priv` `@staticmethod` (L2416-2420)
L2418> `yield n`
L2419> `yield from DocumentViewerDownloader._iter_nodes(n.children)`

### fn `def _first_numeric_index(nodes: List[TocNode]) -> Optional[int]` `priv` `@staticmethod` (L2422-2428)
L2426> `return i`
L2427> `return None`

### fn `def _trim_toc_nodes(nodes: List[TocNode]) -> List[TocNode]` `priv` `@staticmethod` (L2430-2446)
L2431> Trim TOC for display: start from first "1 " entry, drop trailing IMPORTANT NOTICE.
L2433> `return []`
L2445> `return trimmed if trimmed else list(nodes)`

### fn `def _limit_toc_nodes(` `priv` `@staticmethod` (L2448-2449)

### fn `def _limit_by_reading_order(` `priv` `@staticmethod` (L2454-2455)

### fn `def _prune_toc_to_allowed(` `priv` `@staticmethod` (L2487-2488)

### fn `def _first_toc_entry_title(nodes: List[TocNode]) -> Optional[str]` `priv` `@staticmethod` (L2505-2511)
L2509> `return title`
L2510> `return None`

### fn `def _is_important_notice_label(title: Optional[str]) -> bool` `priv` `@staticmethod` (L2513-2516)
L2515> `return text.startswith("important notice")`

### fn `def _is_important_notice_section(section_html: str) -> bool` `priv` `@staticmethod` (L2518-2527)
L2524> `return True`
L2526> `return "important notice and disclaimer" in flat_text`

### fn `def _select_section_nodes(nodes: List[TocNode]) -> List[TocNode]` `priv` `@staticmethod` (L2529-2553)
L2530-2534> Choose the slice of TOC nodes to download: from first title starting with 1 " through the last occurrence of "IMPORTANT NOTICE" (inclusive). If missing, fall back to the full list.
L2537> `return []`
L2552> `return flat[start_idx : end_idx + 1]`

### fn `def _dedup_toc_nodes_by_href(self, nodes: List[TocNode]) -> List[TocNode]` `priv` (L2554-2580)
L2555> Merge duplicate TOC nodes by normalized href within same parent level.
L2558> Scope seen to this level only
L2562> Recursively deduplicate children first
L2567> Merge children and prefer the more descriptive/structured title
L2577> `return out`
L2579> `return dedup_list(nodes)`

### fn `def dedup_list(items: List[TocNode]) -> List[TocNode]` (L2557-2578)
L2555> Merge duplicate TOC nodes by normalized href within same parent level.
L2558> Scope seen to this level only
L2562> Recursively deduplicate children first
L2567> Merge children and prefer the more descriptive/structured title
L2577> `return out`

### fn `def _is_section_scrollable(self, page, viewport_multiplier: float = 2.0) -> bool` `priv` (L2581-2600)
L2582-2586> Verifica se la sezione attuale ha contenuto sufficiente per permettere scroll. Una sezione è considerata scrollable se scrollHeight è almeno (viewport_multiplier * clientHeight). Default: almeno 2x l'altezza del viewport.
L2597> `return bool(result)`
L2599> `return False`

### fn `def _remove_toc_elements(self, soup: BeautifulSoup) -> None` `priv` (L2601-2634)
L2602-2605> Remove TOC/navigation elements from captured content to prevent contamination of document.html with navigation tree.
L2606> Remove by tag name (TI custom components)
L2616> Remove by selector
L2618> Main navigation tree
L2619> Sidebar container
L2620> TOC contents section
L2621> Tab bar
L2622> Tab slider navigation
L2623> Document lister title (captured separately)
L2624> TOC hierarchy container
L2625> Mini navigation controls
L2626> TOC by data attribute
L2627> Tab bar by data attribute
L2628> TOC by data attribute
L2629> Command bar

### fn `def _convert_doxygen_definition_lists(self, soup: BeautifulSoup) -> None` `priv` (L2635-2706)
L2636-2647> Convert Doxygen-style definition lists and textual "term / : description pairs into inline bold uppercase labels followed by the description. Examples: <dl><dt>Attention</dt><dd>Please be aware...</dd></dl> -> <p><strong>ATTENTION:</strong> Please be aware...</p> <p>Attention</p> <p>:   Please be aware...</p> -> <p><strong>ATTENTION:</strong> Please be aware...</p>
L2649> Handle <dl><dt>/<dd> pairs first
L2663> Handle adjacent paragraph style variations:
L2664> 1) <p>Label</p> + <p>: description</p>
L2665> 2) <p>Label</p> + <p>:</p> + <p>description</p>
L2675> Case A: right paragraph starts with a colon followed by text
L2687> Case B: right paragraph is just a colon (possibly with spaces)
L2698> remove the marker and the description nodes
L2702> Otherwise, not a definition-style pair
L2704> Non-fatal: if conversion fails, leave document unchanged
L2705> `return`

### fn `def _extract_fragment_only(` `priv` (L2707-2708)
L2704> Non-fatal: if conversion fails, leave document unchanged

### fn `def score_value(val: str) -> int` (L2720-2737)
L2722> `return 0`
L2725> `return 100`
L2727> `return 80`
L2736> `return score`

### fn `def pick_best_section(elements)` (L2738-2755)
L2754> `return best`

### fn `def matches_fragment(el) -> bool` (L2766-2779)
L2768> `return False`
L2771> `return True`
L2774> `return True`
L2777> `return True`
L2778> `return False`

### fn `def _wait_for_fragment(self, page, fragment: str, timeout_ms: int = 8000) -> bool` `priv` (L2807-2850)
L2810> `return True`
L2845> `return True`
L2847> `return False`
L2849> `return False`

### fn `def _click_toc_link(self, page, fragment: str) -> bool` `priv` (L2851-2871)
L2854> `return False`
L2856> `return bool(`
L2870> `return False`

### fn `def run(self) -> None` (L2872-3071)
L2885> `return cand`
L2890> `return value.lower()`
L2896> `return section_html`
L2910> `return section_html`
L2915> `return str(section)`
L2931> Expand navigation tree (with repeated passes and scroll in TOC) to capture full TOC
L2953> Also capture doc-lister title if present (TI pages have this as a separate element)
L2974> Prepend doc title if captured separately
L2991> Apply reading-order limit: take the first <limit> entries across all levels
L3020> (full_url_with_fragment, anchor, title, fragment)
L3023> Map section index to TOC node
L3026> Map section URL -> anchor kept in document
L3029> Map normalized fragment -> chosen anchor
L3044> Choose/reuse anchor for this fragment (regardless of whether it will be downloaded)
L3051> Reuse anchor for repeated section URLs so TOC always points to a kept section
L3065> For TI document-viewer, the fragment determines which content is loaded
L3066> Use the full URL with fragment to ensure unique content per section

### fn `def make_anchor(raw_fragment: str, title: str, used: Set[str]) -> str` (L2876-2886)
L2885> `return cand`

### fn `def normalize_text(value: str) -> str` (L2887-2891)
L2890> `return value.lower()`

### fn `def strip_ti_disclaimer(section_html: str) -> str` (L2892-2916)
L2896> `return section_html`
L2910> `return section_html`
L2915> `return str(section)`

### class `class DoxygenExportDownloader(BaseDownloader)` : BaseDownloader (L3324-3523)
L3321> ----------------------------
L3447> `return out`
L3480> Track expanded items for limit enforcement
L3483> Expand systematically by clicking on arrows multiple times
L3485> Increased rounds for deep nesting
- fn `def matches_url(cls, url: str) -> bool` (L3328-3334)
  L3330> TI export path typically contains /exports/ and ends with index.html
  L3331> `return ("/exports/" in u.path and url.lower().endswith(".html")) or (`
- fn `def probe_html(cls, url: str, html: str) -> bool` (L3336-3339)
  L3338> `return ('name="generator"' in h and "doxygen" in h) or ("dynsections.js" in h)`
- fn `def _scope(self) -> Tuple[str, str]` `priv` (L3340-3347)
  L3346> `return host, scope_dir_url`
- fn `def _fetch_soup(self, url: str) -> BeautifulSoup` `priv` (L3348-3352)
  L3351> `return BeautifulSoup(r.text, "lxml")`
- fn `def _is_in_scope(self, url: str, host: str, scope_dir_url: str) -> bool` `priv` (L3353-3360)
  L3355> `return False`
  L3358> `return False`
  L3359> `return url.startswith(scope_dir_url)`
- fn `def _page_title(self, soup: BeautifulSoup) -> str` `priv` (L3361-3369)
  L3364> `return t.get_text(strip=True)`
  L3367> `return " ".join(h1.get_text(" ", strip=True).split())`
  L3368> `return "Page"`
- fn `def _document_title(self, soup: BeautifulSoup) -> str` `priv` (L3370-3394)
  L3375> `return text`
  L3391> `return combined`
  L3393> `return self._page_title(soup)`
- fn `def _extract_main(self, soup: BeautifulSoup) -> BeautifulSoup` `priv` (L3395-3411)
  L3402> Remove TOC elements from page content
  L3410> `return frag`
- fn `def _remove_toc_elements(self, soup: BeautifulSoup) -> None` `priv` (L3412-3432)
  L3413> Remove TOC/navigation elements from page content to prevent duplication.
  L3415> `return`
  L3417> Remove TOC containers and navigation elements
- fn `def _links_to_html_pages(` `priv` (L3433-3434)
- fn `def _expand_nav_tree(self, page) -> None` `priv` (L3449-3478)
  L3450> Wait for the nav tree to load completely
  L3456> Scroll to make sure all content is loaded
  L3458-3466> (() => { const navTree = document.querySelector('#nav-tree-contents'); if (navTree) { navTree.scrollTop = 0; navTree.scrollIntoView(); } })();
  L3475> Wait for final DOM stabilization

### fn `def _expand_nav_tree_full(self, page) -> None` `priv` (L3479-3678)
L3480> Track expanded items for limit enforcement
L3483> Expand systematically by clicking on arrows multiple times
L3485> Increased rounds for deep nesting
L3487-3567> f ((limit, expandedCount) => {{ const root = document.querySelector('#nav-tree-contents'); if (!root) return {{clicks: 0, expanded: expandedCount}}; let clicks = 0; let currentExpanded = expandedCount; Function to check if an item is an API Reference section or inside one function isApiReferenceRelated(item) {{ Check if this item itself is API Reference const label = item.querySelector('.label'); if (label) {{ const labelText = label.textContent.trim(); if (labelText === 'API Reference') {{ console.log('Found API Reference section, skipping expansion'); return true; }} }} Check if we're inside an API Reference section let parent = item.parentElement; while (parent && parent !== root) {{ if (parent.classList && parent.classList.contains('children_ul')) {{ const parentItem = parent.previousElementSibling; if (parentItem && parentItem.classList && parentItem.classList.contains('item')) {{ const parentLabel = parentItem.querySelector('.label'); if (parentLabel && parentLabel.textContent.trim() === 'API Reference') {{ console.log('Found item inside API Reference section, skipping expansion'); return true; }} }} }} parent = parent.parentElement; }} return false; }} Get all items with arrows that might be expandable const items = Array.from(root.querySelectorAll('div.item')); for (const item of items) {{ Check limit before expanding if (limit && currentExpanded >= limit) {{ console.log('Reached expansion limit:', limit); break; }} const arrow = item.querySelector('.arrow'); if (arrow) {{ const text = arrow.textContent.trim(); if (text === '►' || text === '▶' || text === '+') {{ const label = item.querySelector('.label'); const labelText = label ? label.textContent.trim() : 'no-label'; console.log('Found expandable item:', labelText); Skip API Reference sections and their children if (isApiReferenceRelated(item)) {{ console.log('Skipping API Reference related item:', labelText); continue; }} console.log('Expanding item:', labelText); try {{ arrow.click(); clicks++; currentExpanded++; }} catch (e) {{ try {{ item.click(); clicks++; currentExpanded++; }} catch (e2) {{ Continue to next item }} }} }} }} }} return {{clicks: clicks, expanded: currentExpanded}}; }})({self.limit or "null"}, {expanded_count})
L3578> Stop if limit reached or no more clicks
L3588> Wait for content to load after clicks
L3598> Final pass: force expand any remaining collapsed elements, except API Reference
L3599> Only if we haven't reached the limit
L3602-3676> (() => { const root = document.querySelector('#nav-tree-contents'); if (!root) return; Function to check if an item is API Reference related function isApiReferenceRelated(element) { const item = element.closest('div.item'); if (!item) return false; Check if this item itself is API Reference const label = item.querySelector('.label'); if (label && label.textContent.trim() === 'API Reference') { return true; } Check if we're inside an API Reference section let parent = item.parentElement; while (parent && parent !== root) { if (parent.classList && parent.classList.contains('children_ul')) { const parentItem = parent.previousElementSibling; if (parentItem && parentItem.classList && parentItem.classList.contains('item')) { const parentLabel = parentItem.querySelector('.label'); if (parentLabel && parentLabel.textContent.trim() === 'API Reference') { return true; } } } parent = parent.parentElement; } return false; } Force all arrows to expanded state, except API Reference related const arrows = root.querySelectorAll('.arrow'); arrows.forEach(arrow => { if (!isApiReferenceRelated(arrow)) { const text = arrow.textContent.trim(); if (text === '►' || text === '▶' || text === '+') { arrow.textContent = '▼'; } } }); Force all ul elements to be visible, except those under API Reference But don't set display: block, leave styles empty to match fixture const uls = root.querySelectorAll('ul'); uls.forEach(ul => { if (!isApiReferenceRelated(ul)) { ul.style.visibility = 'visible'; ul.style.height = 'auto'; ul.style.overflow = 'visible'; Don't set display: block to match fixture expectations } }); Ensure API Reference section is collapsed const items = Array.from(root.querySelectorAll('div.item')); for (const item of items) { const label = item.querySelector('.label'); if (label && label.textContent.trim() === 'API Reference') { const arrow = item.querySelector('.arrow'); if (arrow) { arrow.textContent = '►'; // Force collapsed state } Hide children of API Reference const childrenUl = item.parentElement.querySelector('ul.children_ul'); if (childrenUl) { childrenUl.style.display = 'none'; } break; } } })();

### fn `def _expand_nav_tree_limited(self, page, limit: int) -> None` `priv` (L3679-3780)
L3602> (() => {
L3603> const root = document.querySelector('#nav-tree-contents');
L3604> if (!root) return;
L3605> ...
L3684-3759> (limit) => { const root = document.querySelector('#nav-tree-contents > ul'); if (!root) return {expanded: 0, count: 0, reached: false}; let expanded = 0; let count = 0; function isApiReferenceRelated(item) { const label = item.querySelector('.label'); if (label && label.textContent.trim() === 'API Reference') { return true; } let parent = item.parentElement; while (parent) { if (parent.classList && parent.classList.contains('children_ul')) { const parentItem = parent.previousElementSibling; if (parentItem && parentItem.classList && parentItem.classList.contains('item')) { const parentLabel = parentItem.querySelector('.label'); if (parentLabel && parentLabel.textContent.trim() === 'API Reference') { return true; } } } parent = parent.parentElement; } return false; } function arrowState(arrow) { if (!arrow) return 'leaf'; const text = arrow.textContent.trim(); if (text === '▼') return 'expanded'; if (text === '►' || text === '▶' || text === '+') return 'collapsed'; return 'leaf'; } function walk(ul) { const items = Array.from(ul.children).filter(el => el.tagName.toLowerCase() === 'li'); for (const li of items) { if (count >= limit) return true; const item = li.querySelector(':scope > div.item'); if (!item) continue; count += 1; if (count >= limit) return true; const arrow = item.querySelector('.arrow'); const state = arrowState(arrow); let didExpand = false; if (state === 'collapsed' && !isApiReferenceRelated(item)) { try { arrow.click(); expanded += 1; didExpand = true; } catch (e) { try { item.click(); expanded += 1; didExpand = true; } catch (e2) { ignore } } } const childUl = li.querySelector(':scope > ul'); if (childUl && (state === 'expanded' || didExpand)) { if (walk(childUl)) return true; } } return false; } walk(root); return {expanded: expanded, count: count, reached: count >= limit}; } ,

### fn `def _cleanup_nav_tree_styles(self, page) -> None` `priv` (L3781-3805)
L3783-3803> (() => { const root = document.querySelector('#nav-tree-contents'); if (!root) return; Remove display styles from all elements const allElements = root.querySelectorAll('*'); allElements.forEach(el => { if (el.style.display) { el.style.display = ''; } }); Special handling for ul elements - ensure they have empty style const uls = root.querySelectorAll('ul'); uls.forEach(ul => { ul.removeAttribute('style'); ul.setAttribute('style', ''); }); })();

### fn `def _fetch_nav_tree_with_playwright(self) -> Tuple[str, str]` `priv` (L3806-3889)
L3783> (() => {
L3784> const root = document.querySelector('#nav-tree-contents');
L3785> if (!root) return;
L3786> ...
L3833-3863> (() => { const el = document.querySelector('#nav-tree-contents ul'); if (!el) return ''; Clone the element to avoid modifying the original const clone = el.cloneNode(true); Clean up extra styles added during expansion const uls = clone.querySelectorAll('ul'); uls.forEach(ul => { ul.style.visibility = ''; ul.style.height = ''; ul.style.overflow = ''; }); Also clean up the root element itself if (clone.style) { clone.style.visibility = ''; clone.style.height = ''; clone.style.overflow = ''; } Remove only the expansion arrow links (those with arrow spans as siblings) Actually, let's not remove any javascript:void(0) links for now The fixture expects them to be preserved return clone.outerHTML; })()
L3888> `return nav_html, nav_outline`

### fn `def _nav_link_href(self, link, base_url: str) -> str` `priv` (L3890-3907)
L3892> `return ""`
L3895> `return normalize_url(href, base_url)`
L3903> `return normalize_url(f"{page}#{frag}" if frag else page, base_url)`
L3905> `return normalize_url(cls, base_url)`
L3906> `return ""`

### fn `def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]` `priv` (L3908-3910)
L3909> `return toc_from_nav_html(toc_html, "document.html")`

### fn `def _toc_nodes_from_nav_html(self, nav_html: str) -> List[TocNode]` `priv` (L3911-3940)
L3915> `return []`
L3934> `return items`
L3938> `return nodes[0].children`
L3939> `return nodes`

### fn `def parse_ul(ul) -> List[TocNode]` (L3917-3935)
L3934> `return items`

### fn `def _iter_toc_nodes(nodes: List[TocNode]) -> Iterable[TocNode]` `priv` `@staticmethod` (L3942-3946)
L3944> `yield n`
L3945> `yield from DoxygenExportDownloader._iter_toc_nodes(n.children)`

### fn `def _select_main_container(self, soup: BeautifulSoup)` `priv` (L3947-3961)
L3949> `return None`
L3958> `return None`
L3960> `return main`

### fn `def _find_fragment_anchor(self, main, fragment: str)` `priv` (L3962-3981)
L3965> `return None`
L3968> `return None`
L3970> `return target`
L3974> `return parent`
L3979> `return next_heading`
L3980> `return target`

### fn `def _normalize_heading_text(value: str) -> str` `priv` `@staticmethod` (L3983-3985)
L3984> `return " ".join((value or "").split()).strip().lower()`

### fn `def _strip_duplicate_section_title(` `priv` (L3986-3987)

### fn `def _extract_section_html(` `priv` (L4021-4022)

### fn `def direct_child(el)` (L4041-4046)
L4045> `return cur if cur and cur.parent == main else None`

### fn `def _build_toc(self, doc: BeautifulSoup) -> List[TocNode]` `priv` (L4070-4128)
L4074> `return nodes`
L4076> Track content by hash to consolidate duplicates
L4090> Create content hash for deduplication
L4095> Duplicate content - point to existing anchor
L4099> New content - use this section's anchor
L4127> `return nodes`

### fn `def run(self) -> None` (L4129-4328)
L4143> `return`
L4253> Download assets from the touched pages
L4302> `return`
L4308> Crawl pages

- var `MAX_PAGES = 250` (L4309) — Crawl pages
### class `class ResourceExplorerModule` (L4487-4498)
L4484> ----------------------------
L4493> `return None`
- fn `def select(` (L4490-4491)
- fn `def run(self, downloader: "ResourceExplorerDownloader", selection: Dict[str, str]) -> None` (L4495-4498)
  L4496> `raise NotImplementedError`

### class `class RMModuleDoxigen(ResourceExplorerModule)` : ResourceExplorerModule (L4499-4535)
L4508> `return None`
L4513> `return None`
L4516> `return None`
L4518> `return {"doxygen_url": doxygen_url}`
- fn `def select(` (L4504-4505)
- fn `def run(self, downloader: "ResourceExplorerDownloader", selection: Dict[str, str]) -> None` (L4520-4535)
  L4523> `raise RuntimeError("Modulo RMModuleDoxigen: URL Doxygen non valida.")`

### class `class ResourceExplorerDownloader(BaseDownloader)` : BaseDownloader (L4536-4621)
L4558> `return module, selection`
L4559> `return None`
- fn `def __init__(self, *args, **kwargs)` `priv` (L4539-4542)
- fn `def matches_url(cls, url: str) -> bool` (L4544-4547)
  L4546> `return u.netloc.endswith("dev.ti.com") and "/tirex/explore/node" in u.path.lower()`
- fn `def probe_html(cls, url: str, html: str) -> bool` (L4549-4551)
  L4550> `return "css-1aefuid-contentContainer" in (html or "")`
- fn `def _select_module(` `priv` (L4552-4553)
- fn `def _render_with_playwright(self) -> str` `priv` (L4561-4592)
  L4589> `return html`
  L4591> `return ""`
- fn `def run(self) -> None` (L4593-4621)
  L4599> `raise RuntimeError("Impossibile scaricare la pagina Resource Explorer.") from exc`
  L4606> `return`
  L4617> `return`
  L4619> `raise RuntimeError("Nessun modulo Resource Explorer compatibile trovato.")`

### fn `def build_arg_parser() -> argparse.ArgumentParser` (L4627-4667)
L4624> ----------------------------
L4665> `return ap`

### fn `def print_strict_help(program: str, version: str, parser: argparse.ArgumentParser) -> None` (L4668-4714)
L4669-4673> Print the strict help block required by REQ-024. The function prints a fixed header and usage/example blocks and then generates the full list of implemented options from the parser.
L4674> Header
L4678> Usage
L4683> Example(s)
L4688> Fixed core options block
L4695> Generate full list of options from parser._actions (avoid duplicates)
L4697> Collect actions in insertion order
L4700> Skip the help/version that we've already printed
L4706> show metavar for positional/optional arguments where appropriate
L4711> Align to match typical formatting

### fn `def main() -> int` (L4715-4761)
L4717> If executed with no parameters or with -h/--help, print strict help and exit 0
L4720> `return 0`
L4759> `return 0`

## Comments
- L2: htmldownloader.py Downloader offline multi-formato per: ...
- L99: Check GitHub releases for a newer version. Any failure is treated as "no update" and produces no output.
- L114-115: ---------------------------- | Shared helpers
- L158: Map URL -> out_dir/assets/<host>/<path> (with query fingerprint if present)
- L210: Tronca la TOC alle prime ``max_entries`` voci in visita pre-order.
- L250: Remove external stylesheets, inline styles, style tags, and class attributes.
- L292: Check for title-only elements (e.g., <li class="toc-title">)
- L296: Create a node without href (will be rendered as plain text)
- L313: fallback: attempt with any list if no top-level found
- L317: Process only the first list to avoid duplicates from multiple nav structures
- L323: Produce a deterministic, ASCII outline from the expanded nav tree HTML.
- L434: Append version to the first line of the usage (preserve trailing parts)
- L463: inline background-image url(...)
- L525: Normalize <a href> links inside document.html. Allowed outcomes: - External links with explicit scheme (http/https/ftp/ftps) ...
- L538: Index document ids case-insensitively
- L570: Direct in-document anchor
- L584: Normalize casing
- L594: Unknown fragment → drop href
- L607: External link with explicit scheme
- L612: Attempt to rewrite any URL-with-fragment to a local in-doc anchor
- L632: No fragment and not an allowed external scheme → drop href
- L725: return f"""<!doctype html> <html lang="it"> <head> <meta charset="utf-8"/> ...
- L739-740: ---------------------------- | Downloader framework
- L801: Execute post-processing pipeline to verify generated files.
- L811: Verify that each link in toc.html points to an existing anchor in document.html and that the link text matches the heading text in document.html.
- L821: Find all links in TOC
- L835: Find corresponding element in document.html
- L843: Check if it's a heading and text matches
- L859: Verify the maximum depth of the TOC and warn if it exceeds 6 levels.
- L887: Prune TOC entries at depth >=7 and remove heading prefixes from TOC links and document headings.
- L899: Process toc.html
- L906: Prune TOC at depth >=7
- L926: Clean heading prefixes from TOC links
- L933: Process document.html
- L938: Clean heading prefixes from headings
- L943-946: If we pruned deep TOC entries, demote their corresponding headings in document.html. | A heading is associated to a pruned TOC entry if: | - the heading id is referenced by a pruned TOC href, OR | - the heading is contained in a div/section whose id is referenced by a pruned TOC href.
- L977: Remove TOC entries that point to an anchor already referenced earlier. The function processes `toc.html` in reading (pre-order) order. When an entr...
- L1013: promote children: process children and extend at this level
- L1021: process children recursively
- L1027-1028: Build TocNode list from the captured TOC HTML and process with the | TocNode-based algorithm, then rebuild the TOC HTML deterministically.
- L1036: Convert to bold uppercase the headings (h1-h6) that are NOT referenced by toc.html. A heading is considered referenced if: - its own id is referenc...
- L1059: Map fragment id -> toc depth (depth = number of UL ancestors)
- L1093: Process headings in document.html
- L1111: Not referenced: convert to bold uppercase non-heading
- L1120-1122: Referenced: correct heading level based on TOC depth. | For container-based references, correct only the first heading inside that container | to avoid flattening internal structure.
- L1139: Verifica finale: TOC e heading devono essere coerenti e allo stesso livello.
- L1312: Sposta gli id referenziati dalla TOC sugli heading h1..h6. Se un fragment `#...` in toc.html punta a un contenitore (div/section/...), e quel conte...
- L1349: Build an index of ids in the document (case-insensitive).
- L1393: Remove id from the container and assign the TOC fragment id to the heading.
- L1401-1402: Try to preserve the old heading id by moving it to the container, | but only if it does not collide with another element.
- L1413: Re-index after modifications and ensure all TOC href fragments point to headings.
- L1455: Normalizza il numbering di TOC e heading in base alla struttura della TOC. Operazioni: 1) Rimuove prefissi numerici pre-esistenti (es: "1 ", "1.", ...
- L1488: Phase 1: remove existing numbering from all TOC link texts
- L1494: Phase 1: remove existing numbering from all headings in the document
- L1525: Maintain counters per depth
- L1544: Apply numbering to corresponding headings (by fragment id)
- L1571-1572: Remove all style references from document.html and toc.html. | Process document.html
- L1579: Process toc.html
- L1587: Add border lines to tables and images in document.html by injecting CSS styles. Images that are not inside a table receive a border with the same t...
- L1598: Check if there are any tables or images in the document
- L1604: Create or find the head element
- L1614-1626: Create style tag with table border CSS and image border CSS | style_tag.string = table { border-collapse: collapse; } ...
- L1632: Normalize all <a href> links in document.html. Allowed links: - External URLs with explicit scheme (http/https/ftp/ftps) ...
- L1647: Remove image files under assets/ that are not referenced in HTML files.
- L1652: Read HTML contents to search references
- L1675: If neither the relative path nor the basename appear in the HTML, delete
- L1684: Remove asset files under assets/ that are not referenced in document.html. The check is performed only against document.html contents and considers...
- L1709: If neither the relative path nor the basename appear in document.html, delete
- L1718: Move images from nested asset subdirs to the root of `assets/` adding a uuid suffix and update HTML refs.
- L1729: Collect image files under assets recursively
- L1733: skip files already in the root of assets
- L1744: ensure unique
- L1760: Update references in HTML files
- L1773: Remove empty directories under assets/ starting from leaves.
- L1778-1779: Walk directories bottom-up and try to remove empty ones | Use sorted(reverse=True) to attempt children before parents
- L1783: rmdir only if empty
- L1791: Remove the top-level `assets/` directory if it is empty. This runs after `_clean_assets_tree` and will delete the `assets` directory only if there ...
- L1802: Check for any files or non-empty directories under assets
- L1805-1806: if any file exists, or any directory that contains something, mark | as non-empty
- L1812: if dir contains any children, it's non-empty
- L1863-1864: ---------------------------- | Document-viewer (TI) downloader
- L2431: Trim TOC for display: start from first "1 " entry, drop trailing IMPORTANT NOTICE.
- L2457: Return the first ``max_entries`` nodes following pre-order (reading) traversal.
- L2490: Prune a TOC tree to only nodes present in ``allowed_ids`` (by object id), preserving structure.
- L2530: Choose the slice of TOC nodes to download: from first title starting with 1 " through the last occurrence of "IMPORTANT NOTICE" (inclusive). If mis...
- L2562: Recursively deduplicate children first
- L2567: Merge children and prefer the more descriptive/structured title
- L2582: Verifica se la sezione attuale ha contenuto sufficiente per permettere scroll. Una sezione è considerata scrollable se scrollHeight è almeno (viewp...
- L2602-2606: Remove TOC/navigation elements from captured content to prevent contamination of document.html wi... | Remove by tag name (TI custom components)
- L2616: Remove by selector
- L2636-2649: Convert Doxygen-style definition lists and textual "term / : description pairs into inline bold u... | Handle <dl><dt>/<dd> pairs first
- L2663-2665: Handle adjacent paragraph style variations: | 1) <p>Label</p> + <p>: description</p> | 2) <p>Label</p> + <p>:</p> + <p>description</p>
- L2675: Case A: right paragraph starts with a colon followed by text
- L2687: Case B: right paragraph is just a colon (possibly with spaces)
- L2698: remove the marker and the description nodes
- L2702: Otherwise, not a definition-style pair
- L2710: Return soup narrowed to the element matching the fragment id/name, if present (case-insensitive).
- L2756: Prefer a single documentSection card that matches the fragment to avoid duplicated parent cards.
- L2931: Expand navigation tree (with repeated passes and scroll in TOC) to capture full TOC
- L2953: Also capture doc-lister title if present (TI pages have this as a separate element)
- L2974: Prepend doc title if captured separately
- L2991: Apply reading-order limit: take the first <limit> entries across all levels
- L3044: Choose/reuse anchor for this fragment (regardless of whether it will be downloaded)
- L3051: Reuse anchor for repeated section URLs so TOC always points to a kept section
- L3065-3066: For TI document-viewer, the fragment determines which content is loaded | Use the full URL with fragment to ensure unique content per section
- L3113: Download all deduplicated sections (skip scrollability filtering)
- L3116: Download sections starting from the first scrollable one
- L3289-3290: Convert Doxygen-style definition lists and textual definition | pairs into inline bold uppercase labels to improve text retrieval
- L3319-3320: ---------------------------- | Doxygen-export downloader
- L3330: TI export path typically contains /exports/ and ends with index.html
- L3402: Remove TOC elements from page content
- L3413: Remove TOC/navigation elements from page content to prevent duplication.
- L3417: Remove TOC containers and navigation elements
- L3450: Wait for the nav tree to load completely
- L3456-3466: Scroll to make sure all content is loaded | (() => { const navTree = document.querySelector('#nav-tree-contents'); if (navTree) { ...
- L3475: Wait for final DOM stabilization
- L3480: Track expanded items for limit enforcement
- L3483: Expand systematically by clicking on arrows multiple times
- L3487: f ((limit, expandedCount) => {{ const root = document.querySelector('#nav-tree-contents'); if (!root) return {{clicks: 0, expanded: expandedCount}}...
- L3578: Stop if limit reached or no more clicks
- L3588: Wait for content to load after clicks
- L3598-3599: Final pass: force expand any remaining collapsed elements, except API Reference | Only if we haven't reached the limit
- L3684: (limit) => { const root = document.querySelector('#nav-tree-contents > ul'); if (!root) return {expanded: 0, count: 0, reached: false}; ...
- L3833: (() => { const el = document.querySelector('#nav-tree-contents ul'); if (!el) return ''; ...
- L4076: Track content by hash to consolidate duplicates
- L4090: Create content hash for deduplication
- L4095: Duplicate content - point to existing anchor
- L4099: New content - use this section's anchor
- L4253: Download assets from the touched pages
- L4360: Build unified doc with robust anchors and content deduplication
- L4380: Skip duplicate content
- L4433: Download assets from all pages
- L4452: Rewrite to local
- L4455: Remove stylesheet references and inline styles
- L4458: Output
- L4482-4483: ---------------------------- | Resource Explorer downloader
- L4622-4623: ---------------------------- | Main
- L4669-4674: Print the strict help block required by REQ-024. The function prints a fixed header and usage/exa... | Header
- L4678: Usage
- L4683: Example(s)
- L4688: Fixed core options block
- L4695-4697: Generate full list of options from parser._actions (avoid duplicates) | Collect actions in insertion order
- L4700: Skip the help/version that we've already printed
- L4706: show metavar for positional/optional arguments where appropriate
- L4711: Align to match typical formatting
- L4717: If executed with no parameters or with -h/--help, print strict help and exit 0

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`GITHUB_API_TIMEOUT_S`|var|pub|47||
|`_parse_version_tuple`|fn|priv|50-63|def _parse_version_tuple(v: str) -> Optional[Tuple[int, ....|
|`_is_version_newer`|fn|priv|64-74|def _is_version_newer(latest: str, current: str) -> bool|
|`_get_latest_version_from_github`|fn|priv|75-97|def _get_latest_version_from_github(owner: str, repo: str...|
|`check_for_new_version`|fn|pub|98-113|def check_for_new_version(program: str, current_version: ...|
|`safe_filename`|fn|pub|119-125|def safe_filename(path: str) -> str|
|`positive_int`|fn|pub|126-135|def positive_int(value: str) -> int|
|`is_http_url`|fn|pub|136-143|def is_http_url(s: str) -> bool|
|`normalize_url`|fn|pub|144-152|def normalize_url(u: str, base: str) -> str|
|`ensure_parent`|fn|pub|153-156|def ensure_parent(p: Path) -> None|
|`local_path_for_url`|fn|pub|157-175|def local_path_for_url(asset_url: str, out_dir: Path) -> ...|
|`download_one`|fn|pub|176-177|def download_one(|
|`escape_html`|fn|pub|192-201|def escape_html(s: str) -> str|
|`TocNode`|class|pub|203-208|class TocNode|
|`limit_toc_nodes`|fn|pub|209-229|def limit_toc_nodes(nodes: List[TocNode], max_entries: Op...|
|`trim_list`|fn|pub|216-226|def trim_list(items: List[TocNode]) -> List[TocNode]|
|`ensure_heading_ids`|fn|pub|230-248|def ensure_heading_ids(soup: BeautifulSoup) -> None|
|`strip_styles`|fn|pub|249-261|def strip_styles(soup: BeautifulSoup) -> None|
|`toc_from_headings`|fn|pub|262-283|def toc_from_headings(soup: BeautifulSoup) -> List[TocNode]|
|`toc_from_nav_html`|fn|pub|284-321|def toc_from_nav_html(toc_html: str, base_url: str) -> Li...|
|`parse_list`|fn|pub|287-310|def parse_list(list_el) -> List[TocNode]|
|`nav_outline_from_html`|fn|pub|322-361|def nav_outline_from_html(nav_html: str) -> str|
|`norm_text`|fn|pub|328-331|def norm_text(t: str) -> str|
|`bullet`|fn|pub|332-338|def bullet(depth: int) -> str|
|`walk_ul`|fn|pub|339-355|def walk_ul(ul, depth: int) -> None|
|`ASSET_ATTRS`|var|pub|362||
|`HEADING_TAG_RE`|var|pub|369||
|`Logger`|class|pub|372-394|class Logger|
|`Logger.__init__`|fn|priv|375-378|def __init__(self, verbose: bool = False, debug: bool = F...|
|`Logger.info`|fn|pub|379-381|def info(self, msg: str) -> None|
|`Logger.verbose`|fn|pub|382-385|def verbose(self, msg: str) -> None|
|`Logger.debug`|fn|pub|386-389|def debug(self, msg: str) -> None|
|`Logger.check`|fn|pub|390-394|def check(self, msg: str) -> None|
|`UpgradeAction`|class|pub|395-418|class UpgradeAction(argparse.Action)|
|`UpgradeAction.__call__`|fn|priv|396-401|def __call__(|
|`VersionedArgumentParser`|class|pub|419-443|class VersionedArgumentParser(argparse.ArgumentParser)|
|`VersionedArgumentParser.__init__`|fn|priv|426-429|def __init__(self, *args, version: str = "", **kwargs)|
|`VersionedArgumentParser.format_usage`|fn|pub|430-443|def format_usage(self) -> str|
|`iter_asset_urls`|fn|pub|444-475|def iter_asset_urls(soup: BeautifulSoup, page_url: str) -...|
|`rewrite_asset_links_inplace`|fn|pub|476-477|def rewrite_asset_links_inplace(|
|`to_rel`|fn|pub|479-485|def to_rel(u: str) -> str|
|`repl`|fn|pub|509-512|def repl(m)|
|`ALLOWED_EXTERNAL_LINK_SCHEMES`|var|pub|516||
|`normalize_document_links_inplace`|fn|pub|524-651|def normalize_document_links_inplace(soup: BeautifulSoup,...|
|`build_toc_html`|fn|pub|652-655|def build_toc_html(|
|`resolved_href`|fn|pub|657-665|def resolved_href(href: str) -> str|
|`render_nodes`|fn|pub|666-677|def render_nodes(nodes: List[TocNode]) -> str|
|`build_frameset_index`|fn|pub|699-700|def build_frameset_index(|
|`minimal_readable_wrapper`|fn|pub|722-723|def minimal_readable_wrapper(|
|`BaseDownloader`|class|pub|744-943|class BaseDownloader|
|`BaseDownloader.__init__`|fn|priv|747-755|def __init__(|
|`BaseDownloader.matches_url`|fn|pub|787-789|def matches_url(cls, url: str) -> bool|
|`BaseDownloader.probe_html`|fn|pub|791-793|def probe_html(cls, url: str, html: str) -> bool|
|`BaseDownloader.run`|fn|pub|794-796|def run(self) -> None|
|`BaseDownloader._toc_tree_from_html`|fn|priv|797-799|def _toc_tree_from_html(self, toc_html: str) -> List[TocN...|
|`BaseDownloader.post_process`|fn|pub|800-809|def post_process(self) -> None|
|`BaseDownloader._verify_toc_consistency`|fn|priv|810-857|def _verify_toc_consistency(self) -> None|
|`BaseDownloader._verify_toc_depth`|fn|priv|858-885|def _verify_toc_depth(self) -> None|
|`BaseDownloader.get_max_depth`|fn|pub|866-875|def get_max_depth(ul, current_depth=0)|
|`_prune_toc_and_clean_headings`|fn|priv|886-975|def _prune_toc_and_clean_headings(self) -> None|
|`BaseDownloader.href_fragment_id`|fn|pub|892-898|def href_fragment_id(href: str) -> str|
|`BaseDownloader.prune_ul`|fn|pub|910-923|def prune_ul(ul, depth)|
|`_deduplicate_toc_entries`|fn|priv|976-1034|def _deduplicate_toc_entries(self) -> None|
|`href_fragment_id`|fn|pub|992-998|def href_fragment_id(href: str) -> str|
|`process_nodes`|fn|pub|1005-1026|def process_nodes(nodes: List[TocNode], seen: Set[str]) -...|
|`_enforce_toc_headings`|fn|priv|1035-1137|def _enforce_toc_headings(self) -> None|
|`href_fragment_id`|fn|pub|1052-1058|def href_fragment_id(href: str) -> str|
|`clamp_heading_level`|fn|pub|1070-1080|def clamp_heading_level(depth: int) -> int|
|`find_referenced_container_id`|fn|pub|1081-1092|def find_referenced_container_id(h) -> str|
|`_test_toc_headings`|fn|priv|1138-1310|def _test_toc_headings(self) -> None|
|`href_fragment_id`|fn|pub|1149-1155|def href_fragment_id(href: str) -> str|
|`clamp_heading_level`|fn|pub|1156-1162|def clamp_heading_level(depth: int) -> int|
|`summarize`|fn|pub|1280-1287|def summarize(items: List[str]) -> str|
|`fix_heading_ref_position`|fn|pub|1311-1453|def fix_heading_ref_position(self) -> None|
|`fix_heading_numbering`|fn|pub|1454-1569|def fix_heading_numbering(self) -> None|
|`normalize_ws`|fn|pub|1475-1477|def normalize_ws(text: str) -> str|
|`strip_numbering_prefix`|fn|pub|1478-1480|def strip_numbering_prefix(text: str) -> str|
|`set_flat_text`|fn|pub|1481-1484|def set_flat_text(tag, text: str) -> None|
|`href_fragment_id`|fn|pub|1506-1512|def href_fragment_id(href: str) -> str|
|`_clean_document_style`|fn|priv|1570-1585|def _clean_document_style(self) -> None|
|`_add_document_style`|fn|priv|1586-1616|def _add_document_style(self) -> None|
|`_normalize_document_links`|fn|priv|1631-1645|def _normalize_document_links(self) -> None|
|`_remove_unused_images`|fn|priv|1646-1682|def _remove_unused_images(self) -> None|
|`_remove_unused_assets`|fn|priv|1683-1716|def _remove_unused_assets(self) -> None|
|`_normalize_image_position`|fn|priv|1717-1771|def _normalize_image_position(self) -> None|
|`_clean_assets_tree`|fn|priv|1772-1789|def _clean_assets_tree(self) -> None|
|`_remove_empty_assets_root`|fn|priv|1790-1829|def _remove_empty_assets_root(self) -> None|
|`DownloaderRegistry`|class|pub|1830-1862|class DownloaderRegistry|
|`DownloaderRegistry.__init__`|fn|priv|1831-1833|def __init__(self)|
|`DownloaderRegistry.register`|fn|pub|1834-1836|def register(self, downloader_cls: type[BaseDownloader]) ...|
|`DownloaderRegistry.detect`|fn|pub|1837-1862|def detect(self, url: str, session: requests.Session) -> ...|
|`guess_ext_from_content_type`|fn|pub|1868-1881|def guess_ext_from_content_type(ct: str) -> str|
|`NetworkImageRecorder`|class|pub|1882-1924|class NetworkImageRecorder|
|`NetworkImageRecorder.__init__`|fn|priv|1888-1892|def __init__(self, out_dir: Path)|
|`NetworkImageRecorder.attach`|fn|pub|1893-1924|def attach(self, page)|
|`NetworkImageRecorder.on_response`|fn|pub|1894-1921|def on_response(resp)|
|`DocumentViewerDownloader`|class|pub|1925-2124|class DocumentViewerDownloader(BaseDownloader)|
|`DocumentViewerDownloader.TOC_SELECTORS`|var|pub|1928||
|`DocumentViewerDownloader.CONTENT_SELECTORS`|var|pub|1937||
|`DocumentViewerDownloader.TOC_SCROLL_SELECTORS`|var|pub|1950||
|`DocumentViewerDownloader.matches_url`|fn|pub|1959-1962|def matches_url(cls, url: str) -> bool|
|`DocumentViewerDownloader.probe_html`|fn|pub|1964-1967|def probe_html(cls, url: str, html: str) -> bool|
|`DocumentViewerDownloader._pick_best_outerhtml`|fn|priv|1968-1991|def _pick_best_outerhtml(self, page, selectors: List[str]...|
|`DocumentViewerDownloader._expand_full_toc`|fn|priv|1992-1993|def _expand_full_toc(|
|`DocumentViewerDownloader._scroll_toc_container`|fn|priv|2044-2045|def _scroll_toc_container(|
|`_find_scroll_container`|fn|priv|2092-2150|def _find_scroll_container(self, page)|
|`_auto_scroll_element`|fn|priv|2151-2159|def _auto_scroll_element(|
|`_auto_scroll`|fn|priv|2219-2225|def _auto_scroll(|
|`_collect_cards_from_container`|fn|priv|2284-2291|def _collect_cards_from_container(|
|`_best_card_for_fragment`|fn|priv|2357-2358|def _best_card_for_fragment(|
|`score_value`|fn|pub|2369-2383|def score_value(val: str) -> int|
|`_fragment_matches_url`|fn|priv|2400-2411|def _fragment_matches_url(self, fragment: str, data_url: ...|
|`_toc_tree_from_html`|fn|priv|2412-2414|def _toc_tree_from_html(self, toc_html: str) -> List[TocN...|
|`_iter_nodes`|fn|priv|2416-2420|def _iter_nodes(nodes: List[TocNode]) -> Iterable[TocNode]|
|`_first_numeric_index`|fn|priv|2422-2428|def _first_numeric_index(nodes: List[TocNode]) -> Optiona...|
|`_trim_toc_nodes`|fn|priv|2430-2446|def _trim_toc_nodes(nodes: List[TocNode]) -> List[TocNode]|
|`_limit_toc_nodes`|fn|priv|2448-2449|def _limit_toc_nodes(|
|`_limit_by_reading_order`|fn|priv|2454-2455|def _limit_by_reading_order(|
|`_prune_toc_to_allowed`|fn|priv|2487-2488|def _prune_toc_to_allowed(|
|`_first_toc_entry_title`|fn|priv|2505-2511|def _first_toc_entry_title(nodes: List[TocNode]) -> Optio...|
|`_is_important_notice_label`|fn|priv|2513-2516|def _is_important_notice_label(title: Optional[str]) -> bool|
|`_is_important_notice_section`|fn|priv|2518-2527|def _is_important_notice_section(section_html: str) -> bool|
|`_select_section_nodes`|fn|priv|2529-2553|def _select_section_nodes(nodes: List[TocNode]) -> List[T...|
|`_dedup_toc_nodes_by_href`|fn|priv|2554-2580|def _dedup_toc_nodes_by_href(self, nodes: List[TocNode]) ...|
|`dedup_list`|fn|pub|2557-2578|def dedup_list(items: List[TocNode]) -> List[TocNode]|
|`_is_section_scrollable`|fn|priv|2581-2600|def _is_section_scrollable(self, page, viewport_multiplie...|
|`_remove_toc_elements`|fn|priv|2601-2634|def _remove_toc_elements(self, soup: BeautifulSoup) -> None|
|`_convert_doxygen_definition_lists`|fn|priv|2635-2706|def _convert_doxygen_definition_lists(self, soup: Beautif...|
|`_extract_fragment_only`|fn|priv|2707-2708|def _extract_fragment_only(|
|`score_value`|fn|pub|2720-2737|def score_value(val: str) -> int|
|`pick_best_section`|fn|pub|2738-2755|def pick_best_section(elements)|
|`matches_fragment`|fn|pub|2766-2779|def matches_fragment(el) -> bool|
|`_wait_for_fragment`|fn|priv|2807-2850|def _wait_for_fragment(self, page, fragment: str, timeout...|
|`_click_toc_link`|fn|priv|2851-2871|def _click_toc_link(self, page, fragment: str) -> bool|
|`run`|fn|pub|2872-3071|def run(self) -> None|
|`make_anchor`|fn|pub|2876-2886|def make_anchor(raw_fragment: str, title: str, used: Set[...|
|`normalize_text`|fn|pub|2887-2891|def normalize_text(value: str) -> str|
|`strip_ti_disclaimer`|fn|pub|2892-2916|def strip_ti_disclaimer(section_html: str) -> str|
|`DoxygenExportDownloader`|class|pub|3324-3523|class DoxygenExportDownloader(BaseDownloader)|
|`DoxygenExportDownloader.matches_url`|fn|pub|3328-3334|def matches_url(cls, url: str) -> bool|
|`DoxygenExportDownloader.probe_html`|fn|pub|3336-3339|def probe_html(cls, url: str, html: str) -> bool|
|`DoxygenExportDownloader._scope`|fn|priv|3340-3347|def _scope(self) -> Tuple[str, str]|
|`DoxygenExportDownloader._fetch_soup`|fn|priv|3348-3352|def _fetch_soup(self, url: str) -> BeautifulSoup|
|`DoxygenExportDownloader._is_in_scope`|fn|priv|3353-3360|def _is_in_scope(self, url: str, host: str, scope_dir_url...|
|`DoxygenExportDownloader._page_title`|fn|priv|3361-3369|def _page_title(self, soup: BeautifulSoup) -> str|
|`DoxygenExportDownloader._document_title`|fn|priv|3370-3394|def _document_title(self, soup: BeautifulSoup) -> str|
|`DoxygenExportDownloader._extract_main`|fn|priv|3395-3411|def _extract_main(self, soup: BeautifulSoup) -> Beautiful...|
|`DoxygenExportDownloader._remove_toc_elements`|fn|priv|3412-3432|def _remove_toc_elements(self, soup: BeautifulSoup) -> None|
|`DoxygenExportDownloader._links_to_html_pages`|fn|priv|3433-3434|def _links_to_html_pages(|
|`DoxygenExportDownloader._expand_nav_tree`|fn|priv|3449-3478|def _expand_nav_tree(self, page) -> None|
|`_expand_nav_tree_full`|fn|priv|3479-3678|def _expand_nav_tree_full(self, page) -> None|
|`_expand_nav_tree_limited`|fn|priv|3679-3780|def _expand_nav_tree_limited(self, page, limit: int) -> None|
|`_cleanup_nav_tree_styles`|fn|priv|3781-3805|def _cleanup_nav_tree_styles(self, page) -> None|
|`_fetch_nav_tree_with_playwright`|fn|priv|3806-3889|def _fetch_nav_tree_with_playwright(self) -> Tuple[str, str]|
|`_nav_link_href`|fn|priv|3890-3907|def _nav_link_href(self, link, base_url: str) -> str|
|`_toc_tree_from_html`|fn|priv|3908-3910|def _toc_tree_from_html(self, toc_html: str) -> List[TocN...|
|`_toc_nodes_from_nav_html`|fn|priv|3911-3940|def _toc_nodes_from_nav_html(self, nav_html: str) -> List...|
|`parse_ul`|fn|pub|3917-3935|def parse_ul(ul) -> List[TocNode]|
|`_iter_toc_nodes`|fn|priv|3942-3946|def _iter_toc_nodes(nodes: List[TocNode]) -> Iterable[Toc...|
|`_select_main_container`|fn|priv|3947-3961|def _select_main_container(self, soup: BeautifulSoup)|
|`_find_fragment_anchor`|fn|priv|3962-3981|def _find_fragment_anchor(self, main, fragment: str)|
|`_normalize_heading_text`|fn|priv|3983-3985|def _normalize_heading_text(value: str) -> str|
|`_strip_duplicate_section_title`|fn|priv|3986-3987|def _strip_duplicate_section_title(|
|`_extract_section_html`|fn|priv|4021-4022|def _extract_section_html(|
|`direct_child`|fn|pub|4041-4046|def direct_child(el)|
|`_build_toc`|fn|priv|4070-4128|def _build_toc(self, doc: BeautifulSoup) -> List[TocNode]|
|`run`|fn|pub|4129-4328|def run(self) -> None|
|`MAX_PAGES`|var|pub|4309||
|`ResourceExplorerModule`|class|pub|4487-4498|class ResourceExplorerModule|
|`ResourceExplorerModule.select`|fn|pub|4490-4491|def select(|
|`ResourceExplorerModule.run`|fn|pub|4495-4498|def run(self, downloader: "ResourceExplorerDownloader", s...|
|`RMModuleDoxigen`|class|pub|4499-4535|class RMModuleDoxigen(ResourceExplorerModule)|
|`RMModuleDoxigen.select`|fn|pub|4504-4505|def select(|
|`RMModuleDoxigen.run`|fn|pub|4520-4535|def run(self, downloader: "ResourceExplorerDownloader", s...|
|`ResourceExplorerDownloader`|class|pub|4536-4621|class ResourceExplorerDownloader(BaseDownloader)|
|`ResourceExplorerDownloader.__init__`|fn|priv|4539-4542|def __init__(self, *args, **kwargs)|
|`ResourceExplorerDownloader.matches_url`|fn|pub|4544-4547|def matches_url(cls, url: str) -> bool|
|`ResourceExplorerDownloader.probe_html`|fn|pub|4549-4551|def probe_html(cls, url: str, html: str) -> bool|
|`ResourceExplorerDownloader._select_module`|fn|priv|4552-4553|def _select_module(|
|`ResourceExplorerDownloader._render_with_playwright`|fn|priv|4561-4592|def _render_with_playwright(self) -> str|
|`ResourceExplorerDownloader.run`|fn|pub|4593-4621|def run(self) -> None|
|`build_arg_parser`|fn|pub|4627-4667|def build_arg_parser() -> argparse.ArgumentParser|
|`print_strict_help`|fn|pub|4668-4714|def print_strict_help(program: str, version: str, parser:...|
|`main`|fn|pub|4715-4761|def main() -> int|


---

# version.py | Python | 9L | 0 symbols | 0 imports | 1 comments
> Path: `/home/ogekuri/HtmlDownloader/src/htmldownloader/version.py`
> Version metadata for HtmlDownloader. Keep this module lightweight so it can be imported without pulling heavy runtime dependencies.

