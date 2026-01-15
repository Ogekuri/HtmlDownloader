#!/usr/bin/env python3
"""Testa il limite --limit=30 sul Resource Explorer TI (modulo Doxygen)."""

import re
import shutil
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup


RESOURCE_EXPLORER_URL = (
    "https://dev.ti.com/tirex/explore/node?node="
    "A__AD2nw6Uu4txAz2eqZdShBg__DIGITAL-POWER-SDK-AM263X__k-hvNHd__LATEST"
)
LIMIT = 30

_DOWNLOADED = False


def _ensure_resource_explorer_download(project_root: Path, out_dir: Path) -> None:
    """Run the download once per test session to keep runtime reasonable."""
    global _DOWNLOADED
    if _DOWNLOADED and (out_dir / "toc.html").exists() and (out_dir / "document.html").exists():
        return

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "htmldownloader.cli",
        "--from-url",
        RESOURCE_EXPLORER_URL,
        "--to-dir",
        str(out_dir),
        "--limit",
        str(LIMIT),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=900,
        cwd=str(project_root),
    )

    assert result.returncode == 0, (
        f"CLI failed: rc={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    assert "resource-explorer" in (result.stdout or "").lower(), (
        "CLI output must mention resource-explorer as selected downloader"
    )
    _DOWNLOADED = True


def _read_html(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def _collect_toc_entries(path: Path) -> list[str]:
    soup = _read_html(path)
    return [link.get_text(" ", strip=True) for link in soup.select("ul a")]


def test_resource_explorer_limit_downloads_first_30_sections():
    project_root = Path(__file__).parent.parent
    out_dir = project_root / "temp" / "test_resource_explorer_am263x"

    _ensure_resource_explorer_download(project_root, out_dir)

    toc_path = out_dir / "toc.html"
    doc_path = out_dir / "document.html"
    assert toc_path.exists(), "toc.html non trovato"
    assert doc_path.exists(), "document.html non trovato"

    toc_entries = _collect_toc_entries(toc_path)
    assert 0 < len(toc_entries) <= LIMIT, "toc.html deve contenere al massimo 30 voci"

    doc_soup = _read_html(doc_path)
    heading_ids = {
        h.get("id")
        for h in doc_soup.find_all(re.compile(r"^h[1-6]$"))
        if h.get("id")
    }
    expected_pages = {f"page-{i}" for i in range(1, LIMIT + 1)}

    toc_soup = _read_html(toc_path)
    toc_fragments = []
    for link in toc_soup.find_all("a"):
        href = (link.get("href") or "").strip()
        if "#" in href:
            frag = href.split("#", 1)[1].strip()
            if frag:
                toc_fragments.append(frag)

    missing_in_doc = [frag for frag in toc_fragments if frag not in heading_ids]
    assert not missing_in_doc, f"Anchor mancanti per link TOC: {missing_in_doc[:5]}"

    extra_pages = [hid for hid in heading_ids if hid.startswith("page-") and hid not in expected_pages]
    assert not extra_pages, f"document.html contiene sezioni oltre il limite: {extra_pages[:5]}"
