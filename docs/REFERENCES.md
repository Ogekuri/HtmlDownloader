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
> Path: `/home/ogekuri/HtmlDownloader/src/htmldownloader/__init__.py`

## Imports
```
from .version import __version__
from .cli import main
```


---

# __main__.py | Python | 12L | 0 symbols | 2 imports | 1 comments
> Path: `/home/ogekuri/HtmlDownloader/src/htmldownloader/__main__.py`

## Imports
```
from .cli import main
import sys
```


---

# cli.py | Python | 5812L | 184 symbols | 21 imports | 339 comments
> Path: `/home/ogekuri/HtmlDownloader/src/htmldownloader/cli.py`

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

- var `GITHUB_API_TIMEOUT_S = 1` (L37)
- Brief: Module-level variable `GITHUB_API_TIMEOUT_S`.
### fn `def _parse_version_tuple(v: str) -> Optional[Tuple[int, ...]]` `priv` (L40-59)
- Brief: Execute `_parse_version_tuple`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: v Input argument for `_parse_version_tuple`.
- Return: Optional[Tuple[int, ...]] Return value of `_parse_version_tuple`.

### fn `def _is_version_newer(latest: str, current: str) -> bool` `priv` (L60-77)
- Brief: Execute `_is_version_newer`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: latest Input argument for `_is_version_newer`. current Input argument for `_is_version_newer`.
- Return: bool Return value of `_is_version_newer`.

### fn `def _get_latest_version_from_github(owner: str, repo: str) -> Optional[str]` `priv` (L78-107)
- Brief: Execute `_get_latest_version_from_github`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: owner Input argument for `_get_latest_version_from_github`. repo Input argument for `_get_latest_version_from_github`.
- Return: Optional[str] Return value of `_get_latest_version_from_github`.

### fn `def check_for_new_version(program: str, current_version: str) -> None` (L108-126)
- Brief: Execute `check_for_new_version`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: program Input argument for `check_for_new_version`. current_version Input argument for `check_for_new_version`.
- Return: None Return value of `check_for_new_version`.

### fn `def safe_filename(path: str) -> str` (L132-144)
- Brief: Execute `safe_filename`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: path Input argument for `safe_filename`.
- Return: str Return value of `safe_filename`.

### fn `def positive_int(value: str) -> int` (L145-160)
- Brief: Execute `positive_int`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: value Input argument for `positive_int`.
- Return: int Return value of `positive_int`.

### fn `def is_http_url(s: str) -> bool` (L161-174)
- Brief: Execute `is_http_url`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: s Input argument for `is_http_url`.
- Return: bool Return value of `is_http_url`.

### fn `def normalize_url(u: str, base: str) -> str` (L175-190)
- Brief: Execute `normalize_url`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: u Input argument for `normalize_url`. base Input argument for `normalize_url`.
- Return: str Return value of `normalize_url`.

### fn `def ensure_parent(p: Path) -> None` (L191-200)
- Brief: Execute `ensure_parent`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: p Input argument for `ensure_parent`.
- Return: None Return value of `ensure_parent`.

### fn `def local_path_for_url(asset_url: str, out_dir: Path) -> Path` (L201-223)
- Brief: Execute `local_path_for_url`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: asset_url Input argument for `local_path_for_url`. out_dir Input argument for `local_path_for_url`.
- Return: Path Return value of `local_path_for_url`.

### fn `def download_one(` (L224-225)

### fn `def escape_html(s: str) -> str` (L249-264)
- Brief: Execute `escape_html`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: s Input argument for `escape_html`.
- Return: str Return value of `escape_html`.

### class `class TocNode` `@dataclass` (L266-275)
- Brief: Define class `TocNode`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline.

### fn `def limit_toc_nodes(nodes: List[TocNode], max_entries: Optional[int]) -> List[TocNode]` (L276-308)
- Brief: Execute `limit_toc_nodes`. Execute `trim_list`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `limit_toc_nodes`. max_entries Input argument for `limit_toc_nodes`. items Input argument for `trim_list`.
- Return: List[TocNode] Return value of `limit_toc_nodes`. List[TocNode] Return value of `trim_list`.

### fn `def trim_list(items: List[TocNode]) -> List[TocNode]` (L289-305)
- Brief: Execute `trim_list`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: items Input argument for `trim_list`.
- Return: List[TocNode] Return value of `trim_list`.

### fn `def ensure_heading_ids(soup: BeautifulSoup) -> None` (L309-333)
- Brief: Execute `ensure_heading_ids`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `ensure_heading_ids`.
- Return: None Return value of `ensure_heading_ids`.

### fn `def strip_styles(soup: BeautifulSoup) -> None` (L334-351)
- Brief: Execute `strip_styles`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `strip_styles`.
- Return: None Return value of `strip_styles`.

### fn `def toc_from_headings(soup: BeautifulSoup) -> List[TocNode]` (L352-379)
- Brief: Execute `toc_from_headings`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `toc_from_headings`.
- Return: List[TocNode] Return value of `toc_from_headings`.

### fn `def toc_from_nav_html(toc_html: str, base_url: str) -> List[TocNode]` (L380-430)
- Brief: Execute `toc_from_nav_html`. Execute `parse_list`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: toc_html Input argument for `toc_from_nav_html`. base_url Input argument for `toc_from_nav_html`. list_el Input argument for `parse_list`.
- Return: List[TocNode] Return value of `toc_from_nav_html`. List[TocNode] Return value of `parse_list`.

### fn `def parse_list(list_el) -> List[TocNode]` (L390-419)
- Brief: Execute `parse_list`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: list_el Input argument for `parse_list`.
- Return: List[TocNode] Return value of `parse_list`.

### fn `def nav_outline_from_html(nav_html: str) -> str` (L431-494)
- Brief: Execute `nav_outline_from_html`. Execute `norm_text`. Execute `bullet`. Execute `walk_ul`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: nav_html Input argument for `nav_outline_from_html`. t Input argument for `norm_text`. depth Input argument for `bullet`. ul Input argument for `walk_ul`. depth Input argument for `walk_ul`.
- Return: str Return value of `nav_outline_from_html`. str Return value of `norm_text`. str Return value of `bullet`. None Return value of `walk_ul`.

### fn `def norm_text(t: str) -> str` (L442-451)
- Brief: Execute `norm_text`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: t Input argument for `norm_text`.
- Return: str Return value of `norm_text`.

### fn `def bullet(depth: int) -> str` (L452-464)
- Brief: Execute `bullet`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: depth Input argument for `bullet`.
- Return: str Return value of `bullet`.

### fn `def walk_ul(ul, depth: int) -> None` (L465-488)
- Brief: Execute `walk_ul`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: ul Input argument for `walk_ul`. depth Input argument for `walk_ul`.
- Return: None Return value of `walk_ul`.

- var `ASSET_ATTRS = [` (L496)
- Brief: Module-level variable `ASSET_ATTRS`.
- var `HEADING_TAG_RE = re.compile(r"^h[1-6]$")` (L504)
- Brief: Module-level variable `HEADING_TAG_RE`.
### class `class Logger` (L507-568)
- Brief: Define class `Logger`. Execute `__init__`. Execute `info`. Execute `verbose`. Execute `debug`. Execute `check`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `__init__`. verbose Input argument for `__init__`. debug Input argument for `__init__`. self Input argument for `info`. msg Input argument for `info`. self Input argument for `verbose`. msg Input argument for `verbose`. self Input argument for `debug`. msg Input argument for `debug`. self Input argument for `check`. msg Input argument for `check`.
- Return: Any Return value of `__init__`. None Return value of `info`. None Return value of `verbose`. None Return value of `debug`. None Return value of `check`.
- fn `def __init__(self, verbose: bool = False, debug: bool = False)` `priv` (L513-524)
  - Brief: Define class `Logger`. Execute `__init__`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`. verbose Input argument for `__init__`. debug Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def info(self, msg: str) -> None` (L525-534)
  - Brief: Execute `info`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `info`. msg Input argument for `info`.
  - Return: None Return value of `info`.
- fn `def verbose(self, msg: str) -> None` (L535-545)
  - Brief: Execute `verbose`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `verbose`. msg Input argument for `verbose`.
  - Return: None Return value of `verbose`.
- fn `def debug(self, msg: str) -> None` (L546-556)
  - Brief: Execute `debug`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `debug`. msg Input argument for `debug`.
  - Return: None Return value of `debug`.
- fn `def check(self, msg: str) -> None` (L557-568)
  - Brief: Execute `check`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `check`. msg Input argument for `check`.
  - Return: None Return value of `check`.

