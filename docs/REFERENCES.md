# Files Structure
```
.
└── src
    └── htmldownloader
        ├── __init__.py
        ├── __main__.py
        ├── cli.py
        └── version.py
```

# __init__.py | Python | 14L | 0 symbols | 2 imports | 2 comments
> Path: `src/htmldownloader/__init__.py`
- Brief: HtmlDownloader package entry module.
- Details: Exposes package-level symbols used by CLI entrypoints and version reporting.
@module_symbols functions=0 classes=0 variables=1
@variables __all__

## Imports
```
from .version import __version__
from .cli import main
```


---

# __main__.py | Python | 12L | 0 symbols | 2 imports | 1 comments
> Path: `src/htmldownloader/__main__.py`
- Brief: HtmlDownloader package entry module.
- Details: Exposes package-level symbols used by CLI entrypoints and version reporting.
@module_symbols functions=0 classes=0 variables=0

## Imports
```
from .cli import main
import sys
```


---

# cli.py | Python | 5813L | 184 symbols | 20 imports | 338 comments
> Path: `src/htmldownloader/cli.py`
- Brief: Module implementation for HtmlDownloader runtime.
- Details: Contains executable logic and internal helpers used by the CLI workflow.
@module_symbols functions=28 classes=12 variables=4
@functions _parse_version_tuple, _is_version_newer, _get_latest_version_from_github, check_for_new_version, safe_filename, positive_int, is_http_url, normalize_url, ensure_parent, local_path_for_url, download_one, escape_html, limit_toc_nodes, ensure_heading_ids, strip_styles, toc_from_headings, toc_from_nav_html, nav_outline_from_html, iter_asset_urls, rewrite_asset_links_inplace, normalize_document_links_inplace, build_toc_html, build_frameset_index, minimal_readable_wrapper, guess_ext_from_content_type, build_arg_parser, print_strict_help, main
@classes TocNode, Logger, UpgradeAction, VersionedArgumentParser, BaseDownloader, DownloaderRegistry, NetworkImageRecorder, DocumentViewerDownloader, DoxygenExportDownloader, ResourceExplorerModule, RMModuleDoxigen, ResourceExplorerDownloader
@variables GITHUB_API_TIMEOUT_S, ASSET_ATTRS, HEADING_TAG_RE, ALLOWED_EXTERNAL_LINK_SCHEMES

## Imports
```
from __future__ import annotations
import argparse
import mimetypes
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, urldefrag, unquote
import requests
from bs4 import BeautifulSoup  # pyright: ignore[reportMissingImports]
from tqdm import tqdm  # pyright: ignore[reportMissingModuleSource]
import uuid
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError  # pyright: ignore[reportMissingImports]
from .version import __version__
import re
import re
from bs4 import NavigableString  # pyright: ignore[reportMissingImports]
```

## Definitions

- var `GITHUB_API_TIMEOUT_S = 1` (L36)
- Brief: Module-level variable `GITHUB_API_TIMEOUT_S`.
### fn `def _parse_version_tuple(v: str) -> Optional[Tuple[int, ...]]` `priv` (L39-58)
- Brief: Execute `_parse_version_tuple`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: v Input argument for `_parse_version_tuple`.
- Return: Optional[Tuple[int, ...]] Return value of `_parse_version_tuple`.

### fn `def _is_version_newer(latest: str, current: str) -> bool` `priv` (L59-76)
- Brief: Execute `_is_version_newer`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: latest Input argument for `_is_version_newer`.
- Param: current Input argument for `_is_version_newer`.
- Return: bool Return value of `_is_version_newer`.

### fn `def _get_latest_version_from_github(owner: str, repo: str) -> Optional[str]` `priv` (L77-106)
- Brief: Execute `_get_latest_version_from_github`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: owner Input argument for `_get_latest_version_from_github`.
- Param: repo Input argument for `_get_latest_version_from_github`.
- Return: Optional[str] Return value of `_get_latest_version_from_github`.

### fn `def check_for_new_version(program: str, current_version: str) -> None` (L107-125)
- Brief: Execute `check_for_new_version`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: program Input argument for `check_for_new_version`.
- Param: current_version Input argument for `check_for_new_version`.
- Return: None Return value of `check_for_new_version`.

### fn `def safe_filename(path: str) -> str` (L131-143)
- Brief: Execute `safe_filename`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: path Input argument for `safe_filename`.
- Return: str Return value of `safe_filename`.

### fn `def positive_int(value: str) -> int` (L144-159)
- Brief: Execute `positive_int`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: value Input argument for `positive_int`.
- Return: int Return value of `positive_int`.

### fn `def is_http_url(s: str) -> bool` (L160-173)
- Brief: Execute `is_http_url`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: s Input argument for `is_http_url`.
- Return: bool Return value of `is_http_url`.

### fn `def normalize_url(u: str, base: str) -> str` (L174-189)
- Brief: Execute `normalize_url`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: u Input argument for `normalize_url`.
- Param: base Input argument for `normalize_url`.
- Return: str Return value of `normalize_url`.

### fn `def ensure_parent(p: Path) -> None` (L190-199)
- Brief: Execute `ensure_parent`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: p Input argument for `ensure_parent`.
- Return: None Return value of `ensure_parent`.

### fn `def local_path_for_url(asset_url: str, out_dir: Path) -> Path` (L200-222)
- Brief: Execute `local_path_for_url`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: asset_url Input argument for `local_path_for_url`.
- Param: out_dir Input argument for `local_path_for_url`.
- Return: Path Return value of `local_path_for_url`.

### fn `def download_one(` (L223-224)

### fn `def escape_html(s: str) -> str` (L248-263)
- Brief: Execute `download_one`.
- Brief: Execute `escape_html`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: session Input argument for `download_one`.
- Param: url Input argument for `download_one`.
- Param: dest Input argument for `download_one`.
- Param: timeout Input argument for `download_one`.
- Param: s Input argument for `escape_html`.
- Return: bool Return value of `download_one`.
- Return: str Return value of `escape_html`.

### class `class TocNode` `@dataclass` (L265-274)
- Brief: Define class `TocNode`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.

