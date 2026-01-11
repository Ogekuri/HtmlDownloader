#!/usr/bin/env python3
"""Verifica estrazione TOC Doxygen (nav tree) in modalita' toc-only."""

import shutil
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from htmldownloader.cli import DoxygenExportDownloader, Logger
import requests


API_GUIDE_URL = "https://software-dl.ti.com/mcu-plus-sdk/esd/AM64X/latest/exports/docs/api_guide_am64x/index.html"


def _normalize_html(path: Path) -> str:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    return "\n".join(line.rstrip() for line in soup.prettify().splitlines() if line.strip())


def _normalize_outline(path: Path) -> str:
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.replace("\xa0", " ")
        if not line.strip():
            continue
        lines.append(" ".join(line.split()))
    return "\n".join(lines)


def test_api_guide_nav_tree_matches_fixtures():
    project_root = Path(__file__).parent.parent
    out_dir = project_root / "temp" / "test_api_guide_nav_tree"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    logger = Logger()
    downloader = DoxygenExportDownloader(API_GUIDE_URL, out_dir, session, logger=logger, toc_only=True)

    nav_html, nav_outline = downloader._fetch_nav_tree_with_playwright()

    if nav_html:
        (out_dir / "toc_raw.html").write_text(nav_html, encoding="utf-8")
    if nav_outline:
        (out_dir / "toc_raw.txt").write_text(nav_outline, encoding="utf-8")

    toc_html_path = out_dir / "toc_raw.html"
    toc_txt_path = out_dir / "toc_raw.txt"

    assert toc_html_path.exists(), "toc_raw.html non trovato"
    assert toc_txt_path.exists(), "toc_raw.txt non trovato"

    # Non devono essere generati gli artefatti documento
    assert not (out_dir / "document.html").exists(), "document.html non deve essere generato in toc-only"
    assert not (out_dir / "index.html").exists(), "index.html non deve essere generato in toc-only"

    expected_html_path = project_root / "src" / "tests" / "toc.html"
    expected_txt_path = project_root / "src" / "tests" / "toc.txt"

    actual_html = _normalize_html(toc_html_path)
    expected_html = _normalize_html(expected_html_path)
    assert actual_html == expected_html, "toc_raw.html non coincide con la fixture"

    actual_outline = _normalize_outline(toc_txt_path)
    expected_outline = _normalize_outline(expected_txt_path)
    assert actual_outline == expected_outline, "toc_raw.txt non coincide con la fixture"


if __name__ == "__main__":
    raise SystemExit(test_api_guide_nav_tree_matches_fixtures())
