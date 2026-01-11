#!/usr/bin/env python3
"""Test case to ensure SPRADJ8 export does not duplicate sections or anchors."""

import re
import shutil
from pathlib import Path
from urllib.parse import urldefrag

from bs4 import BeautifulSoup

from tests.document_links_check import assert_document_links_valid
from tests.heading_toc_check import assert_toc_headings_consistent
from tests.test_sprz457 import run_download


def _collect_toc_fragments(toc_path: Path) -> list[str]:
    soup = BeautifulSoup(toc_path.read_text(encoding="utf-8"), "html.parser")
    fragments: list[str] = []
    for link in soup.find_all("a"):
        href = link.get("href") or ""
        _, frag = urldefrag(href)
        if frag:
            fragments.append(frag.lower())
    return fragments


def _collect_document_heading_ids(doc_path: Path) -> list[str]:
    soup = BeautifulSoup(doc_path.read_text(encoding="utf-8"), "html.parser")
    return [h.get("id").lower() for h in soup.find_all(re.compile(r"^h[1-6]$")) if h.get("id")]


_DOWNLOADED = False


def _ensure_spradj8_download(project_root: Path, out_dir: Path) -> None:
    global _DOWNLOADED
    if _DOWNLOADED and (out_dir / "toc.html").exists() and (out_dir / "document.html").exists():
        return

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    url = "https://www.ti.com/document-viewer/lit/html/spradj8"
    assert run_download(url, out_dir), "Download failed for SPRADJ8"
    _DOWNLOADED = True


def test_spradj8_deduplicates_sections_and_anchors(tmp_path_factory):
    project_root = Path(__file__).parent.parent
    out_dir = project_root / "temp" / "test_spradj8"

    _ensure_spradj8_download(project_root, out_dir)

    toc_path = out_dir / "toc.html"
    doc_path = out_dir / "document.html"
    assert toc_path.exists(), "toc.html not found"
    assert doc_path.exists(), "document.html not found"

    toc_fragments = _collect_toc_fragments(toc_path)
    assert toc_fragments, "TOC should contain at least one anchor"

    frag_counts = {}
    for frag in toc_fragments:
        frag_counts[frag] = frag_counts.get(frag, 0) + 1
    duplicated_toc = [f for f, c in frag_counts.items() if c > 1]
    assert not duplicated_toc, f"Duplicated TOC anchors: {duplicated_toc[:5]}"

    doc_heading_ids = _collect_document_heading_ids(doc_path)
    assert doc_heading_ids, "document.html should contain headings with ids"

    doc_soup = BeautifulSoup(doc_path.read_text(encoding="utf-8"), "html.parser")
    heading_text = "10 Debug Network Topologies and Techniques"

    def norm(value: str) -> str:
        return " ".join((value or "").split()).lower()

    expected = norm(heading_text)
    heading_matches = [
        h
        for h in doc_soup.find_all(["strong", re.compile(r"^h[1-6]$")])
        if norm(h.get_text(" ", strip=True)) == expected
    ]
    assert len(heading_matches) == 1, (
        f"Heading '{heading_text}' not found or duplicated (found={len(heading_matches)})"
    )

    heading_counts = {}
    for hid in doc_heading_ids:
        heading_counts[hid] = heading_counts.get(hid, 0) + 1
    duplicated_headings = [s for s, c in heading_counts.items() if c > 1]
    assert not duplicated_headings, f"Duplicated heading ids in document: {duplicated_headings[:5]}"

    missing_in_doc = [frag for frag in frag_counts if frag not in heading_counts]
    assert not missing_in_doc, f"TOC anchors missing as heading ids in document: {missing_in_doc[:5]}"


def test_spradj8_headings_are_all_referenced_by_toc(tmp_path_factory):
    project_root = Path(__file__).parent.parent
    out_dir = project_root / "temp" / "test_spradj8"

    _ensure_spradj8_download(project_root, out_dir)

    toc_path = out_dir / "toc.html"
    doc_path = out_dir / "document.html"
    assert_toc_headings_consistent(toc_path, doc_path)


def test_spradj8_post_links():
    """Verifica che tutti i link in document.html siano validi (TST-021)."""
    project_root = Path(__file__).parent.parent
    out_dir = project_root / "temp" / "test_spradj8"

    _ensure_spradj8_download(project_root, out_dir)

    doc_path = out_dir / "document.html"
    assert_document_links_valid(doc_path)


if __name__ == "__main__":
    raise SystemExit(test_spradj8_deduplicates_sections_and_anchors())