### class `class UpgradeAction(argparse.Action)` : argparse.Action (L569-606)
- Brief: Define class `UpgradeAction`. Execute `__call__`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `__call__`. parser Input argument for `__call__`. namespace Input argument for `__call__`. values Input argument for `__call__`. option_string Input argument for `__call__`.
- Return: None Return value of `__call__`.
- fn `def __call__(` `priv` (L574-579)
  - Brief: Define class `UpgradeAction`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline.

### class `class VersionedArgumentParser(argparse.ArgumentParser)` : argparse.ArgumentParser (L607-645)
- Brief: Define class `VersionedArgumentParser`. Execute `__init__`. Execute `format_usage`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `__init__`. version Input argument for `__init__`. *args Input argument for `__init__`. **kwargs Input argument for `__init__`. self Input argument for `format_usage`.
- Return: Any Return value of `__init__`. str Return value of `format_usage`.
- fn `def __init__(self, *args, version: str = "", **kwargs)` `priv` (L613-625)
  - Brief: Define class `VersionedArgumentParser`. Execute `__init__`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`. version Input argument for `__init__`. *args Input argument for `__init__`. **kwargs Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def format_usage(self) -> str` (L626-645)
  - Brief: Execute `format_usage`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `format_usage`.
  - Return: str Return value of `format_usage`.

### fn `def iter_asset_urls(soup: BeautifulSoup, page_url: str) -> Set[str]` (L646-684)
- Brief: Execute `iter_asset_urls`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `iter_asset_urls`. page_url Input argument for `iter_asset_urls`.
- Return: Set[str] Return value of `iter_asset_urls`.

### fn `def rewrite_asset_links_inplace(` (L685-686)

### fn `def to_rel(u: str) -> str` (L696-708)
- Brief: Execute `rewrite_asset_links_inplace`. Execute `to_rel`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `rewrite_asset_links_inplace`.
... u Input argument for `to_rel`.
- Return: str Return value of `to_rel`.

### fn `def repl(m)` (L732-741)
- Brief: Execute `repl`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: m Input argument for `repl`.
- Return: Any Return value of `repl`.

- var `ALLOWED_EXTERNAL_LINK_SCHEMES = {` (L746)
- Brief: Module-level variable `ALLOWED_EXTERNAL_LINK_SCHEMES`.
### fn `def normalize_document_links_inplace(soup: BeautifulSoup, logger: Optional[Logger]) -> None` (L754-879)
- Brief: Execute `normalize_document_links_inplace`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: soup Input argument for `normalize_document_links_inplace`. logger Input argument for `normalize_document_links_inplace`.
- Return: None Return value of `normalize_document_links_inplace`.

### fn `def build_toc_html(` (L880-883)

### fn `def resolved_href(href: str) -> str` (L893-907)
- Brief: Execute `build_toc_html`. Execute `resolved_href`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: toc_items Input argument for `build_toc_html`.
... href Input argument for `resolved_href`.
- Return: str Return value of `resolved_href`.