### fn `def limit_toc_nodes(nodes: List[TocNode], max_entries: Optional[int]) -> List[TocNode]` (L275-307)
- Brief: Execute `limit_toc_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `limit_toc_nodes`.
- Param: max_entries Input argument for `limit_toc_nodes`.
- Return: List[TocNode] Return value of `limit_toc_nodes`.

### fn `def trim_list(items: List[TocNode]) -> List[TocNode]` (L288-304)
- Brief: Execute `limit_toc_nodes`.
- Brief: Execute `trim_list`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `limit_toc_nodes`.
- Param: max_entries Input argument for `limit_toc_nodes`.
- Param: items Input argument for `trim_list`.
- Return: List[TocNode] Return value of `limit_toc_nodes`.
- Return: List[TocNode] Return value of `trim_list`.

### fn `def ensure_heading_ids(soup: BeautifulSoup) -> None` (L308-332)
- Brief: Execute `ensure_heading_ids`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `ensure_heading_ids`.
- Return: None Return value of `ensure_heading_ids`.

### fn `def strip_styles(soup: BeautifulSoup) -> None` (L333-350)
- Brief: Execute `strip_styles`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `strip_styles`.
- Return: None Return value of `strip_styles`.

### fn `def toc_from_headings(soup: BeautifulSoup) -> List[TocNode]` (L351-378)
- Brief: Execute `toc_from_headings`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `toc_from_headings`.
- Return: List[TocNode] Return value of `toc_from_headings`.

### fn `def toc_from_nav_html(toc_html: str, base_url: str) -> List[TocNode]` (L379-429)
- Brief: Execute `toc_from_nav_html`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: toc_html Input argument for `toc_from_nav_html`.
- Param: base_url Input argument for `toc_from_nav_html`.
- Return: List[TocNode] Return value of `toc_from_nav_html`.

### fn `def parse_list(list_el) -> List[TocNode]` (L389-418)
- Brief: Execute `toc_from_nav_html`.
- Brief: Execute `parse_list`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: toc_html Input argument for `toc_from_nav_html`.
- Param: base_url Input argument for `toc_from_nav_html`.
- Param: list_el Input argument for `parse_list`.
- Return: List[TocNode] Return value of `toc_from_nav_html`.
- Return: List[TocNode] Return value of `parse_list`.

### fn `def nav_outline_from_html(nav_html: str) -> str` (L430-493)
- Brief: Execute `nav_outline_from_html`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nav_html Input argument for `nav_outline_from_html`.
- Return: str Return value of `nav_outline_from_html`.

### fn `def norm_text(t: str) -> str` (L441-450)
- Brief: Execute `nav_outline_from_html`.
- Brief: Execute `norm_text`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nav_html Input argument for `nav_outline_from_html`.
- Param: t Input argument for `norm_text`.
- Return: str Return value of `nav_outline_from_html`.
- Return: str Return value of `norm_text`.

### fn `def bullet(depth: int) -> str` (L451-463)
- Brief: Execute `bullet`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: depth Input argument for `bullet`.
- Return: str Return value of `bullet`.

### fn `def walk_ul(ul, depth: int) -> None` (L464-487)
- Brief: Execute `walk_ul`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: ul Input argument for `walk_ul`.
- Param: depth Input argument for `walk_ul`.
- Return: None Return value of `walk_ul`.

- var `ASSET_ATTRS = [` (L495)
- Brief: Module-level variable `ASSET_ATTRS`.
- var `HEADING_TAG_RE = re.compile(r"^h[1-6]$")` (L503)
- Brief: Module-level variable `HEADING_TAG_RE`.
### class `class Logger` (L506-567)
- Brief: Define class `Logger`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def __init__(self, verbose: bool = False, debug: bool = False)` `priv` (L512-523)
  - Brief: Define class `Logger`.
  - Brief: Execute `__init__`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`.
  - Param: verbose Input argument for `__init__`.
  - Param: debug Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def info(self, msg: str) -> None` (L524-533)
  - Brief: Execute `info`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `info`.
  - Param: msg Input argument for `info`.
  - Return: None Return value of `info`.
- fn `def verbose(self, msg: str) -> None` (L534-544)
  - Brief: Execute `verbose`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `verbose`.
  - Param: msg Input argument for `verbose`.
  - Return: None Return value of `verbose`.
- fn `def debug(self, msg: str) -> None` (L545-555)
  - Brief: Execute `debug`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `debug`.
  - Param: msg Input argument for `debug`.
  - Return: None Return value of `debug`.
- fn `def check(self, msg: str) -> None` (L556-567)
  - Brief: Execute `check`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `check`.
  - Param: msg Input argument for `check`.
  - Return: None Return value of `check`.

### class `class UpgradeAction(argparse.Action)` : argparse.Action (L568-605)
- Brief: Define class `UpgradeAction`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def __call__(` `priv` (L573-578)
  - Brief: Define class `UpgradeAction`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.

### class `class VersionedArgumentParser(argparse.ArgumentParser)` : argparse.ArgumentParser (L606-644)
- Brief: Define class `VersionedArgumentParser`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def __init__(self, *args, version: str = "", **kwargs)` `priv` (L612-624)
  - Brief: Define class `VersionedArgumentParser`.
  - Brief: Execute `__init__`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`.
  - Param: version Input argument for `__init__`.
  - Param: *args Input argument for `__init__`.
  - Param: **kwargs Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def format_usage(self) -> str` (L625-644)
  - Brief: Execute `format_usage`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `format_usage`.
  - Return: str Return value of `format_usage`.

### fn `def iter_asset_urls(soup: BeautifulSoup, page_url: str) -> Set[str]` (L645-683)
- Brief: Execute `iter_asset_urls`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `iter_asset_urls`.
- Param: page_url Input argument for `iter_asset_urls`.
- Return: Set[str] Return value of `iter_asset_urls`.

### fn `def rewrite_asset_links_inplace(` (L684-685)

### fn `def to_rel(u: str) -> str` (L695-707)
- Brief: Execute `rewrite_asset_links_inplace`.
- Brief: Execute `to_rel`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `rewrite_asset_links_inplace`.
- Param: base_url Input argument for `rewrite_asset_links_inplace`.
- Param: out_dir Input argument for `rewrite_asset_links_inplace`.
- Param: u Input argument for `to_rel`.
- Return: None Return value of `rewrite_asset_links_inplace`.
- Return: str Return value of `to_rel`.

### fn `def repl(m)` (L731-740)
- Brief: Execute `repl`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: m Input argument for `repl`.
- Return: Any Return value of `repl`.

- var `ALLOWED_EXTERNAL_LINK_SCHEMES = {` (L745)
- Brief: Module-level variable `ALLOWED_EXTERNAL_LINK_SCHEMES`.
### fn `def normalize_document_links_inplace(soup: BeautifulSoup, logger: Optional[Logger]) -> None` (L753-878)
- Brief: Execute `normalize_document_links_inplace`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `normalize_document_links_inplace`.
- Param: logger Input argument for `normalize_document_links_inplace`.
- Return: None Return value of `normalize_document_links_inplace`.

### fn `def build_toc_html(` (L879-882)

### fn `def resolved_href(href: str) -> str` (L892-906)
- Brief: Execute `build_toc_html`.
- Brief: Execute `resolved_href`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: toc_items Input argument for `build_toc_html`.
- Param: document_filename Input argument for `build_toc_html`.
- Param: target_frame Input argument for `build_toc_html`.
- Param: href Input argument for `resolved_href`.
- Return: str Return value of `build_toc_html`.
- Return: str Return value of `resolved_href`.

### fn `def render_nodes(nodes: List[TocNode], indent_level: int = 0) -> str` (L907-935)
- Brief: Execute `render_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `render_nodes`.
- Param: indent_level Input argument for `render_nodes`.
- Return: str Return value of `render_nodes`.

### fn `def build_frameset_index(` (L957-958)

### fn `def minimal_readable_wrapper(` (L987-988)
- Brief: Execute `build_frameset_index`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: toc_filename Input argument for `build_frameset_index`.
- Param: document_filename Input argument for `build_frameset_index`.
- Return: str Return value of `build_frameset_index`.

### class `class BaseDownloader` (L1016-1215)
- Brief: Execute `minimal_readable_wrapper`.
- Brief: Define class `BaseDownloader`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- Param: inner_html Input argument for `minimal_readable_wrapper`.
- Param: title Input argument for `minimal_readable_wrapper`.
- Return: str Return value of `minimal_readable_wrapper`.
- fn `def __init__(` `priv` (L1023-1031)
  - Brief: Define class `BaseDownloader`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def matches_url(cls, url: str) -> bool` (L1076-1085)
  - Brief: Execute `matches_url`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `matches_url`.
  - Param: url Input argument for `matches_url`.
  - Return: bool Return value of `matches_url`.
- fn `def probe_html(cls, url: str, html: str) -> bool` (L1087-1097)
  - Brief: Execute `probe_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `probe_html`.
  - Param: url Input argument for `probe_html`.
  - Param: html Input argument for `probe_html`.
  - Return: bool Return value of `probe_html`.
- fn `def run(self) -> None` (L1098-1106)
  - Brief: Execute `run`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `run`.
  - Return: None Return value of `run`.
- fn `def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]` `priv` (L1107-1116)
  - Brief: Execute `_toc_tree_from_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_toc_tree_from_html`.
  - Param: toc_html Input argument for `_toc_tree_from_html`.
  - Return: List[TocNode] Return value of `_toc_tree_from_html`.
- fn `def post_process(self) -> None` (L1117-1131)
  - Brief: Execute `post_process`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `post_process`.
  - Return: None Return value of `post_process`.
- fn `def _verify_toc_consistency(self) -> None` `priv` (L1132-1183)
  - Brief: Execute `_verify_toc_consistency`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_verify_toc_consistency`.
  - Return: None Return value of `_verify_toc_consistency`.
- fn `def get_max_depth(ul, current_depth=0)` (L1197-1213)
  - Brief: Execute `_verify_toc_depth`.
  - Brief: Execute `get_max_depth`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_verify_toc_depth`.
  - Param: ul Input argument for `get_max_depth`.
  - Param: current_depth Input argument for `get_max_depth`.
  - Return: None Return value of `_verify_toc_depth`.
  - Return: Any Return value of `get_max_depth`.

### fn `def _verify_toc_depth(self) -> None` `priv` (L1184-1223)
- Brief: Execute `_verify_toc_depth`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_verify_toc_depth`.
- Return: None Return value of `_verify_toc_depth`.

### fn `def _prune_toc_and_clean_headings(self) -> None` `priv` (L1224-1325)
- Brief: Execute `_prune_toc_and_clean_headings`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_prune_toc_and_clean_headings`.
- Return: None Return value of `_prune_toc_and_clean_headings`.

### fn `def href_fragment_id(href: str) -> str` (L1235-1247)
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: href Input argument for `href_fragment_id`.
- Return: str Return value of `href_fragment_id`.

### fn `def prune_ul(ul, depth)` (L1258-1278)
- Brief: Execute `prune_ul`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: ul Input argument for `prune_ul`.
- Param: depth Input argument for `prune_ul`.
- Return: Any Return value of `prune_ul`.

### fn `def _deduplicate_toc_entries(self) -> None` `priv` (L1326-1394)
- Brief: Execute `_deduplicate_toc_entries`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_deduplicate_toc_entries`.
- Return: None Return value of `_deduplicate_toc_entries`.

### fn `def href_fragment_id(href: str) -> str` (L1339-1351)
- Brief: Execute `_deduplicate_toc_entries`.
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_deduplicate_toc_entries`.
- Param: href Input argument for `href_fragment_id`.
- Return: None Return value of `_deduplicate_toc_entries`.
- Return: str Return value of `href_fragment_id`.

### fn `def process_nodes(nodes: List[TocNode], seen: Set[str]) -> List[TocNode]` (L1358-1386)
- Brief: Execute `process_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `process_nodes`.
- Param: seen Input argument for `process_nodes`.
- Return: List[TocNode] Return value of `process_nodes`.

### fn `def _enforce_toc_headings(self) -> None` `priv` (L1395-1513)
- Brief: Execute `_enforce_toc_headings`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_enforce_toc_headings`.
- Return: None Return value of `_enforce_toc_headings`.

### fn `def href_fragment_id(href: str) -> str` (L1410-1422)
- Brief: Execute `_enforce_toc_headings`.
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_enforce_toc_headings`.
- Param: href Input argument for `href_fragment_id`.
- Return: None Return value of `_enforce_toc_headings`.
- Return: str Return value of `href_fragment_id`.

### fn `def clamp_heading_level(depth: int) -> int` (L1434-1450)
- Brief: Execute `clamp_heading_level`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: depth Input argument for `clamp_heading_level`.
- Return: int Return value of `clamp_heading_level`.

### fn `def find_referenced_container_id(h) -> str` (L1451-1468)
- Brief: Execute `find_referenced_container_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: h Input argument for `find_referenced_container_id`.
- Return: str Return value of `find_referenced_container_id`.

### fn `def _test_toc_headings(self) -> None` `priv` (L1514-1709)
- Brief: Execute `_test_toc_headings`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_test_toc_headings`.
- Return: None Return value of `_test_toc_headings`.

### fn `def href_fragment_id(href: str) -> str` (L1530-1542)
- Brief: Execute `_test_toc_headings`.
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_test_toc_headings`.
- Param: href Input argument for `href_fragment_id`.
- Return: None Return value of `_test_toc_headings`.
- Return: str Return value of `href_fragment_id`.

### fn `def clamp_heading_level(depth: int) -> int` (L1543-1555)
- Brief: Execute `clamp_heading_level`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: depth Input argument for `clamp_heading_level`.
- Return: int Return value of `clamp_heading_level`.

### fn `def summarize(items: List[str]) -> str` (L1673-1686)
- Brief: Execute `summarize`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: items Input argument for `summarize`.
- Return: str Return value of `summarize`.

### fn `def fix_heading_ref_position(self) -> None` (L1710-1850)
- Brief: Execute `fix_heading_ref_position`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `fix_heading_ref_position`.
- Return: None Return value of `fix_heading_ref_position`.

### fn `def fix_heading_numbering(self) -> None` (L1851-1989)
- Brief: Execute `fix_heading_numbering`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `fix_heading_numbering`.
- Return: None Return value of `fix_heading_numbering`.

### fn `def normalize_ws(text: str) -> str` (L1870-1878)
- Brief: Execute `normalize_ws`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: text Input argument for `normalize_ws`.
- Return: str Return value of `normalize_ws`.

### fn `def strip_numbering_prefix(text: str) -> str` (L1879-1887)
- Brief: Execute `strip_numbering_prefix`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: text Input argument for `strip_numbering_prefix`.
- Return: str Return value of `strip_numbering_prefix`.

### fn `def set_flat_text(tag, text: str) -> None` (L1888-1898)
- Brief: Execute `set_flat_text`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: tag Input argument for `set_flat_text`.
- Param: text Input argument for `set_flat_text`.
- Return: None Return value of `set_flat_text`.

### fn `def href_fragment_id(href: str) -> str` (L1920-1932)
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: href Input argument for `href_fragment_id`.
- Return: str Return value of `href_fragment_id`.

### fn `def _clean_document_style(self) -> None` `priv` (L1990-2010)
- Brief: Execute `_clean_document_style`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_clean_document_style`.
- Return: None Return value of `_clean_document_style`.

### fn `def _add_document_style(self) -> None` `priv` (L2011-2042)
- Brief: Execute `_add_document_style`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_add_document_style`.
- Return: None Return value of `_add_document_style`.

### fn `def _normalize_document_links(self) -> None` `priv` (L2057-2071)
- Brief: Execute `_normalize_document_links`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_normalize_document_links`.
- Return: None Return value of `_normalize_document_links`.

### fn `def _remove_unused_images(self) -> None` `priv` (L2072-2113)
- Brief: Execute `_remove_unused_images`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_remove_unused_images`.
- Return: None Return value of `_remove_unused_images`.

### fn `def _remove_unused_assets(self) -> None` `priv` (L2114-2148)
- Brief: Execute `_remove_unused_assets`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_remove_unused_assets`.
- Return: None Return value of `_remove_unused_assets`.

### fn `def _normalize_image_position(self) -> None` `priv` (L2149-2208)
- Brief: Execute `_normalize_image_position`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_normalize_image_position`.
- Return: None Return value of `_normalize_image_position`.

### fn `def _clean_assets_tree(self) -> None` `priv` (L2209-2231)
- Brief: Execute `_clean_assets_tree`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_clean_assets_tree`.
- Return: None Return value of `_clean_assets_tree`.

### fn `def _remove_empty_assets_root(self) -> None` `priv` (L2232-2270)
- Brief: Execute `_remove_empty_assets_root`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_remove_empty_assets_root`.
- Return: None Return value of `_remove_empty_assets_root`.

### class `class DownloaderRegistry` (L2271-2328)
- Brief: Define class `DownloaderRegistry`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def __init__(self)` `priv` (L2276-2284)
  - Brief: Define class `DownloaderRegistry`.
  - Brief: Execute `__init__`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def register(self, downloader_cls: type[BaseDownloader]) -> None` (L2285-2294)
  - Brief: Execute `register`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `register`.
  - Param: downloader_cls Input argument for `register`.
  - Return: None Return value of `register`.
- fn `def detect(self, url: str, session: requests.Session) -> type[BaseDownloader]` (L2295-2328)
  - Brief: Execute `detect`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `detect`.
  - Param: url Input argument for `detect`.
  - Param: session Input argument for `detect`.
  - Return: type[BaseDownloader] Return value of `detect`.

### fn `def guess_ext_from_content_type(ct: str) -> str` (L2334-2353)
- Brief: Execute `guess_ext_from_content_type`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: ct Input argument for `guess_ext_from_content_type`.
- Return: str Return value of `guess_ext_from_content_type`.

### class `class NetworkImageRecorder` (L2354-2416)
- Brief: Define class `NetworkImageRecorder`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def __init__(self, out_dir: Path)` `priv` (L2360-2371)
  - Brief: Define class `NetworkImageRecorder`.
  - Brief: Execute `__init__`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`.
  - Param: out_dir Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def attach(self, page)` (L2372-2416)
  - Brief: Execute `attach`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `attach`.
  - Param: page Input argument for `attach`.
  - Return: Any Return value of `attach`.
- fn `def on_response(resp)` (L2380-2413)
  - Brief: Execute `attach`.
  - Brief: Execute `on_response`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `attach`.
  - Param: page Input argument for `attach`.
  - Param: resp Input argument for `on_response`.
  - Return: Any Return value of `attach`.
  - Return: Any Return value of `on_response`.

### class `class DocumentViewerDownloader(BaseDownloader)` : BaseDownloader (L2417-2616)
- Brief: Define class `DocumentViewerDownloader`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- var `TOC_SELECTORS = [` (L2424)
  - Brief: Define class `DocumentViewerDownloader`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- var `CONTENT_SELECTORS = [` (L2433)
- var `TOC_SCROLL_SELECTORS = [` (L2446)
- fn `def matches_url(cls, url: str) -> bool` (L2455-2465)
  - Brief: Execute `matches_url`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `matches_url`.
  - Param: url Input argument for `matches_url`.
  - Return: bool Return value of `matches_url`.
- fn `def probe_html(cls, url: str, html: str) -> bool` (L2467-2478)
  - Brief: Execute `probe_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `probe_html`.
  - Param: url Input argument for `probe_html`.
  - Param: html Input argument for `probe_html`.
  - Return: bool Return value of `probe_html`.
- fn `def _pick_best_outerhtml(self, page, selectors: List[str]) -> Optional[str]` `priv` (L2479-2510)
  - Brief: Execute `_pick_best_outerhtml`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_pick_best_outerhtml`.
  - Param: page Input argument for `_pick_best_outerhtml`.
  - Param: selectors Input argument for `_pick_best_outerhtml`.
  - Return: Optional[str] Return value of `_pick_best_outerhtml`.
- fn `def _expand_full_toc(` `priv` (L2511-2512)
- fn `def _scroll_toc_container(` `priv` (L2572-2573)
  - Brief: Execute `_expand_full_toc`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_expand_full_toc`.
  - Param: page Input argument for `_expand_full_toc`.
  - Param: max_rounds Input argument for `_expand_full_toc`.
  - Param: settle_ms Input argument for `_expand_full_toc`.
  - Return: None Return value of `_expand_full_toc`.

### fn `def _find_scroll_container(self, page)` `priv` (L2630-2695)
- Brief: Execute `_find_scroll_container`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_find_scroll_container`.
- Param: page Input argument for `_find_scroll_container`.
- Return: Any Return value of `_find_scroll_container`.

### fn `def _auto_scroll_element(` `priv` (L2696-2704)

### fn `def _auto_scroll(` `priv` (L2777-2783)
- Brief: Execute `_auto_scroll_element`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_auto_scroll_element`.
- Param: page Input argument for `_auto_scroll_element`.
- Param: element Input argument for `_auto_scroll_element`.
- Param: settle_ms Input argument for `_auto_scroll_element`.
- Param: step_px Input argument for `_auto_scroll_element`.
- Param: max_rounds Input argument for `_auto_scroll_element`.
- Param: stable_rounds Input argument for `_auto_scroll_element`.
- Param: label Input argument for `_auto_scroll_element`.
- Return: bool Return value of `_auto_scroll_element`.

### fn `def _collect_cards_from_container(` `priv` (L2853-2860)
- Brief: Execute `_auto_scroll`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_auto_scroll`.
- Param: page Input argument for `_auto_scroll`.
- Param: settle_ms Input argument for `_auto_scroll`.
- Param: step_px Input argument for `_auto_scroll`.
- Param: max_rounds Input argument for `_auto_scroll`.
- Param: stable_rounds Input argument for `_auto_scroll`.
- Return: None Return value of `_auto_scroll`.

### fn `def _best_card_for_fragment(` `priv` (L2938-2939)
- Brief: Execute `_collect_cards_from_container`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_collect_cards_from_container`.
- Param: page Input argument for `_collect_cards_from_container`.
- Param: container Input argument for `_collect_cards_from_container`.
- Param: settle_ms Input argument for `_collect_cards_from_container`.
- Param: step_ratio Input argument for `_collect_cards_from_container`.
- Param: stable_rounds Input argument for `_collect_cards_from_container`.
- Param: max_rounds Input argument for `_collect_cards_from_container`.
- Return: Dict[str, str] Return value of `_collect_cards_from_container`.

### fn `def score_value(val: str) -> int` (L2958-2978)
- Brief: Execute `_best_card_for_fragment`.
- Brief: Execute `score_value`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_best_card_for_fragment`.
- Param: cards Input argument for `_best_card_for_fragment`.
- Param: fragment Input argument for `_best_card_for_fragment`.
- Param: val Input argument for `score_value`.
- Return: Optional[Tuple[str, str]] Return value of `_best_card_for_fragment`.
- Return: int Return value of `score_value`.

### fn `def _fragment_matches_url(self, fragment: str, data_url: str) -> bool` `priv` (L2995-3014)
- Brief: Execute `_fragment_matches_url`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_fragment_matches_url`.
- Param: fragment Input argument for `_fragment_matches_url`.
- Param: data_url Input argument for `_fragment_matches_url`.
- Return: bool Return value of `_fragment_matches_url`.

### fn `def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]` `priv` (L3015-3024)
- Brief: Execute `_toc_tree_from_html`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_toc_tree_from_html`.
- Param: toc_html Input argument for `_toc_tree_from_html`.
- Return: List[TocNode] Return value of `_toc_tree_from_html`.

### fn `def _iter_nodes(nodes: List[TocNode]) -> Iterable[TocNode]` `priv` `@staticmethod` (L3026-3036)
- Brief: Execute `_iter_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_iter_nodes`.
- Return: Iterable[TocNode] Return value of `_iter_nodes`.

### fn `def _first_numeric_index(nodes: List[TocNode]) -> Optional[int]` `priv` `@staticmethod` (L3038-3050)
- Brief: Execute `_first_numeric_index`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_first_numeric_index`.
- Return: Optional[int] Return value of `_first_numeric_index`.

### fn `def _trim_toc_nodes(nodes: List[TocNode]) -> List[TocNode]` `priv` `@staticmethod` (L3052-3073)
- Brief: Execute `_trim_toc_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_trim_toc_nodes`.
- Return: List[TocNode] Return value of `_trim_toc_nodes`.

### fn `def _limit_toc_nodes(` `priv` `@staticmethod` (L3075-3076)

### fn `def _limit_by_reading_order(` `priv` `@staticmethod` (L3088-3089)

### fn `def _prune_toc_to_allowed(` `priv` `@staticmethod` (L3127-3128)

### fn `def _first_toc_entry_title(nodes: List[TocNode]) -> Optional[str]` `priv` `@staticmethod` (L3151-3163)
- Brief: Execute `_first_toc_entry_title`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_first_toc_entry_title`.
- Return: Optional[str] Return value of `_first_toc_entry_title`.

### fn `def _is_important_notice_label(title: Optional[str]) -> bool` `priv` `@staticmethod` (L3165-3174)
- Brief: Execute `_is_important_notice_label`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: title Input argument for `_is_important_notice_label`.
- Return: bool Return value of `_is_important_notice_label`.

### fn `def _is_important_notice_section(section_html: str) -> bool` `priv` `@staticmethod` (L3176-3191)
- Brief: Execute `_is_important_notice_section`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: section_html Input argument for `_is_important_notice_section`.
- Return: bool Return value of `_is_important_notice_section`.

### fn `def _select_section_nodes(nodes: List[TocNode]) -> List[TocNode]` `priv` `@staticmethod` (L3193-3218)
- Brief: Execute `_select_section_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_select_section_nodes`.
- Return: List[TocNode] Return value of `_select_section_nodes`.

### fn `def _dedup_toc_nodes_by_href(self, nodes: List[TocNode]) -> List[TocNode]` `priv` (L3219-3257)
- Brief: Execute `_dedup_toc_nodes_by_href`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_dedup_toc_nodes_by_href`.
- Param: nodes Input argument for `_dedup_toc_nodes_by_href`.
- Return: List[TocNode] Return value of `_dedup_toc_nodes_by_href`.

### fn `def dedup_list(items: List[TocNode]) -> List[TocNode]` (L3228-3255)
- Brief: Execute `_dedup_toc_nodes_by_href`.
- Brief: Execute `dedup_list`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_dedup_toc_nodes_by_href`.
- Param: nodes Input argument for `_dedup_toc_nodes_by_href`.
- Param: items Input argument for `dedup_list`.
- Return: List[TocNode] Return value of `_dedup_toc_nodes_by_href`.
- Return: List[TocNode] Return value of `dedup_list`.

### fn `def _is_section_scrollable(self, page, viewport_multiplier: float = 2.0) -> bool` `priv` (L3258-3280)
- Brief: Execute `_is_section_scrollable`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_is_section_scrollable`.
- Param: page Input argument for `_is_section_scrollable`.
- Param: viewport_multiplier Input argument for `_is_section_scrollable`.
- Return: bool Return value of `_is_section_scrollable`.

### fn `def _remove_toc_elements(self, soup: BeautifulSoup) -> None` `priv` (L3281-3317)
- Brief: Execute `_remove_toc_elements`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_remove_toc_elements`.
- Param: soup Input argument for `_remove_toc_elements`.
- Return: None Return value of `_remove_toc_elements`.

### fn `def _convert_doxygen_definition_lists(self, soup: BeautifulSoup) -> None` `priv` (L3318-3384)
- Brief: Execute `_convert_doxygen_definition_lists`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_convert_doxygen_definition_lists`.
- Param: soup Input argument for `_convert_doxygen_definition_lists`.
- Return: None Return value of `_convert_doxygen_definition_lists`.

### fn `def _extract_fragment_only(` `priv` (L3385-3386)

### fn `def score_value(val: str) -> int` (L3405-3428)
- Brief: Execute `_extract_fragment_only`.
- Brief: Execute `score_value`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_extract_fragment_only`.
- Param: soup Input argument for `_extract_fragment_only`.
- Param: fragment Input argument for `_extract_fragment_only`.
- Param: val Input argument for `score_value`.
- Return: BeautifulSoup Return value of `_extract_fragment_only`.
- Return: int Return value of `score_value`.

### fn `def pick_best_section(elements)` (L3429-3452)
- Brief: Execute `pick_best_section`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: elements Input argument for `pick_best_section`.
- Return: Any Return value of `pick_best_section`.

### fn `def matches_fragment(el) -> bool` (L3463-3482)
- Brief: Execute `matches_fragment`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: el Input argument for `matches_fragment`.
- Return: bool Return value of `matches_fragment`.

### fn `def _wait_for_fragment(self, page, fragment: str, timeout_ms: int = 8000) -> bool` `priv` (L3510-3562)
- Brief: Execute `_wait_for_fragment`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_wait_for_fragment`.
- Param: page Input argument for `_wait_for_fragment`.
- Param: fragment Input argument for `_wait_for_fragment`.
- Param: timeout_ms Input argument for `_wait_for_fragment`.
- Return: bool Return value of `_wait_for_fragment`.

### fn `def _click_toc_link(self, page, fragment: str) -> bool` `priv` (L3563-3591)
- Brief: Execute `_click_toc_link`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_click_toc_link`.
- Param: page Input argument for `_click_toc_link`.
- Param: fragment Input argument for `_click_toc_link`.
- Return: bool Return value of `_click_toc_link`.

### fn `def run(self) -> None` (L3592-3791)
- Brief: Execute `run`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `run`.
- Return: None Return value of `run`.

### fn `def make_anchor(raw_fragment: str, title: str, used: Set[str]) -> str` (L3602-3620)
- Brief: Execute `run`.
- Brief: Execute `make_anchor`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `run`.
- Param: raw_fragment Input argument for `make_anchor`.
- Param: title Input argument for `make_anchor`.
- Param: used Input argument for `make_anchor`.
- Return: None Return value of `run`.
- Return: str Return value of `make_anchor`.

### fn `def normalize_text(value: str) -> str` (L3621-3631)
- Brief: Execute `normalize_text`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: value Input argument for `normalize_text`.
- Return: str Return value of `normalize_text`.

### fn `def strip_ti_disclaimer(section_html: str) -> str` (L3632-3662)
- Brief: Execute `strip_ti_disclaimer`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: section_html Input argument for `strip_ti_disclaimer`.
- Return: str Return value of `strip_ti_disclaimer`.

### class `class DoxygenExportDownloader(BaseDownloader)` : BaseDownloader (L4070-4269)
- Brief: Define class `DoxygenExportDownloader`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def matches_url(cls, url: str) -> bool` (L4078-4091)
  - Brief: Execute `matches_url`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `matches_url`.
  - Param: url Input argument for `matches_url`.
  - Return: bool Return value of `matches_url`.
- fn `def probe_html(cls, url: str, html: str) -> bool` (L4093-4104)
  - Brief: Execute `probe_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `probe_html`.
  - Param: url Input argument for `probe_html`.
  - Param: html Input argument for `probe_html`.
  - Return: bool Return value of `probe_html`.
- fn `def _scope(self) -> Tuple[str, str]` `priv` (L4105-4118)
  - Brief: Execute `_scope`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_scope`.
  - Return: Tuple[str, str] Return value of `_scope`.
- fn `def _fetch_soup(self, url: str) -> BeautifulSoup` `priv` (L4119-4130)
  - Brief: Execute `_fetch_soup`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_fetch_soup`.
  - Param: url Input argument for `_fetch_soup`.
  - Return: BeautifulSoup Return value of `_fetch_soup`.
- fn `def _is_in_scope(self, url: str, host: str, scope_dir_url: str) -> bool` `priv` (L4131-4147)
  - Brief: Execute `_is_in_scope`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_is_in_scope`.
  - Param: url Input argument for `_is_in_scope`.
  - Param: host Input argument for `_is_in_scope`.
  - Param: scope_dir_url Input argument for `_is_in_scope`.
  - Return: bool Return value of `_is_in_scope`.
- fn `def _page_title(self, soup: BeautifulSoup) -> str` `priv` (L4148-4163)
  - Brief: Execute `_page_title`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_page_title`.
  - Param: soup Input argument for `_page_title`.
  - Return: str Return value of `_page_title`.
- fn `def _document_title(self, soup: BeautifulSoup) -> str` `priv` (L4164-4195)
  - Brief: Execute `_document_title`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_document_title`.
  - Param: soup Input argument for `_document_title`.
  - Return: str Return value of `_document_title`.
- fn `def _extract_main(self, soup: BeautifulSoup) -> BeautifulSoup` `priv` (L4196-4219)
  - Brief: Execute `_extract_main`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_extract_main`.
  - Param: soup Input argument for `_extract_main`.
  - Return: BeautifulSoup Return value of `_extract_main`.
- fn `def _remove_toc_elements(self, soup: BeautifulSoup) -> None` `priv` (L4220-4246)
  - Brief: Execute `_remove_toc_elements`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_remove_toc_elements`.
  - Param: soup Input argument for `_remove_toc_elements`.
  - Return: None Return value of `_remove_toc_elements`.
- fn `def _links_to_html_pages(` `priv` (L4247-4248)

### fn `def _expand_nav_tree(self, page) -> None` `priv` (L4273-4309)
- Brief: Execute `_expand_nav_tree`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_expand_nav_tree`.
- Param: page Input argument for `_expand_nav_tree`.
- Return: None Return value of `_expand_nav_tree`.

### fn `def _expand_nav_tree_full(self, page) -> None` `priv` (L4310-4509)
- Brief: Execute `_expand_nav_tree_full`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_expand_nav_tree_full`.
- Param: page Input argument for `_expand_nav_tree_full`.
- Return: None Return value of `_expand_nav_tree_full`.

### fn `def _expand_nav_tree_limited(self, page, limit: int) -> None` `priv` (L4518-4627)
- Brief: Execute `_expand_nav_tree_limited`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_expand_nav_tree_limited`.
- Param: page Input argument for `_expand_nav_tree_limited`.
- Param: limit Input argument for `_expand_nav_tree_limited`.
- Return: None Return value of `_expand_nav_tree_limited`.

### fn `def _cleanup_nav_tree_styles(self, page) -> None` `priv` (L4628-4659)
- Brief: Execute `_cleanup_nav_tree_styles`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_cleanup_nav_tree_styles`.
- Param: page Input argument for `_cleanup_nav_tree_styles`.
- Return: None Return value of `_cleanup_nav_tree_styles`.

### fn `def _fetch_nav_tree_with_playwright(self) -> Tuple[str, str]` `priv` (L4660-4749)
- Brief: Execute `_fetch_nav_tree_with_playwright`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_fetch_nav_tree_with_playwright`.
- Return: Tuple[str, str] Return value of `_fetch_nav_tree_with_playwright`.

### fn `def _nav_link_href(self, link, base_url: str) -> str` `priv` (L4750-4775)
- Brief: Execute `_nav_link_href`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_nav_link_href`.
- Param: link Input argument for `_nav_link_href`.
- Param: base_url Input argument for `_nav_link_href`.
- Return: str Return value of `_nav_link_href`.

### fn `def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]` `priv` (L4776-4785)
- Brief: Execute `_toc_tree_from_html`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_toc_tree_from_html`.
- Param: toc_html Input argument for `_toc_tree_from_html`.
- Return: List[TocNode] Return value of `_toc_tree_from_html`.

### fn `def _toc_nodes_from_nav_html(self, nav_html: str) -> List[TocNode]` `priv` (L4786-4828)
- Brief: Execute `_toc_nodes_from_nav_html`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_toc_nodes_from_nav_html`.
- Param: nav_html Input argument for `_toc_nodes_from_nav_html`.
- Return: List[TocNode] Return value of `_toc_nodes_from_nav_html`.

### fn `def parse_ul(ul) -> List[TocNode]` (L4799-4823)
- Brief: Execute `_toc_nodes_from_nav_html`.
- Brief: Execute `parse_ul`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_toc_nodes_from_nav_html`.
- Param: nav_html Input argument for `_toc_nodes_from_nav_html`.
- Param: ul Input argument for `parse_ul`.
- Return: List[TocNode] Return value of `_toc_nodes_from_nav_html`.
- Return: List[TocNode] Return value of `parse_ul`.

### fn `def _iter_toc_nodes(nodes: List[TocNode]) -> Iterable[TocNode]` `priv` `@staticmethod` (L4830-4840)
- Brief: Execute `_iter_toc_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_iter_toc_nodes`.
- Return: Iterable[TocNode] Return value of `_iter_toc_nodes`.

### fn `def _select_main_container(self, soup: BeautifulSoup)` `priv` (L4841-4862)
- Brief: Execute `_select_main_container`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_select_main_container`.
- Param: soup Input argument for `_select_main_container`.
- Return: Any Return value of `_select_main_container`.

### fn `def _find_fragment_anchor(self, main, fragment: str)` `priv` (L4863-4890)
- Brief: Execute `_find_fragment_anchor`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_find_fragment_anchor`.
- Param: main Input argument for `_find_fragment_anchor`.
- Param: fragment Input argument for `_find_fragment_anchor`.
- Return: Any Return value of `_find_fragment_anchor`.

### fn `def _normalize_heading_text(value: str) -> str` `priv` `@staticmethod` (L4892-4900)
- Brief: Execute `_normalize_heading_text`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: value Input argument for `_normalize_heading_text`.
- Return: str Return value of `_normalize_heading_text`.

### fn `def _strip_duplicate_section_title(` `priv` (L4901-4902)

### fn `def _extract_section_html(` `priv` (L4945-4946)
- Brief: Execute `_strip_duplicate_section_title`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_strip_duplicate_section_title`.
- Param: container Input argument for `_strip_duplicate_section_title`.
- Param: title Input argument for `_strip_duplicate_section_title`.
- Param: section_anchor Input argument for `_strip_duplicate_section_title`.
- Return: Optional[str] Return value of `_strip_duplicate_section_title`.

### fn `def direct_child(el)` (L4974-4985)
- Brief: Execute `_extract_section_html`.
- Brief: Execute `direct_child`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_extract_section_html`.
- Param: soup Input argument for `_extract_section_html`.
- Param: fragment Input argument for `_extract_section_html`.
- Param: next_fragment Input argument for `_extract_section_html`.
- Param: el Input argument for `direct_child`.
- Return: str Return value of `_extract_section_html`.
- Return: Any Return value of `direct_child`.

### fn `def _build_toc(self, doc: BeautifulSoup) -> List[TocNode]` `priv` (L5009-5073)
- Brief: Execute `_build_toc`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_build_toc`.
- Param: doc Input argument for `_build_toc`.
- Return: List[TocNode] Return value of `_build_toc`.

### fn `def run(self) -> None` (L5074-5273)
- Brief: Execute `run`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `run`.
- Return: None Return value of `run`.

- var `MAX_PAGES = 250` (L5261)
### class `class ResourceExplorerModule` (L5439-5471)
- Brief: Define class `ResourceExplorerModule`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def select(` (L5446-5447)
  - Brief: Define class `ResourceExplorerModule`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def run(self, downloader: "ResourceExplorerDownloader", selection: Dict[str, str]) -> None` (L5460-5471)
  - Brief: Execute `select`.
  - Brief: Execute `run`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `select`.
  - Param: url Input argument for `select`.
  - Param: html Input argument for `select`.
  - Param: soup Input argument for `select`.
  - Param: self Input argument for `run`.
  - Param: downloader Input argument for `run`.
  - Param: selection Input argument for `run`.
  - Return: Optional[Dict[str, str]] Return value of `select`.
  - Return: None Return value of `run`.

### class `class RMModuleDoxigen(ResourceExplorerModule)` : ResourceExplorerModule (L5472-5529)
- Brief: Define class `RMModuleDoxigen`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def select(` (L5481-5482)
  - Brief: Define class `RMModuleDoxigen`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def run(self, downloader: "ResourceExplorerDownloader", selection: Dict[str, str]) -> None` (L5506-5529)
  - Brief: Execute `select`.
  - Brief: Execute `run`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `select`.
  - Param: url Input argument for `select`.
  - Param: html Input argument for `select`.
  - Param: soup Input argument for `select`.
  - Param: self Input argument for `run`.
  - Param: downloader Input argument for `run`.
  - Param: selection Input argument for `run`.
  - Return: Optional[Dict[str, str]] Return value of `select`.
  - Return: None Return value of `run`.

### class `class ResourceExplorerDownloader(BaseDownloader)` : BaseDownloader (L5530-5662)
- Brief: Define class `ResourceExplorerDownloader`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
- fn `def __init__(self, *args, **kwargs)` `priv` (L5537-5548)
  - Brief: Define class `ResourceExplorerDownloader`.
  - Brief: Execute `__init__`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`.
  - Param: *args Input argument for `__init__`.
  - Param: **kwargs Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def matches_url(cls, url: str) -> bool` (L5550-5560)
  - Brief: Execute `matches_url`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `matches_url`.
  - Param: url Input argument for `matches_url`.
  - Return: bool Return value of `matches_url`.
- fn `def probe_html(cls, url: str, html: str) -> bool` (L5562-5572)
  - Brief: Execute `probe_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `probe_html`.
  - Param: url Input argument for `probe_html`.
  - Param: html Input argument for `probe_html`.
  - Return: bool Return value of `probe_html`.
- fn `def _select_module(` `priv` (L5573-5574)
- fn `def _render_with_playwright(self) -> str` `priv` (L5590-5627)
  - Brief: Execute `_select_module`.
  - Brief: Execute `_render_with_playwright`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_select_module`.
  - Param: html Input argument for `_select_module`.
  - Param: soup Input argument for `_select_module`.
  - Param: self Input argument for `_render_with_playwright`.
  - Return: Optional[Tuple[ResourceExplorerModule, Dict[str, str]]] Return value of `_select_module`.
  - Return: str Return value of `_render_with_playwright`.
- fn `def run(self) -> None` (L5628-5662)
  - Brief: Execute `run`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `run`.
  - Return: None Return value of `run`.

### fn `def build_arg_parser() -> argparse.ArgumentParser` (L5668-5713)
- Brief: Execute `build_arg_parser`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Return: argparse.ArgumentParser Return value of `build_arg_parser`.

### fn `def print_strict_help(program: str, version: str, parser: argparse.ArgumentParser) -> None` (L5714-5759)
- Brief: Execute `print_strict_help`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: program Input argument for `print_strict_help`.
- Param: version Input argument for `print_strict_help`.
- Param: parser Input argument for `print_strict_help`.
- Return: None Return value of `print_strict_help`.

### fn `def main() -> int` (L5760-5811)
- Brief: Execute `main`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Return: int Return value of `main`.

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`GITHUB_API_TIMEOUT_S`|var|pub|36||
|`_parse_version_tuple`|fn|priv|39-58|def _parse_version_tuple(v: str) -> Optional[Tuple[int, ....|
|`_is_version_newer`|fn|priv|59-76|def _is_version_newer(latest: str, current: str) -> bool|
|`_get_latest_version_from_github`|fn|priv|77-106|def _get_latest_version_from_github(owner: str, repo: str...|
|`check_for_new_version`|fn|pub|107-125|def check_for_new_version(program: str, current_version: ...|
|`safe_filename`|fn|pub|131-143|def safe_filename(path: str) -> str|
|`positive_int`|fn|pub|144-159|def positive_int(value: str) -> int|
|`is_http_url`|fn|pub|160-173|def is_http_url(s: str) -> bool|
|`normalize_url`|fn|pub|174-189|def normalize_url(u: str, base: str) -> str|
|`ensure_parent`|fn|pub|190-199|def ensure_parent(p: Path) -> None|
|`local_path_for_url`|fn|pub|200-222|def local_path_for_url(asset_url: str, out_dir: Path) -> ...|
|`download_one`|fn|pub|223-224|def download_one(|
|`escape_html`|fn|pub|248-263|def escape_html(s: str) -> str|
|`TocNode`|class|pub|265-274|class TocNode|
|`limit_toc_nodes`|fn|pub|275-307|def limit_toc_nodes(nodes: List[TocNode], max_entries: Op...|
|`trim_list`|fn|pub|288-304|def trim_list(items: List[TocNode]) -> List[TocNode]|
|`ensure_heading_ids`|fn|pub|308-332|def ensure_heading_ids(soup: BeautifulSoup) -> None|
|`strip_styles`|fn|pub|333-350|def strip_styles(soup: BeautifulSoup) -> None|
|`toc_from_headings`|fn|pub|351-378|def toc_from_headings(soup: BeautifulSoup) -> List[TocNode]|
|`toc_from_nav_html`|fn|pub|379-429|def toc_from_nav_html(toc_html: str, base_url: str) -> Li...|
|`parse_list`|fn|pub|389-418|def parse_list(list_el) -> List[TocNode]|
|`nav_outline_from_html`|fn|pub|430-493|def nav_outline_from_html(nav_html: str) -> str|
|`norm_text`|fn|pub|441-450|def norm_text(t: str) -> str|
|`bullet`|fn|pub|451-463|def bullet(depth: int) -> str|
|`walk_ul`|fn|pub|464-487|def walk_ul(ul, depth: int) -> None|
|`ASSET_ATTRS`|var|pub|495||
|`HEADING_TAG_RE`|var|pub|503||
|`Logger`|class|pub|506-567|class Logger|
|`Logger.__init__`|fn|priv|512-523|def __init__(self, verbose: bool = False, debug: bool = F...|
|`Logger.info`|fn|pub|524-533|def info(self, msg: str) -> None|
|`Logger.verbose`|fn|pub|534-544|def verbose(self, msg: str) -> None|
|`Logger.debug`|fn|pub|545-555|def debug(self, msg: str) -> None|
|`Logger.check`|fn|pub|556-567|def check(self, msg: str) -> None|
|`UpgradeAction`|class|pub|568-605|class UpgradeAction(argparse.Action)|
|`UpgradeAction.__call__`|fn|priv|573-578|def __call__(|
|`VersionedArgumentParser`|class|pub|606-644|class VersionedArgumentParser(argparse.ArgumentParser)|
|`VersionedArgumentParser.__init__`|fn|priv|612-624|def __init__(self, *args, version: str = "", **kwargs)|
|`VersionedArgumentParser.format_usage`|fn|pub|625-644|def format_usage(self) -> str|
|`iter_asset_urls`|fn|pub|645-683|def iter_asset_urls(soup: BeautifulSoup, page_url: str) -...|
|`rewrite_asset_links_inplace`|fn|pub|684-685|def rewrite_asset_links_inplace(|
|`to_rel`|fn|pub|695-707|def to_rel(u: str) -> str|
|`repl`|fn|pub|731-740|def repl(m)|
|`ALLOWED_EXTERNAL_LINK_SCHEMES`|var|pub|745||
|`normalize_document_links_inplace`|fn|pub|753-878|def normalize_document_links_inplace(soup: BeautifulSoup,...|
|`build_toc_html`|fn|pub|879-882|def build_toc_html(|
|`resolved_href`|fn|pub|892-906|def resolved_href(href: str) -> str|
|`render_nodes`|fn|pub|907-935|def render_nodes(nodes: List[TocNode], indent_level: int ...|
|`build_frameset_index`|fn|pub|957-958|def build_frameset_index(|
|`minimal_readable_wrapper`|fn|pub|987-988|def minimal_readable_wrapper(|
|`BaseDownloader`|class|pub|1016-1215|class BaseDownloader|
|`BaseDownloader.__init__`|fn|priv|1023-1031|def __init__(|
|`BaseDownloader.matches_url`|fn|pub|1076-1085|def matches_url(cls, url: str) -> bool|
|`BaseDownloader.probe_html`|fn|pub|1087-1097|def probe_html(cls, url: str, html: str) -> bool|
|`BaseDownloader.run`|fn|pub|1098-1106|def run(self) -> None|
|`BaseDownloader._toc_tree_from_html`|fn|priv|1107-1116|def _toc_tree_from_html(self, toc_html: str) -> List[TocN...|
|`BaseDownloader.post_process`|fn|pub|1117-1131|def post_process(self) -> None|
|`BaseDownloader._verify_toc_consistency`|fn|priv|1132-1183|def _verify_toc_consistency(self) -> None|
|`_verify_toc_depth`|fn|priv|1184-1223|def _verify_toc_depth(self) -> None|
|`BaseDownloader.get_max_depth`|fn|pub|1197-1213|def get_max_depth(ul, current_depth=0)|
|`_prune_toc_and_clean_headings`|fn|priv|1224-1325|def _prune_toc_and_clean_headings(self) -> None|
|`href_fragment_id`|fn|pub|1235-1247|def href_fragment_id(href: str) -> str|
|`prune_ul`|fn|pub|1258-1278|def prune_ul(ul, depth)|
|`_deduplicate_toc_entries`|fn|priv|1326-1394|def _deduplicate_toc_entries(self) -> None|
|`href_fragment_id`|fn|pub|1339-1351|def href_fragment_id(href: str) -> str|
|`process_nodes`|fn|pub|1358-1386|def process_nodes(nodes: List[TocNode], seen: Set[str]) -...|
|`_enforce_toc_headings`|fn|priv|1395-1513|def _enforce_toc_headings(self) -> None|
|`href_fragment_id`|fn|pub|1410-1422|def href_fragment_id(href: str) -> str|
|`clamp_heading_level`|fn|pub|1434-1450|def clamp_heading_level(depth: int) -> int|
|`find_referenced_container_id`|fn|pub|1451-1468|def find_referenced_container_id(h) -> str|
|`_test_toc_headings`|fn|priv|1514-1709|def _test_toc_headings(self) -> None|
|`href_fragment_id`|fn|pub|1530-1542|def href_fragment_id(href: str) -> str|
|`clamp_heading_level`|fn|pub|1543-1555|def clamp_heading_level(depth: int) -> int|
|`summarize`|fn|pub|1673-1686|def summarize(items: List[str]) -> str|
|`fix_heading_ref_position`|fn|pub|1710-1850|def fix_heading_ref_position(self) -> None|
|`fix_heading_numbering`|fn|pub|1851-1989|def fix_heading_numbering(self) -> None|
|`normalize_ws`|fn|pub|1870-1878|def normalize_ws(text: str) -> str|
|`strip_numbering_prefix`|fn|pub|1879-1887|def strip_numbering_prefix(text: str) -> str|
|`set_flat_text`|fn|pub|1888-1898|def set_flat_text(tag, text: str) -> None|
|`href_fragment_id`|fn|pub|1920-1932|def href_fragment_id(href: str) -> str|
|`_clean_document_style`|fn|priv|1990-2010|def _clean_document_style(self) -> None|
|`_add_document_style`|fn|priv|2011-2042|def _add_document_style(self) -> None|
|`_normalize_document_links`|fn|priv|2057-2071|def _normalize_document_links(self) -> None|
|`_remove_unused_images`|fn|priv|2072-2113|def _remove_unused_images(self) -> None|
|`_remove_unused_assets`|fn|priv|2114-2148|def _remove_unused_assets(self) -> None|
|`_normalize_image_position`|fn|priv|2149-2208|def _normalize_image_position(self) -> None|
|`_clean_assets_tree`|fn|priv|2209-2231|def _clean_assets_tree(self) -> None|
|`_remove_empty_assets_root`|fn|priv|2232-2270|def _remove_empty_assets_root(self) -> None|
|`DownloaderRegistry`|class|pub|2271-2328|class DownloaderRegistry|
|`DownloaderRegistry.__init__`|fn|priv|2276-2284|def __init__(self)|
|`DownloaderRegistry.register`|fn|pub|2285-2294|def register(self, downloader_cls: type[BaseDownloader]) ...|
|`DownloaderRegistry.detect`|fn|pub|2295-2328|def detect(self, url: str, session: requests.Session) -> ...|
|`guess_ext_from_content_type`|fn|pub|2334-2353|def guess_ext_from_content_type(ct: str) -> str|
|`NetworkImageRecorder`|class|pub|2354-2416|class NetworkImageRecorder|
|`NetworkImageRecorder.__init__`|fn|priv|2360-2371|def __init__(self, out_dir: Path)|
|`NetworkImageRecorder.attach`|fn|pub|2372-2416|def attach(self, page)|
|`NetworkImageRecorder.on_response`|fn|pub|2380-2413|def on_response(resp)|
|`DocumentViewerDownloader`|class|pub|2417-2616|class DocumentViewerDownloader(BaseDownloader)|
|`DocumentViewerDownloader.TOC_SELECTORS`|var|pub|2424||
|`DocumentViewerDownloader.CONTENT_SELECTORS`|var|pub|2433||
|`DocumentViewerDownloader.TOC_SCROLL_SELECTORS`|var|pub|2446||
|`DocumentViewerDownloader.matches_url`|fn|pub|2455-2465|def matches_url(cls, url: str) -> bool|
|`DocumentViewerDownloader.probe_html`|fn|pub|2467-2478|def probe_html(cls, url: str, html: str) -> bool|
|`DocumentViewerDownloader._pick_best_outerhtml`|fn|priv|2479-2510|def _pick_best_outerhtml(self, page, selectors: List[str]...|
|`DocumentViewerDownloader._expand_full_toc`|fn|priv|2511-2512|def _expand_full_toc(|
|`DocumentViewerDownloader._scroll_toc_container`|fn|priv|2572-2573|def _scroll_toc_container(|
|`_find_scroll_container`|fn|priv|2630-2695|def _find_scroll_container(self, page)|
|`_auto_scroll_element`|fn|priv|2696-2704|def _auto_scroll_element(|
|`_auto_scroll`|fn|priv|2777-2783|def _auto_scroll(|
|`_collect_cards_from_container`|fn|priv|2853-2860|def _collect_cards_from_container(|
|`_best_card_for_fragment`|fn|priv|2938-2939|def _best_card_for_fragment(|
|`score_value`|fn|pub|2958-2978|def score_value(val: str) -> int|
|`_fragment_matches_url`|fn|priv|2995-3014|def _fragment_matches_url(self, fragment: str, data_url: ...|
|`_toc_tree_from_html`|fn|priv|3015-3024|def _toc_tree_from_html(self, toc_html: str) -> List[TocN...|
|`_iter_nodes`|fn|priv|3026-3036|def _iter_nodes(nodes: List[TocNode]) -> Iterable[TocNode]|
|`_first_numeric_index`|fn|priv|3038-3050|def _first_numeric_index(nodes: List[TocNode]) -> Optiona...|
|`_trim_toc_nodes`|fn|priv|3052-3073|def _trim_toc_nodes(nodes: List[TocNode]) -> List[TocNode]|
|`_limit_toc_nodes`|fn|priv|3075-3076|def _limit_toc_nodes(|
|`_limit_by_reading_order`|fn|priv|3088-3089|def _limit_by_reading_order(|
|`_prune_toc_to_allowed`|fn|priv|3127-3128|def _prune_toc_to_allowed(|
|`_first_toc_entry_title`|fn|priv|3151-3163|def _first_toc_entry_title(nodes: List[TocNode]) -> Optio...|
|`_is_important_notice_label`|fn|priv|3165-3174|def _is_important_notice_label(title: Optional[str]) -> bool|
|`_is_important_notice_section`|fn|priv|3176-3191|def _is_important_notice_section(section_html: str) -> bool|
|`_select_section_nodes`|fn|priv|3193-3218|def _select_section_nodes(nodes: List[TocNode]) -> List[T...|
|`_dedup_toc_nodes_by_href`|fn|priv|3219-3257|def _dedup_toc_nodes_by_href(self, nodes: List[TocNode]) ...|
|`dedup_list`|fn|pub|3228-3255|def dedup_list(items: List[TocNode]) -> List[TocNode]|
|`_is_section_scrollable`|fn|priv|3258-3280|def _is_section_scrollable(self, page, viewport_multiplie...|
|`_remove_toc_elements`|fn|priv|3281-3317|def _remove_toc_elements(self, soup: BeautifulSoup) -> None|
|`_convert_doxygen_definition_lists`|fn|priv|3318-3384|def _convert_doxygen_definition_lists(self, soup: Beautif...|
|`_extract_fragment_only`|fn|priv|3385-3386|def _extract_fragment_only(|
|`score_value`|fn|pub|3405-3428|def score_value(val: str) -> int|
|`pick_best_section`|fn|pub|3429-3452|def pick_best_section(elements)|
|`matches_fragment`|fn|pub|3463-3482|def matches_fragment(el) -> bool|
|`_wait_for_fragment`|fn|priv|3510-3562|def _wait_for_fragment(self, page, fragment: str, timeout...|
|`_click_toc_link`|fn|priv|3563-3591|def _click_toc_link(self, page, fragment: str) -> bool|
|`run`|fn|pub|3592-3791|def run(self) -> None|
|`make_anchor`|fn|pub|3602-3620|def make_anchor(raw_fragment: str, title: str, used: Set[...|
|`normalize_text`|fn|pub|3621-3631|def normalize_text(value: str) -> str|
|`strip_ti_disclaimer`|fn|pub|3632-3662|def strip_ti_disclaimer(section_html: str) -> str|
|`DoxygenExportDownloader`|class|pub|4070-4269|class DoxygenExportDownloader(BaseDownloader)|
|`DoxygenExportDownloader.matches_url`|fn|pub|4078-4091|def matches_url(cls, url: str) -> bool|
|`DoxygenExportDownloader.probe_html`|fn|pub|4093-4104|def probe_html(cls, url: str, html: str) -> bool|
|`DoxygenExportDownloader._scope`|fn|priv|4105-4118|def _scope(self) -> Tuple[str, str]|
|`DoxygenExportDownloader._fetch_soup`|fn|priv|4119-4130|def _fetch_soup(self, url: str) -> BeautifulSoup|
|`DoxygenExportDownloader._is_in_scope`|fn|priv|4131-4147|def _is_in_scope(self, url: str, host: str, scope_dir_url...|
|`DoxygenExportDownloader._page_title`|fn|priv|4148-4163|def _page_title(self, soup: BeautifulSoup) -> str|
|`DoxygenExportDownloader._document_title`|fn|priv|4164-4195|def _document_title(self, soup: BeautifulSoup) -> str|
|`DoxygenExportDownloader._extract_main`|fn|priv|4196-4219|def _extract_main(self, soup: BeautifulSoup) -> Beautiful...|
|`DoxygenExportDownloader._remove_toc_elements`|fn|priv|4220-4246|def _remove_toc_elements(self, soup: BeautifulSoup) -> None|
|`DoxygenExportDownloader._links_to_html_pages`|fn|priv|4247-4248|def _links_to_html_pages(|
|`_expand_nav_tree`|fn|priv|4273-4309|def _expand_nav_tree(self, page) -> None|
|`_expand_nav_tree_full`|fn|priv|4310-4509|def _expand_nav_tree_full(self, page) -> None|
|`_expand_nav_tree_limited`|fn|priv|4518-4627|def _expand_nav_tree_limited(self, page, limit: int) -> None|
|`_cleanup_nav_tree_styles`|fn|priv|4628-4659|def _cleanup_nav_tree_styles(self, page) -> None|
|`_fetch_nav_tree_with_playwright`|fn|priv|4660-4749|def _fetch_nav_tree_with_playwright(self) -> Tuple[str, str]|
|`_nav_link_href`|fn|priv|4750-4775|def _nav_link_href(self, link, base_url: str) -> str|
|`_toc_tree_from_html`|fn|priv|4776-4785|def _toc_tree_from_html(self, toc_html: str) -> List[TocN...|
|`_toc_nodes_from_nav_html`|fn|priv|4786-4828|def _toc_nodes_from_nav_html(self, nav_html: str) -> List...|
|`parse_ul`|fn|pub|4799-4823|def parse_ul(ul) -> List[TocNode]|
|`_iter_toc_nodes`|fn|priv|4830-4840|def _iter_toc_nodes(nodes: List[TocNode]) -> Iterable[Toc...|
|`_select_main_container`|fn|priv|4841-4862|def _select_main_container(self, soup: BeautifulSoup)|
|`_find_fragment_anchor`|fn|priv|4863-4890|def _find_fragment_anchor(self, main, fragment: str)|
|`_normalize_heading_text`|fn|priv|4892-4900|def _normalize_heading_text(value: str) -> str|
|`_strip_duplicate_section_title`|fn|priv|4901-4902|def _strip_duplicate_section_title(|
|`_extract_section_html`|fn|priv|4945-4946|def _extract_section_html(|
|`direct_child`|fn|pub|4974-4985|def direct_child(el)|
|`_build_toc`|fn|priv|5009-5073|def _build_toc(self, doc: BeautifulSoup) -> List[TocNode]|
|`run`|fn|pub|5074-5273|def run(self) -> None|
|`MAX_PAGES`|var|pub|5261||
|`ResourceExplorerModule`|class|pub|5439-5471|class ResourceExplorerModule|
|`ResourceExplorerModule.select`|fn|pub|5446-5447|def select(|
|`ResourceExplorerModule.run`|fn|pub|5460-5471|def run(self, downloader: "ResourceExplorerDownloader", s...|
|`RMModuleDoxigen`|class|pub|5472-5529|class RMModuleDoxigen(ResourceExplorerModule)|
|`RMModuleDoxigen.select`|fn|pub|5481-5482|def select(|
|`RMModuleDoxigen.run`|fn|pub|5506-5529|def run(self, downloader: "ResourceExplorerDownloader", s...|
|`ResourceExplorerDownloader`|class|pub|5530-5662|class ResourceExplorerDownloader(BaseDownloader)|
|`ResourceExplorerDownloader.__init__`|fn|priv|5537-5548|def __init__(self, *args, **kwargs)|
|`ResourceExplorerDownloader.matches_url`|fn|pub|5550-5560|def matches_url(cls, url: str) -> bool|
|`ResourceExplorerDownloader.probe_html`|fn|pub|5562-5572|def probe_html(cls, url: str, html: str) -> bool|
|`ResourceExplorerDownloader._select_module`|fn|priv|5573-5574|def _select_module(|
|`ResourceExplorerDownloader._render_with_playwright`|fn|priv|5590-5627|def _render_with_playwright(self) -> str|
|`ResourceExplorerDownloader.run`|fn|pub|5628-5662|def run(self) -> None|
|`build_arg_parser`|fn|pub|5668-5713|def build_arg_parser() -> argparse.ArgumentParser|
|`print_strict_help`|fn|pub|5714-5759|def print_strict_help(program: str, version: str, parser:...|
|`main`|fn|pub|5760-5811|def main() -> int|


---

# version.py | Python | 13L | 0 symbols | 0 imports | 3 comments
> Path: `src/htmldownloader/version.py`
- Brief: HtmlDownloader package entry module.
- Details: Exposes package-level symbols used by CLI entrypoints and version reporting.
@module_symbols functions=0 classes=0 variables=2
@variables __version__, __all__

