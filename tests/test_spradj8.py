#!/usr/bin/env python3
"""Test case to ensure SPRADJ8 export does not duplicate sections or anchors."""

import re
import shutil
from pathlib import Path
from urllib.parse import urldefrag

from bs4 import BeautifulSoup

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


def _collect_document_sections(doc_path: Path) -> list[str]:
    soup = BeautifulSoup(doc_path.read_text(encoding="utf-8"), "html.parser")
    return [sec.get("id").lower() for sec in soup.find_all("section") if sec.get("id")]


def test_spradj8_deduplicates_sections_and_anchors(tmp_path_factory):
    project_root = Path(__file__).parent.parent
    out_dir = project_root / "temp" / "test_spradj8"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    url = "https://www.ti.com/document-viewer/lit/html/spradj8"

    assert run_download(url, out_dir), "Download failed for SPRADJ8"

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

    doc_sections = _collect_document_sections(doc_path)
    assert doc_sections, "document.html should contain sections"

    doc_soup = BeautifulSoup(doc_path.read_text(encoding="utf-8"), "html.parser")
    heading_text = "10 Debug Network Topologies and Techniques"
    heading_matches = [
        h for h in doc_soup.find_all(re.compile(r"^h[1-6]$"))
        if " ".join(h.get_text(" ", strip=True).split()) == heading_text
    ]
    assert len(heading_matches) == 1, f"Duplicate heading '{heading_text}' found"

    section_counts = {}
    for sec_id in doc_sections:
        section_counts[sec_id] = section_counts.get(sec_id, 0) + 1
    duplicated_sections = [s for s, c in section_counts.items() if c > 1]
    assert not duplicated_sections, f"Duplicated section ids in document: {duplicated_sections[:5]}"

    missing_in_doc = [frag for frag in frag_counts if frag not in section_counts]
    assert not missing_in_doc, f"TOC anchors missing in document: {missing_in_doc[:5]}"


if __name__ == "__main__":
    raise SystemExit(test_spradj8_deduplicates_sections_and_anchors())