### fn `def render_nodes(nodes: List[TocNode]) -> str` (L908-925)
- Brief: Execute `render_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `render_nodes`.
- Return: str Return value of `render_nodes`.

### fn `def build_frameset_index(` (L947-948)

### fn `def minimal_readable_wrapper(` (L977-978)

### class `class BaseDownloader` (L1006-1205)
- Brief: Define class `BaseDownloader`. Execute `__init__`. Execute `matches_url`. Execute `probe_html`. Execute `run`. Execute `_toc_tree_from_html`. Execute `post_process`. Execute `_verify_toc_consistency`. Execute `_verify_toc_depth`. Execute `get_max_depth`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `__init__`. from_url Input argument for `__init__`. out_dir Input argument for `__init__`. session Input argument for `__init__`. logger Input argument for `__init__`. limit Input argument for `__init__`. toc_only Input argument for `__init__`. disable_numbering Input argument for `__init__`. cls Input argument for `matches_url`. url Input argument for `matches_url`. cls Input argument for `probe_html`. url Input argument for `probe_html`. html Input argument for `probe_html`. self Input argument for `run`. self Input argument for `_toc_tree_from_html`. toc_html Input argument for `_toc_tree_from_html`. self Input argument for `post_process`. self Input argument for `_verify_toc_consistency`. self Input argument for `_verify_toc_depth`. ul Input argument for `get_max_depth`. current_depth Input argument for `get_max_depth`.
- Return: Any Return value of `__init__`. bool Return value of `matches_url`. bool Return value of `probe_html`. None Return value of `run`. List[TocNode] Return value of `_toc_tree_from_html`. None Return value of `post_process`. None Return value of `_verify_toc_consistency`. None Return value of `_verify_toc_depth`. Any Return value of `get_max_depth`.
- fn `def __init__(` `priv` (L1013-1021)
- fn `def matches_url(cls, url: str) -> bool` (L1066-1075)
  - Brief: Execute `matches_url`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `matches_url`. url Input argument for `matches_url`.
  - Return: bool Return value of `matches_url`.
- fn `def probe_html(cls, url: str, html: str) -> bool` (L1077-1087)
  - Brief: Execute `probe_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `probe_html`. url Input argument for `probe_html`. html Input argument for `probe_html`.
  - Return: bool Return value of `probe_html`.
- fn `def run(self) -> None` (L1088-1096)
  - Brief: Execute `run`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `run`.
  - Return: None Return value of `run`.
- fn `def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]` `priv` (L1097-1106)
  - Brief: Execute `_toc_tree_from_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_toc_tree_from_html`. toc_html Input argument for `_toc_tree_from_html`.
  - Return: List[TocNode] Return value of `_toc_tree_from_html`.
- fn `def post_process(self) -> None` (L1107-1121)
  - Brief: Execute `post_process`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `post_process`.
  - Return: None Return value of `post_process`.
- fn `def _verify_toc_consistency(self) -> None` `priv` (L1122-1173)
  - Brief: Execute `_verify_toc_consistency`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_verify_toc_consistency`.
  - Return: None Return value of `_verify_toc_consistency`.
- fn `def get_max_depth(ul, current_depth=0)` (L1187-1203)
  - Brief: Execute `get_max_depth`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: ul Input argument for `get_max_depth`. current_depth Input argument for `get_max_depth`.
  - Return: Any Return value of `get_max_depth`.

### fn `def _verify_toc_depth(self) -> None` `priv` (L1174-1213)
- Brief: Execute `_verify_toc_depth`. Execute `get_max_depth`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_verify_toc_depth`. ul Input argument for `get_max_depth`. current_depth Input argument for `get_max_depth`.
- Return: None Return value of `_verify_toc_depth`. Any Return value of `get_max_depth`.

### fn `def _prune_toc_and_clean_headings(self) -> None` `priv` (L1214-1321)
- Brief: Execute `_prune_toc_and_clean_headings`. Execute `href_fragment_id`. Execute `prune_ul`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_prune_toc_and_clean_headings`. href Input argument for `href_fragment_id`. ul Input argument for `prune_ul`. depth Input argument for `prune_ul`.
- Return: None Return value of `_prune_toc_and_clean_headings`. str Return value of `href_fragment_id`. Any Return value of `prune_ul`.

### fn `def href_fragment_id(href: str) -> str` (L1225-1237)
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: href Input argument for `href_fragment_id`.
- Return: str Return value of `href_fragment_id`.

### fn `def prune_ul(ul, depth)` (L1249-1269)
- Brief: Execute `prune_ul`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: ul Input argument for `prune_ul`. depth Input argument for `prune_ul`.
- Return: Any Return value of `prune_ul`.

### fn `def _deduplicate_toc_entries(self) -> None` `priv` (L1322-1390)
- Brief: Execute `_deduplicate_toc_entries`. Execute `href_fragment_id`. Execute `process_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_deduplicate_toc_entries`. href Input argument for `href_fragment_id`. nodes Input argument for `process_nodes`. seen Input argument for `process_nodes`.
- Return: None Return value of `_deduplicate_toc_entries`. str Return value of `href_fragment_id`. List[TocNode] Return value of `process_nodes`.

### fn `def href_fragment_id(href: str) -> str` (L1335-1347)
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: href Input argument for `href_fragment_id`.
- Return: str Return value of `href_fragment_id`.

### fn `def process_nodes(nodes: List[TocNode], seen: Set[str]) -> List[TocNode]` (L1354-1382)
- Brief: Execute `process_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `process_nodes`. seen Input argument for `process_nodes`.
- Return: List[TocNode] Return value of `process_nodes`.

### fn `def _enforce_toc_headings(self) -> None` `priv` (L1391-1509)
- Brief: Execute `_enforce_toc_headings`. Execute `href_fragment_id`. Execute `clamp_heading_level`. Execute `find_referenced_container_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_enforce_toc_headings`. href Input argument for `href_fragment_id`. depth Input argument for `clamp_heading_level`. h Input argument for `find_referenced_container_id`.
- Return: None Return value of `_enforce_toc_headings`. str Return value of `href_fragment_id`. int Return value of `clamp_heading_level`. str Return value of `find_referenced_container_id`.

### fn `def href_fragment_id(href: str) -> str` (L1406-1418)
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: href Input argument for `href_fragment_id`.
- Return: str Return value of `href_fragment_id`.

### fn `def clamp_heading_level(depth: int) -> int` (L1430-1446)
- Brief: Execute `clamp_heading_level`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: depth Input argument for `clamp_heading_level`.
- Return: int Return value of `clamp_heading_level`.

### fn `def find_referenced_container_id(h) -> str` (L1447-1464)
- Brief: Execute `find_referenced_container_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: h Input argument for `find_referenced_container_id`.
- Return: str Return value of `find_referenced_container_id`.

### fn `def _test_toc_headings(self) -> None` `priv` (L1510-1705)
- Brief: Execute `_test_toc_headings`. Execute `href_fragment_id`. Execute `clamp_heading_level`. Execute `summarize`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_test_toc_headings`. href Input argument for `href_fragment_id`. depth Input argument for `clamp_heading_level`. items Input argument for `summarize`.
- Return: None Return value of `_test_toc_headings`. str Return value of `href_fragment_id`. int Return value of `clamp_heading_level`. str Return value of `summarize`.

### fn `def href_fragment_id(href: str) -> str` (L1526-1538)
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: href Input argument for `href_fragment_id`.
- Return: str Return value of `href_fragment_id`.

### fn `def clamp_heading_level(depth: int) -> int` (L1539-1551)
- Brief: Execute `clamp_heading_level`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: depth Input argument for `clamp_heading_level`.
- Return: int Return value of `clamp_heading_level`.

### fn `def summarize(items: List[str]) -> str` (L1669-1682)
- Brief: Execute `summarize`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: items Input argument for `summarize`.
- Return: str Return value of `summarize`.

### fn `def fix_heading_ref_position(self) -> None` (L1706-1846)
- Brief: Execute `fix_heading_ref_position`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `fix_heading_ref_position`.
- Return: None Return value of `fix_heading_ref_position`.

### fn `def fix_heading_numbering(self) -> None` (L1847-1985)
- Brief: Execute `fix_heading_numbering`. Execute `normalize_ws`. Execute `strip_numbering_prefix`. Execute `set_flat_text`. Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `fix_heading_numbering`. text Input argument for `normalize_ws`. text Input argument for `strip_numbering_prefix`. tag Input argument for `set_flat_text`. text Input argument for `set_flat_text`. href Input argument for `href_fragment_id`.
- Return: None Return value of `fix_heading_numbering`. str Return value of `normalize_ws`. str Return value of `strip_numbering_prefix`. None Return value of `set_flat_text`. str Return value of `href_fragment_id`.

### fn `def normalize_ws(text: str) -> str` (L1866-1874)
- Brief: Execute `normalize_ws`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: text Input argument for `normalize_ws`.
- Return: str Return value of `normalize_ws`.

### fn `def strip_numbering_prefix(text: str) -> str` (L1875-1883)
- Brief: Execute `strip_numbering_prefix`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: text Input argument for `strip_numbering_prefix`.
- Return: str Return value of `strip_numbering_prefix`.

### fn `def set_flat_text(tag, text: str) -> None` (L1884-1894)
- Brief: Execute `set_flat_text`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: tag Input argument for `set_flat_text`. text Input argument for `set_flat_text`.
- Return: None Return value of `set_flat_text`.

### fn `def href_fragment_id(href: str) -> str` (L1916-1928)
- Brief: Execute `href_fragment_id`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: href Input argument for `href_fragment_id`.
- Return: str Return value of `href_fragment_id`.

### fn `def _clean_document_style(self) -> None` `priv` (L1986-2006)
- Brief: Execute `_clean_document_style`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_clean_document_style`.
- Return: None Return value of `_clean_document_style`.

### fn `def _add_document_style(self) -> None` `priv` (L2007-2038)
- Brief: Execute `_add_document_style`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_add_document_style`.
- Return: None Return value of `_add_document_style`.

### fn `def _normalize_document_links(self) -> None` `priv` (L2053-2067)
- Brief: Execute `_normalize_document_links`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_normalize_document_links`.
- Return: None Return value of `_normalize_document_links`.

### fn `def _remove_unused_images(self) -> None` `priv` (L2068-2109)
- Brief: Execute `_remove_unused_images`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_remove_unused_images`.
- Return: None Return value of `_remove_unused_images`.

### fn `def _remove_unused_assets(self) -> None` `priv` (L2110-2144)
- Brief: Execute `_remove_unused_assets`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_remove_unused_assets`.
- Return: None Return value of `_remove_unused_assets`.

### fn `def _normalize_image_position(self) -> None` `priv` (L2145-2204)
- Brief: Execute `_normalize_image_position`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_normalize_image_position`.
- Return: None Return value of `_normalize_image_position`.

### fn `def _clean_assets_tree(self) -> None` `priv` (L2205-2227)
- Brief: Execute `_clean_assets_tree`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_clean_assets_tree`.
- Return: None Return value of `_clean_assets_tree`.

### fn `def _remove_empty_assets_root(self) -> None` `priv` (L2228-2266)
- Brief: Execute `_remove_empty_assets_root`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_remove_empty_assets_root`.
- Return: None Return value of `_remove_empty_assets_root`.

### class `class DownloaderRegistry` (L2267-2324)
- Brief: Define class `DownloaderRegistry`. Execute `__init__`. Execute `register`. Execute `detect`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `__init__`. self Input argument for `register`. downloader_cls Input argument for `register`. self Input argument for `detect`. url Input argument for `detect`. session Input argument for `detect`.
- Return: Any Return value of `__init__`. None Return value of `register`. type[BaseDownloader] Return value of `detect`.
- fn `def __init__(self)` `priv` (L2272-2280)
  - Brief: Define class `DownloaderRegistry`. Execute `__init__`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def register(self, downloader_cls: type[BaseDownloader]) -> None` (L2281-2290)
  - Brief: Execute `register`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `register`. downloader_cls Input argument for `register`.
  - Return: None Return value of `register`.
- fn `def detect(self, url: str, session: requests.Session) -> type[BaseDownloader]` (L2291-2324)
  - Brief: Execute `detect`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `detect`. url Input argument for `detect`. session Input argument for `detect`.
  - Return: type[BaseDownloader] Return value of `detect`.

### fn `def guess_ext_from_content_type(ct: str) -> str` (L2330-2349)
- Brief: Execute `guess_ext_from_content_type`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: ct Input argument for `guess_ext_from_content_type`.
- Return: str Return value of `guess_ext_from_content_type`.

### class `class NetworkImageRecorder` (L2350-2412)
- Brief: Define class `NetworkImageRecorder`. Execute `__init__`. Execute `attach`. Execute `on_response`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `__init__`. out_dir Input argument for `__init__`. self Input argument for `attach`. page Input argument for `attach`. resp Input argument for `on_response`.
- Return: Any Return value of `__init__`. Any Return value of `attach`. Any Return value of `on_response`.
- fn `def __init__(self, out_dir: Path)` `priv` (L2356-2367)
  - Brief: Define class `NetworkImageRecorder`. Execute `__init__`.
  - Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`. out_dir Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def attach(self, page)` (L2368-2412)
  - Brief: Execute `attach`. Execute `on_response`.
  - Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `attach`. page Input argument for `attach`. resp Input argument for `on_response`.
  - Return: Any Return value of `attach`. Any Return value of `on_response`.
- fn `def on_response(resp)` (L2376-2409)
  - Brief: Execute `attach`. Execute `on_response`.
  - Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `attach`.
... resp Input argument for `on_response`.
  - Return: Any Return value of `on_response`.

### class `class DocumentViewerDownloader(BaseDownloader)` : BaseDownloader (L2413-2612)
- Brief: Define class `DocumentViewerDownloader`. Execute `matches_url`. Execute `probe_html`. Execute `_pick_best_outerhtml`. Execute `_expand_full_toc`. Execute `_scroll_toc_container`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: cls Input argument for `matches_url`. url Input argument for `matches_url`. cls Input argument for `probe_html`. url Input argument for `probe_html`. html Input argument for `probe_html`. self Input argument for `_pick_best_outerhtml`. page Input argument for `_pick_best_outerhtml`. selectors Input argument for `_pick_best_outerhtml`. self Input argument for `_expand_full_toc`. page Input argument for `_expand_full_toc`. max_rounds Input argument for `_expand_full_toc`. settle_ms Input argument for `_expand_full_toc`. self Input argument for `_scroll_toc_container`. page Input argument for `_scroll_toc_container`. step_px Input argument for `_scroll_toc_container`. max_rounds Input argument for `_scroll_toc_container`. settle_ms Input argument for `_scroll_toc_container`.
- Return: bool Return value of `matches_url`. bool Return value of `probe_html`. Optional[str] Return value of `_pick_best_outerhtml`. None Return value of `_expand_full_toc`. None Return value of `_scroll_toc_container`.
- var `TOC_SELECTORS = [` (L2420)
- var `CONTENT_SELECTORS = [` (L2429)
- var `TOC_SCROLL_SELECTORS = [` (L2442)
- fn `def matches_url(cls, url: str) -> bool` (L2451-2461)
  - Brief: Execute `matches_url`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `matches_url`. url Input argument for `matches_url`.
  - Return: bool Return value of `matches_url`.
- fn `def probe_html(cls, url: str, html: str) -> bool` (L2463-2474)
  - Brief: Execute `probe_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `probe_html`. url Input argument for `probe_html`. html Input argument for `probe_html`.
  - Return: bool Return value of `probe_html`.
- fn `def _pick_best_outerhtml(self, page, selectors: List[str]) -> Optional[str]` `priv` (L2475-2506)
  - Brief: Execute `_pick_best_outerhtml`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_pick_best_outerhtml`. page Input argument for `_pick_best_outerhtml`. selectors Input argument for `_pick_best_outerhtml`.
  - Return: Optional[str] Return value of `_pick_best_outerhtml`.
- fn `def _expand_full_toc(` `priv` (L2507-2508)
- fn `def _scroll_toc_container(` `priv` (L2568-2569)

### fn `def _find_scroll_container(self, page)` `priv` (L2626-2691)
- Brief: Execute `_find_scroll_container`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_find_scroll_container`. page Input argument for `_find_scroll_container`.
- Return: Any Return value of `_find_scroll_container`.

### fn `def _auto_scroll_element(` `priv` (L2692-2700)

### fn `def _auto_scroll(` `priv` (L2773-2779)

### fn `def _collect_cards_from_container(` `priv` (L2849-2856)

### fn `def _best_card_for_fragment(` `priv` (L2934-2935)

### fn `def score_value(val: str) -> int` (L2954-2974)
- Brief: Execute `score_value`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: val Input argument for `score_value`.
- Return: int Return value of `score_value`.

### fn `def _fragment_matches_url(self, fragment: str, data_url: str) -> bool` `priv` (L2991-3010)
- Brief: Execute `_fragment_matches_url`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_fragment_matches_url`. fragment Input argument for `_fragment_matches_url`. data_url Input argument for `_fragment_matches_url`.
- Return: bool Return value of `_fragment_matches_url`.

### fn `def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]` `priv` (L3011-3020)
- Brief: Execute `_toc_tree_from_html`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_toc_tree_from_html`. toc_html Input argument for `_toc_tree_from_html`.
- Return: List[TocNode] Return value of `_toc_tree_from_html`.

### fn `def _iter_nodes(nodes: List[TocNode]) -> Iterable[TocNode]` `priv` `@staticmethod` (L3022-3032)
- Brief: Execute `_iter_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_iter_nodes`.
- Return: Iterable[TocNode] Return value of `_iter_nodes`.

### fn `def _first_numeric_index(nodes: List[TocNode]) -> Optional[int]` `priv` `@staticmethod` (L3034-3046)
- Brief: Execute `_first_numeric_index`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_first_numeric_index`.
- Return: Optional[int] Return value of `_first_numeric_index`.

### fn `def _trim_toc_nodes(nodes: List[TocNode]) -> List[TocNode]` `priv` `@staticmethod` (L3048-3069)
- Brief: Execute `_trim_toc_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_trim_toc_nodes`.
- Return: List[TocNode] Return value of `_trim_toc_nodes`.

### fn `def _limit_toc_nodes(` `priv` `@staticmethod` (L3071-3072)

### fn `def _limit_by_reading_order(` `priv` `@staticmethod` (L3084-3085)

### fn `def _prune_toc_to_allowed(` `priv` `@staticmethod` (L3123-3124)

### fn `def _first_toc_entry_title(nodes: List[TocNode]) -> Optional[str]` `priv` `@staticmethod` (L3147-3159)
- Brief: Execute `_first_toc_entry_title`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_first_toc_entry_title`.
- Return: Optional[str] Return value of `_first_toc_entry_title`.

### fn `def _is_important_notice_label(title: Optional[str]) -> bool` `priv` `@staticmethod` (L3161-3170)
- Brief: Execute `_is_important_notice_label`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: title Input argument for `_is_important_notice_label`.
- Return: bool Return value of `_is_important_notice_label`.

### fn `def _is_important_notice_section(section_html: str) -> bool` `priv` `@staticmethod` (L3172-3187)
- Brief: Execute `_is_important_notice_section`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: section_html Input argument for `_is_important_notice_section`.
- Return: bool Return value of `_is_important_notice_section`.

### fn `def _select_section_nodes(nodes: List[TocNode]) -> List[TocNode]` `priv` `@staticmethod` (L3189-3214)
- Brief: Execute `_select_section_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_select_section_nodes`.
- Return: List[TocNode] Return value of `_select_section_nodes`.

### fn `def _dedup_toc_nodes_by_href(self, nodes: List[TocNode]) -> List[TocNode]` `priv` (L3215-3253)
- Brief: Execute `_dedup_toc_nodes_by_href`. Execute `dedup_list`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_dedup_toc_nodes_by_href`. nodes Input argument for `_dedup_toc_nodes_by_href`. items Input argument for `dedup_list`.
- Return: List[TocNode] Return value of `_dedup_toc_nodes_by_href`. List[TocNode] Return value of `dedup_list`.

### fn `def dedup_list(items: List[TocNode]) -> List[TocNode]` (L3224-3251)
- Brief: Execute `_dedup_toc_nodes_by_href`. Execute `dedup_list`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_dedup_toc_nodes_by_href`.
... items Input argument for `dedup_list`.
- Return: List[TocNode] Return value of `dedup_list`.

### fn `def _is_section_scrollable(self, page, viewport_multiplier: float = 2.0) -> bool` `priv` (L3254-3276)
- Brief: Execute `_is_section_scrollable`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_is_section_scrollable`. page Input argument for `_is_section_scrollable`. viewport_multiplier Input argument for `_is_section_scrollable`.
- Return: bool Return value of `_is_section_scrollable`.

### fn `def _remove_toc_elements(self, soup: BeautifulSoup) -> None` `priv` (L3277-3313)
- Brief: Execute `_remove_toc_elements`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_remove_toc_elements`. soup Input argument for `_remove_toc_elements`.
- Return: None Return value of `_remove_toc_elements`.

### fn `def _convert_doxygen_definition_lists(self, soup: BeautifulSoup) -> None` `priv` (L3314-3380)
- Brief: Execute `_convert_doxygen_definition_lists`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_convert_doxygen_definition_lists`. soup Input argument for `_convert_doxygen_definition_lists`.
- Return: None Return value of `_convert_doxygen_definition_lists`.

### fn `def _extract_fragment_only(` `priv` (L3381-3382)

### fn `def score_value(val: str) -> int` (L3401-3424)
- Brief: Execute `score_value`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: val Input argument for `score_value`.
- Return: int Return value of `score_value`.

### fn `def pick_best_section(elements)` (L3425-3448)
- Brief: Execute `pick_best_section`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: elements Input argument for `pick_best_section`.
- Return: Any Return value of `pick_best_section`.

### fn `def matches_fragment(el) -> bool` (L3459-3478)
- Brief: Execute `matches_fragment`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: el Input argument for `matches_fragment`.
- Return: bool Return value of `matches_fragment`.

### fn `def _wait_for_fragment(self, page, fragment: str, timeout_ms: int = 8000) -> bool` `priv` (L3506-3558)
- Brief: Execute `_wait_for_fragment`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_wait_for_fragment`. page Input argument for `_wait_for_fragment`. fragment Input argument for `_wait_for_fragment`. timeout_ms Input argument for `_wait_for_fragment`.
- Return: bool Return value of `_wait_for_fragment`.

### fn `def _click_toc_link(self, page, fragment: str) -> bool` `priv` (L3559-3587)
- Brief: Execute `_click_toc_link`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_click_toc_link`. page Input argument for `_click_toc_link`. fragment Input argument for `_click_toc_link`.
- Return: bool Return value of `_click_toc_link`.

### fn `def run(self) -> None` (L3588-3787)
- Brief: Execute `run`. Execute `make_anchor`. Execute `normalize_text`. Execute `strip_ti_disclaimer`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `run`. raw_fragment Input argument for `make_anchor`. title Input argument for `make_anchor`. used Input argument for `make_anchor`. value Input argument for `normalize_text`. section_html Input argument for `strip_ti_disclaimer`.
- Return: None Return value of `run`. str Return value of `make_anchor`. str Return value of `normalize_text`. str Return value of `strip_ti_disclaimer`.

### fn `def make_anchor(raw_fragment: str, title: str, used: Set[str]) -> str` (L3598-3616)
- Brief: Execute `make_anchor`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: raw_fragment Input argument for `make_anchor`. title Input argument for `make_anchor`. used Input argument for `make_anchor`.
- Return: str Return value of `make_anchor`.

### fn `def normalize_text(value: str) -> str` (L3617-3627)
- Brief: Execute `normalize_text`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: value Input argument for `normalize_text`.
- Return: str Return value of `normalize_text`.

### fn `def strip_ti_disclaimer(section_html: str) -> str` (L3628-3658)
- Brief: Execute `strip_ti_disclaimer`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: section_html Input argument for `strip_ti_disclaimer`.
- Return: str Return value of `strip_ti_disclaimer`.

### class `class DoxygenExportDownloader(BaseDownloader)` : BaseDownloader (L4066-4265)
- Brief: Define class `DoxygenExportDownloader`. Execute `matches_url`. Execute `probe_html`. Execute `_scope`. Execute `_fetch_soup`. Execute `_is_in_scope`. Execute `_page_title`. Execute `_document_title`. Execute `_extract_main`. Execute `_remove_toc_elements`. Execute `_links_to_html_pages`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: cls Input argument for `matches_url`. url Input argument for `matches_url`. cls Input argument for `probe_html`. url Input argument for `probe_html`. html Input argument for `probe_html`. self Input argument for `_scope`. self Input argument for `_fetch_soup`. url Input argument for `_fetch_soup`. self Input argument for `_is_in_scope`. url Input argument for `_is_in_scope`. host Input argument for `_is_in_scope`. scope_dir_url Input argument for `_is_in_scope`. self Input argument for `_page_title`. soup Input argument for `_page_title`. self Input argument for `_document_title`. soup Input argument for `_document_title`. self Input argument for `_extract_main`. soup Input argument for `_extract_main`. self Input argument for `_remove_toc_elements`. soup Input argument for `_remove_toc_elements`. self Input argument for `_links_to_html_pages`. soup Input argument for `_links_to_html_pages`. page_url Input argument for `_links_to_html_pages`. host Input argument for `_links_to_html_pages`. scope_dir_url Input argument for `_links_to_html_pages`.
- Return: bool Return value of `matches_url`. bool Return value of `probe_html`. Tuple[str, str] Return value of `_scope`. BeautifulSoup Return value of `_fetch_soup`. bool Return value of `_is_in_scope`. str Return value of `_page_title`. str Return value of `_document_title`. BeautifulSoup Return value of `_extract_main`. None Return value of `_remove_toc_elements`. Set[str] Return value of `_links_to_html_pages`.
- fn `def matches_url(cls, url: str) -> bool` (L4074-4087)
  - Brief: Execute `matches_url`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `matches_url`. url Input argument for `matches_url`.
  - Return: bool Return value of `matches_url`.
- fn `def probe_html(cls, url: str, html: str) -> bool` (L4089-4100)
  - Brief: Execute `probe_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `probe_html`. url Input argument for `probe_html`. html Input argument for `probe_html`.
  - Return: bool Return value of `probe_html`.
- fn `def _scope(self) -> Tuple[str, str]` `priv` (L4101-4114)
  - Brief: Execute `_scope`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_scope`.
  - Return: Tuple[str, str] Return value of `_scope`.
- fn `def _fetch_soup(self, url: str) -> BeautifulSoup` `priv` (L4115-4126)
  - Brief: Execute `_fetch_soup`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_fetch_soup`. url Input argument for `_fetch_soup`.
  - Return: BeautifulSoup Return value of `_fetch_soup`.
- fn `def _is_in_scope(self, url: str, host: str, scope_dir_url: str) -> bool` `priv` (L4127-4143)
  - Brief: Execute `_is_in_scope`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_is_in_scope`. url Input argument for `_is_in_scope`. host Input argument for `_is_in_scope`. scope_dir_url Input argument for `_is_in_scope`.
  - Return: bool Return value of `_is_in_scope`.
- fn `def _page_title(self, soup: BeautifulSoup) -> str` `priv` (L4144-4159)
  - Brief: Execute `_page_title`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_page_title`. soup Input argument for `_page_title`.
  - Return: str Return value of `_page_title`.
- fn `def _document_title(self, soup: BeautifulSoup) -> str` `priv` (L4160-4191)
  - Brief: Execute `_document_title`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_document_title`. soup Input argument for `_document_title`.
  - Return: str Return value of `_document_title`.
- fn `def _extract_main(self, soup: BeautifulSoup) -> BeautifulSoup` `priv` (L4192-4215)
  - Brief: Execute `_extract_main`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_extract_main`. soup Input argument for `_extract_main`.
  - Return: BeautifulSoup Return value of `_extract_main`.
- fn `def _remove_toc_elements(self, soup: BeautifulSoup) -> None` `priv` (L4216-4242)
  - Brief: Execute `_remove_toc_elements`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_remove_toc_elements`. soup Input argument for `_remove_toc_elements`.
  - Return: None Return value of `_remove_toc_elements`.
- fn `def _links_to_html_pages(` `priv` (L4243-4244)

### fn `def _expand_nav_tree(self, page) -> None` `priv` (L4269-4305)
- Brief: Execute `_expand_nav_tree`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_expand_nav_tree`. page Input argument for `_expand_nav_tree`.
- Return: None Return value of `_expand_nav_tree`.

### fn `def _expand_nav_tree_full(self, page) -> None` `priv` (L4306-4505)
- Brief: Execute `_expand_nav_tree_full`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_expand_nav_tree_full`. page Input argument for `_expand_nav_tree_full`.
- Return: None Return value of `_expand_nav_tree_full`.

### fn `def _expand_nav_tree_limited(self, page, limit: int) -> None` `priv` (L4513-4622)
- Brief: Execute `_expand_nav_tree_limited`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_expand_nav_tree_limited`. page Input argument for `_expand_nav_tree_limited`. limit Input argument for `_expand_nav_tree_limited`.
- Return: None Return value of `_expand_nav_tree_limited`.

### fn `def _cleanup_nav_tree_styles(self, page) -> None` `priv` (L4623-4654)
- Brief: Execute `_cleanup_nav_tree_styles`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_cleanup_nav_tree_styles`. page Input argument for `_cleanup_nav_tree_styles`.
- Return: None Return value of `_cleanup_nav_tree_styles`.

### fn `def _fetch_nav_tree_with_playwright(self) -> Tuple[str, str]` `priv` (L4655-4744)
- Brief: Execute `_fetch_nav_tree_with_playwright`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_fetch_nav_tree_with_playwright`.
- Return: Tuple[str, str] Return value of `_fetch_nav_tree_with_playwright`.

### fn `def _nav_link_href(self, link, base_url: str) -> str` `priv` (L4745-4770)
- Brief: Execute `_nav_link_href`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_nav_link_href`. link Input argument for `_nav_link_href`. base_url Input argument for `_nav_link_href`.
- Return: str Return value of `_nav_link_href`.

### fn `def _toc_tree_from_html(self, toc_html: str) -> List[TocNode]` `priv` (L4771-4780)
- Brief: Execute `_toc_tree_from_html`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_toc_tree_from_html`. toc_html Input argument for `_toc_tree_from_html`.
- Return: List[TocNode] Return value of `_toc_tree_from_html`.

### fn `def _toc_nodes_from_nav_html(self, nav_html: str) -> List[TocNode]` `priv` (L4781-4823)
- Brief: Execute `_toc_nodes_from_nav_html`. Execute `parse_ul`.
- Details: Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_toc_nodes_from_nav_html`. nav_html Input argument for `_toc_nodes_from_nav_html`. ul Input argument for `parse_ul`.
- Return: List[TocNode] Return value of `_toc_nodes_from_nav_html`. List[TocNode] Return value of `parse_ul`.

### fn `def parse_ul(ul) -> List[TocNode]` (L4794-4818)
- Brief: Execute `parse_ul`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: ul Input argument for `parse_ul`.
- Return: List[TocNode] Return value of `parse_ul`.

### fn `def _iter_toc_nodes(nodes: List[TocNode]) -> Iterable[TocNode]` `priv` `@staticmethod` (L4825-4835)
- Brief: Execute `_iter_toc_nodes`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: nodes Input argument for `_iter_toc_nodes`.
- Return: Iterable[TocNode] Return value of `_iter_toc_nodes`.

### fn `def _select_main_container(self, soup: BeautifulSoup)` `priv` (L4836-4857)
- Brief: Execute `_select_main_container`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_select_main_container`. soup Input argument for `_select_main_container`.
- Return: Any Return value of `_select_main_container`.

### fn `def _find_fragment_anchor(self, main, fragment: str)` `priv` (L4858-4885)
- Brief: Execute `_find_fragment_anchor`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_find_fragment_anchor`. main Input argument for `_find_fragment_anchor`. fragment Input argument for `_find_fragment_anchor`.
- Return: Any Return value of `_find_fragment_anchor`.

### fn `def _normalize_heading_text(value: str) -> str` `priv` `@staticmethod` (L4887-4895)
- Brief: Execute `_normalize_heading_text`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: value Input argument for `_normalize_heading_text`.
- Return: str Return value of `_normalize_heading_text`.

### fn `def _strip_duplicate_section_title(` `priv` (L4896-4897)

### fn `def _extract_section_html(` `priv` (L4940-4941)

### fn `def direct_child(el)` (L4969-4980)
- Brief: Execute `direct_child`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: el Input argument for `direct_child`.
- Return: Any Return value of `direct_child`.

### fn `def _build_toc(self, doc: BeautifulSoup) -> List[TocNode]` `priv` (L5004-5069)
- Brief: Execute `_build_toc`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `_build_toc`. doc Input argument for `_build_toc`.
- Return: List[TocNode] Return value of `_build_toc`.

### fn `def run(self) -> None` (L5070-5269)
- Brief: Execute `run`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `run`.
- Return: None Return value of `run`.

- var `MAX_PAGES = 250` (L5256)
### class `class ResourceExplorerModule` (L5434-5466)
- Brief: Define class `ResourceExplorerModule`. Execute `select`. Execute `run`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `select`. url Input argument for `select`. html Input argument for `select`. soup Input argument for `select`. self Input argument for `run`. downloader Input argument for `run`. selection Input argument for `run`.
- Return: Optional[Dict[str, str]] Return value of `select`. None Return value of `run`.
- fn `def select(` (L5441-5442)
- fn `def run(self, downloader: "ResourceExplorerDownloader", selection: Dict[str, str]) -> None` (L5455-5466)
  - Brief: Execute `run`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `run`. downloader Input argument for `run`. selection Input argument for `run`.
  - Return: None Return value of `run`.

### class `class RMModuleDoxigen(ResourceExplorerModule)` : ResourceExplorerModule (L5467-5524)
- Brief: Define class `RMModuleDoxigen`. Execute `select`. Execute `run`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `select`. url Input argument for `select`. html Input argument for `select`. soup Input argument for `select`. self Input argument for `run`. downloader Input argument for `run`. selection Input argument for `run`.
- Return: Optional[Dict[str, str]] Return value of `select`. None Return value of `run`.
- fn `def select(` (L5476-5477)
- fn `def run(self, downloader: "ResourceExplorerDownloader", selection: Dict[str, str]) -> None` (L5501-5524)
  - Brief: Execute `run`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `run`. downloader Input argument for `run`. selection Input argument for `run`.
  - Return: None Return value of `run`.

### class `class ResourceExplorerDownloader(BaseDownloader)` : BaseDownloader (L5525-5657)
- Brief: Define class `ResourceExplorerDownloader`. Execute `__init__`. Execute `matches_url`. Execute `probe_html`. Execute `_select_module`. Execute `_render_with_playwright`. Execute `run`.
- Details: Encapsulates behavior used by downloader orchestration and processing pipeline. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics. Implements deterministic control flow as defined by module runtime semantics.
- Param: self Input argument for `__init__`. *args Input argument for `__init__`. **kwargs Input argument for `__init__`. cls Input argument for `matches_url`. url Input argument for `matches_url`. cls Input argument for `probe_html`. url Input argument for `probe_html`. html Input argument for `probe_html`. self Input argument for `_select_module`. html Input argument for `_select_module`. soup Input argument for `_select_module`. self Input argument for `_render_with_playwright`. self Input argument for `run`.
- Return: Any Return value of `__init__`. bool Return value of `matches_url`. bool Return value of `probe_html`. Optional[Tuple[ResourceExplorerModule, Dict[str, str]]] Return value of `_select_module`. str Return value of `_render_with_playwright`. None Return value of `run`.
- fn `def __init__(self, *args, **kwargs)` `priv` (L5532-5543)
  - Brief: Execute `__init__`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `__init__`. *args Input argument for `__init__`. **kwargs Input argument for `__init__`.
  - Return: Any Return value of `__init__`.
- fn `def matches_url(cls, url: str) -> bool` (L5545-5555)
  - Brief: Execute `matches_url`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `matches_url`. url Input argument for `matches_url`.
  - Return: bool Return value of `matches_url`.
- fn `def probe_html(cls, url: str, html: str) -> bool` (L5557-5567)
  - Brief: Execute `probe_html`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: cls Input argument for `probe_html`. url Input argument for `probe_html`. html Input argument for `probe_html`.
  - Return: bool Return value of `probe_html`.
- fn `def _select_module(` `priv` (L5568-5569)
- fn `def _render_with_playwright(self) -> str` `priv` (L5585-5622)
  - Brief: Execute `_render_with_playwright`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `_render_with_playwright`.
  - Return: str Return value of `_render_with_playwright`.
- fn `def run(self) -> None` (L5623-5657)
  - Brief: Execute `run`.
  - Details: Implements deterministic control flow as defined by module runtime semantics.
  - Param: self Input argument for `run`.
  - Return: None Return value of `run`.

### fn `def build_arg_parser() -> argparse.ArgumentParser` (L5663-5708)
- Brief: Execute `build_arg_parser`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Return: argparse.ArgumentParser Return value of `build_arg_parser`.

### fn `def print_strict_help(program: str, version: str, parser: argparse.ArgumentParser) -> None` (L5709-5758)
- Brief: Execute `print_strict_help`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Param: program Input argument for `print_strict_help`. version Input argument for `print_strict_help`. parser Input argument for `print_strict_help`.
- Return: None Return value of `print_strict_help`.

### fn `def main() -> int` (L5759-5810)
- Brief: Execute `main`.
- Details: Implements deterministic control flow as defined by module runtime semantics.
- Return: int Return value of `main`.

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`GITHUB_API_TIMEOUT_S`|var|pub|37||
|`_parse_version_tuple`|fn|priv|40-59|def _parse_version_tuple(v: str) -> Optional[Tuple[int, ....|
|`_is_version_newer`|fn|priv|60-77|def _is_version_newer(latest: str, current: str) -> bool|
|`_get_latest_version_from_github`|fn|priv|78-107|def _get_latest_version_from_github(owner: str, repo: str...|
|`check_for_new_version`|fn|pub|108-126|def check_for_new_version(program: str, current_version: ...|
|`safe_filename`|fn|pub|132-144|def safe_filename(path: str) -> str|
|`positive_int`|fn|pub|145-160|def positive_int(value: str) -> int|
|`is_http_url`|fn|pub|161-174|def is_http_url(s: str) -> bool|
|`normalize_url`|fn|pub|175-190|def normalize_url(u: str, base: str) -> str|
|`ensure_parent`|fn|pub|191-200|def ensure_parent(p: Path) -> None|
|`local_path_for_url`|fn|pub|201-223|def local_path_for_url(asset_url: str, out_dir: Path) -> ...|
|`download_one`|fn|pub|224-225|def download_one(|
|`escape_html`|fn|pub|249-264|def escape_html(s: str) -> str|
|`TocNode`|class|pub|266-275|class TocNode|
|`limit_toc_nodes`|fn|pub|276-308|def limit_toc_nodes(nodes: List[TocNode], max_entries: Op...|
|`trim_list`|fn|pub|289-305|def trim_list(items: List[TocNode]) -> List[TocNode]|
|`ensure_heading_ids`|fn|pub|309-333|def ensure_heading_ids(soup: BeautifulSoup) -> None|
|`strip_styles`|fn|pub|334-351|def strip_styles(soup: BeautifulSoup) -> None|
|`toc_from_headings`|fn|pub|352-379|def toc_from_headings(soup: BeautifulSoup) -> List[TocNode]|
|`toc_from_nav_html`|fn|pub|380-430|def toc_from_nav_html(toc_html: str, base_url: str) -> Li...|
|`parse_list`|fn|pub|390-419|def parse_list(list_el) -> List[TocNode]|
|`nav_outline_from_html`|fn|pub|431-494|def nav_outline_from_html(nav_html: str) -> str|
|`norm_text`|fn|pub|442-451|def norm_text(t: str) -> str|
|`bullet`|fn|pub|452-464|def bullet(depth: int) -> str|
|`walk_ul`|fn|pub|465-488|def walk_ul(ul, depth: int) -> None|
|`ASSET_ATTRS`|var|pub|496||
|`HEADING_TAG_RE`|var|pub|504||
|`Logger`|class|pub|507-568|class Logger|
|`Logger.__init__`|fn|priv|513-524|def __init__(self, verbose: bool = False, debug: bool = F...|
|`Logger.info`|fn|pub|525-534|def info(self, msg: str) -> None|
|`Logger.verbose`|fn|pub|535-545|def verbose(self, msg: str) -> None|
|`Logger.debug`|fn|pub|546-556|def debug(self, msg: str) -> None|
|`Logger.check`|fn|pub|557-568|def check(self, msg: str) -> None|
|`UpgradeAction`|class|pub|569-606|class UpgradeAction(argparse.Action)|
|`UpgradeAction.__call__`|fn|priv|574-579|def __call__(|
|`VersionedArgumentParser`|class|pub|607-645|class VersionedArgumentParser(argparse.ArgumentParser)|
|`VersionedArgumentParser.__init__`|fn|priv|613-625|def __init__(self, *args, version: str = "", **kwargs)|
|`VersionedArgumentParser.format_usage`|fn|pub|626-645|def format_usage(self) -> str|
|`iter_asset_urls`|fn|pub|646-684|def iter_asset_urls(soup: BeautifulSoup, page_url: str) -...|
|`rewrite_asset_links_inplace`|fn|pub|685-686|def rewrite_asset_links_inplace(|
|`to_rel`|fn|pub|696-708|def to_rel(u: str) -> str|
|`repl`|fn|pub|732-741|def repl(m)|
|`ALLOWED_EXTERNAL_LINK_SCHEMES`|var|pub|746||
|`normalize_document_links_inplace`|fn|pub|754-879|def normalize_document_links_inplace(soup: BeautifulSoup,...|
|`build_toc_html`|fn|pub|880-883|def build_toc_html(|
|`resolved_href`|fn|pub|893-907|def resolved_href(href: str) -> str|
|`render_nodes`|fn|pub|908-925|def render_nodes(nodes: List[TocNode]) -> str|
|`build_frameset_index`|fn|pub|947-948|def build_frameset_index(|
|`minimal_readable_wrapper`|fn|pub|977-978|def minimal_readable_wrapper(|
|`BaseDownloader`|class|pub|1006-1205|class BaseDownloader|
|`BaseDownloader.__init__`|fn|priv|1013-1021|def __init__(|
|`BaseDownloader.matches_url`|fn|pub|1066-1075|def matches_url(cls, url: str) -> bool|
|`BaseDownloader.probe_html`|fn|pub|1077-1087|def probe_html(cls, url: str, html: str) -> bool|
|`BaseDownloader.run`|fn|pub|1088-1096|def run(self) -> None|
|`BaseDownloader._toc_tree_from_html`|fn|priv|1097-1106|def _toc_tree_from_html(self, toc_html: str) -> List[TocN...|
|`BaseDownloader.post_process`|fn|pub|1107-1121|def post_process(self) -> None|
|`BaseDownloader._verify_toc_consistency`|fn|priv|1122-1173|def _verify_toc_consistency(self) -> None|
|`_verify_toc_depth`|fn|priv|1174-1213|def _verify_toc_depth(self) -> None|
|`BaseDownloader.get_max_depth`|fn|pub|1187-1203|def get_max_depth(ul, current_depth=0)|
|`_prune_toc_and_clean_headings`|fn|priv|1214-1321|def _prune_toc_and_clean_headings(self) -> None|
|`href_fragment_id`|fn|pub|1225-1237|def href_fragment_id(href: str) -> str|
|`prune_ul`|fn|pub|1249-1269|def prune_ul(ul, depth)|
|`_deduplicate_toc_entries`|fn|priv|1322-1390|def _deduplicate_toc_entries(self) -> None|
|`href_fragment_id`|fn|pub|1335-1347|def href_fragment_id(href: str) -> str|
|`process_nodes`|fn|pub|1354-1382|def process_nodes(nodes: List[TocNode], seen: Set[str]) -...|
|`_enforce_toc_headings`|fn|priv|1391-1509|def _enforce_toc_headings(self) -> None|
|`href_fragment_id`|fn|pub|1406-1418|def href_fragment_id(href: str) -> str|
|`clamp_heading_level`|fn|pub|1430-1446|def clamp_heading_level(depth: int) -> int|
|`find_referenced_container_id`|fn|pub|1447-1464|def find_referenced_container_id(h) -> str|
|`_test_toc_headings`|fn|priv|1510-1705|def _test_toc_headings(self) -> None|
|`href_fragment_id`|fn|pub|1526-1538|def href_fragment_id(href: str) -> str|
|`clamp_heading_level`|fn|pub|1539-1551|def clamp_heading_level(depth: int) -> int|
|`summarize`|fn|pub|1669-1682|def summarize(items: List[str]) -> str|
|`fix_heading_ref_position`|fn|pub|1706-1846|def fix_heading_ref_position(self) -> None|
|`fix_heading_numbering`|fn|pub|1847-1985|def fix_heading_numbering(self) -> None|
|`normalize_ws`|fn|pub|1866-1874|def normalize_ws(text: str) -> str|
|`strip_numbering_prefix`|fn|pub|1875-1883|def strip_numbering_prefix(text: str) -> str|
|`set_flat_text`|fn|pub|1884-1894|def set_flat_text(tag, text: str) -> None|
|`href_fragment_id`|fn|pub|1916-1928|def href_fragment_id(href: str) -> str|
|`_clean_document_style`|fn|priv|1986-2006|def _clean_document_style(self) -> None|
|`_add_document_style`|fn|priv|2007-2038|def _add_document_style(self) -> None|
|`_normalize_document_links`|fn|priv|2053-2067|def _normalize_document_links(self) -> None|
|`_remove_unused_images`|fn|priv|2068-2109|def _remove_unused_images(self) -> None|
|`_remove_unused_assets`|fn|priv|2110-2144|def _remove_unused_assets(self) -> None|
|`_normalize_image_position`|fn|priv|2145-2204|def _normalize_image_position(self) -> None|
|`_clean_assets_tree`|fn|priv|2205-2227|def _clean_assets_tree(self) -> None|
|`_remove_empty_assets_root`|fn|priv|2228-2266|def _remove_empty_assets_root(self) -> None|
|`DownloaderRegistry`|class|pub|2267-2324|class DownloaderRegistry|
|`DownloaderRegistry.__init__`|fn|priv|2272-2280|def __init__(self)|
|`DownloaderRegistry.register`|fn|pub|2281-2290|def register(self, downloader_cls: type[BaseDownloader]) ...|
|`DownloaderRegistry.detect`|fn|pub|2291-2324|def detect(self, url: str, session: requests.Session) -> ...|
|`guess_ext_from_content_type`|fn|pub|2330-2349|def guess_ext_from_content_type(ct: str) -> str|
|`NetworkImageRecorder`|class|pub|2350-2412|class NetworkImageRecorder|
|`NetworkImageRecorder.__init__`|fn|priv|2356-2367|def __init__(self, out_dir: Path)|
|`NetworkImageRecorder.attach`|fn|pub|2368-2412|def attach(self, page)|
|`NetworkImageRecorder.on_response`|fn|pub|2376-2409|def on_response(resp)|
|`DocumentViewerDownloader`|class|pub|2413-2612|class DocumentViewerDownloader(BaseDownloader)|
|`DocumentViewerDownloader.TOC_SELECTORS`|var|pub|2420||
|`DocumentViewerDownloader.CONTENT_SELECTORS`|var|pub|2429||
|`DocumentViewerDownloader.TOC_SCROLL_SELECTORS`|var|pub|2442||
|`DocumentViewerDownloader.matches_url`|fn|pub|2451-2461|def matches_url(cls, url: str) -> bool|
|`DocumentViewerDownloader.probe_html`|fn|pub|2463-2474|def probe_html(cls, url: str, html: str) -> bool|
|`DocumentViewerDownloader._pick_best_outerhtml`|fn|priv|2475-2506|def _pick_best_outerhtml(self, page, selectors: List[str]...|
|`DocumentViewerDownloader._expand_full_toc`|fn|priv|2507-2508|def _expand_full_toc(|
|`DocumentViewerDownloader._scroll_toc_container`|fn|priv|2568-2569|def _scroll_toc_container(|
|`_find_scroll_container`|fn|priv|2626-2691|def _find_scroll_container(self, page)|
|`_auto_scroll_element`|fn|priv|2692-2700|def _auto_scroll_element(|
|`_auto_scroll`|fn|priv|2773-2779|def _auto_scroll(|
|`_collect_cards_from_container`|fn|priv|2849-2856|def _collect_cards_from_container(|
|`_best_card_for_fragment`|fn|priv|2934-2935|def _best_card_for_fragment(|
|`score_value`|fn|pub|2954-2974|def score_value(val: str) -> int|
|`_fragment_matches_url`|fn|priv|2991-3010|def _fragment_matches_url(self, fragment: str, data_url: ...|
|`_toc_tree_from_html`|fn|priv|3011-3020|def _toc_tree_from_html(self, toc_html: str) -> List[TocN...|
|`_iter_nodes`|fn|priv|3022-3032|def _iter_nodes(nodes: List[TocNode]) -> Iterable[TocNode]|
|`_first_numeric_index`|fn|priv|3034-3046|def _first_numeric_index(nodes: List[TocNode]) -> Optiona...|
|`_trim_toc_nodes`|fn|priv|3048-3069|def _trim_toc_nodes(nodes: List[TocNode]) -> List[TocNode]|
|`_limit_toc_nodes`|fn|priv|3071-3072|def _limit_toc_nodes(|
|`_limit_by_reading_order`|fn|priv|3084-3085|def _limit_by_reading_order(|
|`_prune_toc_to_allowed`|fn|priv|3123-3124|def _prune_toc_to_allowed(|
|`_first_toc_entry_title`|fn|priv|3147-3159|def _first_toc_entry_title(nodes: List[TocNode]) -> Optio...|
|`_is_important_notice_label`|fn|priv|3161-3170|def _is_important_notice_label(title: Optional[str]) -> bool|
|`_is_important_notice_section`|fn|priv|3172-3187|def _is_important_notice_section(section_html: str) -> bool|
|`_select_section_nodes`|fn|priv|3189-3214|def _select_section_nodes(nodes: List[TocNode]) -> List[T...|
|`_dedup_toc_nodes_by_href`|fn|priv|3215-3253|def _dedup_toc_nodes_by_href(self, nodes: List[TocNode]) ...|
|`dedup_list`|fn|pub|3224-3251|def dedup_list(items: List[TocNode]) -> List[TocNode]|
|`_is_section_scrollable`|fn|priv|3254-3276|def _is_section_scrollable(self, page, viewport_multiplie...|
|`_remove_toc_elements`|fn|priv|3277-3313|def _remove_toc_elements(self, soup: BeautifulSoup) -> None|
|`_convert_doxygen_definition_lists`|fn|priv|3314-3380|def _convert_doxygen_definition_lists(self, soup: Beautif...|
|`_extract_fragment_only`|fn|priv|3381-3382|def _extract_fragment_only(|
|`score_value`|fn|pub|3401-3424|def score_value(val: str) -> int|
|`pick_best_section`|fn|pub|3425-3448|def pick_best_section(elements)|
|`matches_fragment`|fn|pub|3459-3478|def matches_fragment(el) -> bool|
|`_wait_for_fragment`|fn|priv|3506-3558|def _wait_for_fragment(self, page, fragment: str, timeout...|
|`_click_toc_link`|fn|priv|3559-3587|def _click_toc_link(self, page, fragment: str) -> bool|
|`run`|fn|pub|3588-3787|def run(self) -> None|
|`make_anchor`|fn|pub|3598-3616|def make_anchor(raw_fragment: str, title: str, used: Set[...|
|`normalize_text`|fn|pub|3617-3627|def normalize_text(value: str) -> str|
|`strip_ti_disclaimer`|fn|pub|3628-3658|def strip_ti_disclaimer(section_html: str) -> str|
|`DoxygenExportDownloader`|class|pub|4066-4265|class DoxygenExportDownloader(BaseDownloader)|
|`DoxygenExportDownloader.matches_url`|fn|pub|4074-4087|def matches_url(cls, url: str) -> bool|
|`DoxygenExportDownloader.probe_html`|fn|pub|4089-4100|def probe_html(cls, url: str, html: str) -> bool|
|`DoxygenExportDownloader._scope`|fn|priv|4101-4114|def _scope(self) -> Tuple[str, str]|
|`DoxygenExportDownloader._fetch_soup`|fn|priv|4115-4126|def _fetch_soup(self, url: str) -> BeautifulSoup|
|`DoxygenExportDownloader._is_in_scope`|fn|priv|4127-4143|def _is_in_scope(self, url: str, host: str, scope_dir_url...|
|`DoxygenExportDownloader._page_title`|fn|priv|4144-4159|def _page_title(self, soup: BeautifulSoup) -> str|
|`DoxygenExportDownloader._document_title`|fn|priv|4160-4191|def _document_title(self, soup: BeautifulSoup) -> str|
|`DoxygenExportDownloader._extract_main`|fn|priv|4192-4215|def _extract_main(self, soup: BeautifulSoup) -> Beautiful...|
|`DoxygenExportDownloader._remove_toc_elements`|fn|priv|4216-4242|def _remove_toc_elements(self, soup: BeautifulSoup) -> None|
|`DoxygenExportDownloader._links_to_html_pages`|fn|priv|4243-4244|def _links_to_html_pages(|
|`_expand_nav_tree`|fn|priv|4269-4305|def _expand_nav_tree(self, page) -> None|
|`_expand_nav_tree_full`|fn|priv|4306-4505|def _expand_nav_tree_full(self, page) -> None|
|`_expand_nav_tree_limited`|fn|priv|4513-4622|def _expand_nav_tree_limited(self, page, limit: int) -> None|
|`_cleanup_nav_tree_styles`|fn|priv|4623-4654|def _cleanup_nav_tree_styles(self, page) -> None|
|`_fetch_nav_tree_with_playwright`|fn|priv|4655-4744|def _fetch_nav_tree_with_playwright(self) -> Tuple[str, str]|
|`_nav_link_href`|fn|priv|4745-4770|def _nav_link_href(self, link, base_url: str) -> str|
|`_toc_tree_from_html`|fn|priv|4771-4780|def _toc_tree_from_html(self, toc_html: str) -> List[TocN...|
|`_toc_nodes_from_nav_html`|fn|priv|4781-4823|def _toc_nodes_from_nav_html(self, nav_html: str) -> List...|
|`parse_ul`|fn|pub|4794-4818|def parse_ul(ul) -> List[TocNode]|
|`_iter_toc_nodes`|fn|priv|4825-4835|def _iter_toc_nodes(nodes: List[TocNode]) -> Iterable[Toc...|
|`_select_main_container`|fn|priv|4836-4857|def _select_main_container(self, soup: BeautifulSoup)|
|`_find_fragment_anchor`|fn|priv|4858-4885|def _find_fragment_anchor(self, main, fragment: str)|
|`_normalize_heading_text`|fn|priv|4887-4895|def _normalize_heading_text(value: str) -> str|
|`_strip_duplicate_section_title`|fn|priv|4896-4897|def _strip_duplicate_section_title(|
|`_extract_section_html`|fn|priv|4940-4941|def _extract_section_html(|
|`direct_child`|fn|pub|4969-4980|def direct_child(el)|
|`_build_toc`|fn|priv|5004-5069|def _build_toc(self, doc: BeautifulSoup) -> List[TocNode]|
|`run`|fn|pub|5070-5269|def run(self) -> None|
|`MAX_PAGES`|var|pub|5256||
|`ResourceExplorerModule`|class|pub|5434-5466|class ResourceExplorerModule|
|`ResourceExplorerModule.select`|fn|pub|5441-5442|def select(|
|`ResourceExplorerModule.run`|fn|pub|5455-5466|def run(self, downloader: "ResourceExplorerDownloader", s...|
|`RMModuleDoxigen`|class|pub|5467-5524|class RMModuleDoxigen(ResourceExplorerModule)|
|`RMModuleDoxigen.select`|fn|pub|5476-5477|def select(|
|`RMModuleDoxigen.run`|fn|pub|5501-5524|def run(self, downloader: "ResourceExplorerDownloader", s...|
|`ResourceExplorerDownloader`|class|pub|5525-5657|class ResourceExplorerDownloader(BaseDownloader)|
|`ResourceExplorerDownloader.__init__`|fn|priv|5532-5543|def __init__(self, *args, **kwargs)|
|`ResourceExplorerDownloader.matches_url`|fn|pub|5545-5555|def matches_url(cls, url: str) -> bool|
|`ResourceExplorerDownloader.probe_html`|fn|pub|5557-5567|def probe_html(cls, url: str, html: str) -> bool|
|`ResourceExplorerDownloader._select_module`|fn|priv|5568-5569|def _select_module(|
|`ResourceExplorerDownloader._render_with_playwright`|fn|priv|5585-5622|def _render_with_playwright(self) -> str|
|`ResourceExplorerDownloader.run`|fn|pub|5623-5657|def run(self) -> None|
|`build_arg_parser`|fn|pub|5663-5708|def build_arg_parser() -> argparse.ArgumentParser|
|`print_strict_help`|fn|pub|5709-5758|def print_strict_help(program: str, version: str, parser:...|
|`main`|fn|pub|5759-5810|def main() -> int|


---

# version.py | Python | 13L | 0 symbols | 0 imports | 3 comments
> Path: `/home/ogekuri/HtmlDownloader/src/htmldownloader/version.py`

