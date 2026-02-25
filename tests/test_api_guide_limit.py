#!/usr/bin/env python3
"""Testa il limite --limit=30 sul Doxygen export AM64X API Guide."""

import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urldefrag

from bs4 import BeautifulSoup

from tests.document_links_check import assert_document_links_valid
from tests.heading_toc_check import assert_toc_headings_consistent


API_GUIDE_URL = "https://software-dl.ti.com/mcu-plus-sdk/esd/AM64X/latest/exports/docs/api_guide_am64x/index.html"
LIMIT = 30
GUID_ANCHOR_RE = re.compile(
    r"^guid-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    r"-guid-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)

EXPECTED_TOC_ENTRIES = [
    ("1 Introduction", 1),
    ("1.1 Getting Started", 2),
    ("1.2 Migration Information", 2),
    ("1.3 Block Diagram", 2),
    ("1.4 Directory Structure", 2),
    ("1.5 Licenses", 2),
    ("1.6 Help and Support", 2),
    ("1.7 Documentation Credits", 2),
    ("2 Getting Started", 1),
    ("2.1 Introduction", 2),
    ("2.1.1 Getting Started Goals", 3),
    ("2.1.2 Terms and Abbreviations", 3),
    ("2.1.3 Getting Started Steps", 3),
    ("2.1.4 Next Steps", 3),
    ("2.2 Download, Install and Setup SDK and Tools", 2),
    ("2.2.1 Host PC Requirements", 3),
    ("2.2.2 Download and Install the SDK", 3),
    ("2.2.3 Download and Install Additional SDK Tools", 3),
    ("2.2.3.1 SysConfig", 4),
    ("2.2.3.2 GCC AARCH64 Compiler", 4),
    ("2.2.3.3 GCC ARM (R5) Compiler", 4),
    ("2.2.3.4 Python3", 4),
    ("2.2.3.5 OpenSSL", 4),
    ("2.2.3.6 dfu-util", 4),
    ("2.2.3.6.1 Windows", 5),
    ("2.2.3.6.1.1 Steps to install windows generic USB drivers.", 6),
    ("2.2.3.6.1.2 Setps to Install drivers for using SBL DFU.", 6),
    ("2.2.3.6.2 Linux", 5),
    ("2.2.3.7 PRU-CGT", 4),
    ("2.2.3.8 Mono Runtime", 4),
]


_DOWNLOADED = False


def _ensure_api_guide_download(project_root: Path, out_dir: Path) -> None:
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
        API_GUIDE_URL,
        "--to-dir",
        str(out_dir),
        "--limit",
        str(LIMIT),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600,
        cwd=str(project_root),
    )

    assert result.returncode == 0, (
        f"CLI failed: rc={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    _DOWNLOADED = True


def _read_html(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def _normalize_text(value: str) -> str:
    return " ".join((value or "").split()).lower()


def _collect_toc_entries(path: Path) -> list[tuple[str, int]]:
    soup = _read_html(path)
    entries: list[tuple[str, int]] = []
    for link in soup.select("ul a"):
        title = " ".join(link.get_text(" ", strip=True).split())
        depth = len(link.find_parents("ul"))
        entries.append((title, depth))
    return entries


def test_api_guide_limit_downloads_first_30_sections():
    project_root = Path(__file__).parent.parent
    out_dir = project_root / "temp" / "test_api_guide_am64x"

    _ensure_api_guide_download(project_root, out_dir)

    toc_path = out_dir / "toc.html"
    doc_path = out_dir / "document.html"
    assert toc_path.exists(), "toc.html non trovato"
    assert doc_path.exists(), "document.html non trovato"

    doc_soup = _read_html(doc_path)

    # Verifica titolo del documento estratto dall'intestazione Doxygen
    first_paragraph = doc_soup.find("p")
    assert first_paragraph is not None, "document.html deve iniziare con una riga di titolo"
    title_text = " ".join(first_paragraph.get_text(" ", strip=True).split())
    assert title_text == "AM64x MCU+ SDK 11.02.00", f"Titolo documento inatteso: {title_text!r}"

    heading_ids = {h.get("id") for h in doc_soup.find_all(re.compile(r"^h[1-6]$")) if h.get("id")}
    guid_ids = {hid for hid in heading_ids if GUID_ANCHOR_RE.fullmatch(hid)}

    assert len(guid_ids) == LIMIT, "document.html deve contenere 30 anchor GUID sugli heading"
    legacy_page_ids = [sid for sid in heading_ids if sid.startswith("page-")]
    assert not legacy_page_ids, f"document.html contiene anchor legacy page-*: {legacy_page_ids[:5]}"

    for section in doc_soup.find_all("section"):
        headings = section.find_all(re.compile(r"^h[1-6]$"))
        if not headings:
            continue
        first_title = _normalize_text(headings[0].get_text(" ", strip=True))
        if not first_title:
            continue
        duplicate_count = sum(
            1 for h in headings
            if _normalize_text(h.get_text(" ", strip=True)) == first_title
        )
        assert duplicate_count == 1, (
            f"Titolo duplicato nella sezione {section.get('id')}: {headings[0].get_text(' ', strip=True)!r}"
        )
        for title_el in section.select(".headertitle .title, .header .title"):
            header_title = _normalize_text(title_el.get_text(" ", strip=True))
            assert header_title != first_title, (
                f"Titolo Doxygen duplicato nella sezione {section.get('id')}: {title_el.get_text(' ', strip=True)!r}"
            )

    toc_soup = _read_html(toc_path)
    toc_entries = _collect_toc_entries(toc_path)
    assert toc_entries == EXPECTED_TOC_ENTRIES, (
        "toc.html deve contenere le prime 30 voci in ordine e gerarchia attesi"
    )
    assert len(toc_entries) == LIMIT, "toc.html deve contenere esattamente 30 voci"
    toc_fragments = []
    for link in toc_soup.find_all("a"):
        href = link.get("href") or ""
        _, frag = urldefrag(href)
        if frag:
            toc_fragments.append(frag)
    invalid_guid_fragments = [frag for frag in toc_fragments if not GUID_ANCHOR_RE.fullmatch(frag)]
    assert not invalid_guid_fragments, f"TOC contiene anchor non GUID: {invalid_guid_fragments[:5]}"
    missing_in_doc = [frag for frag in toc_fragments if frag not in heading_ids]
    assert not missing_in_doc, f"Anchor mancanti sugli heading in document.html: {missing_in_doc[:5]}"


def test_api_guide_limit_headings_are_all_referenced_by_toc():
    project_root = Path(__file__).parent.parent
    out_dir = project_root / "temp" / "test_api_guide_am64x"

    _ensure_api_guide_download(project_root, out_dir)

    toc_path = out_dir / "toc.html"
    doc_path = out_dir / "document.html"
    assert_toc_headings_consistent(toc_path, doc_path)


def test_api_guide_post_links():
    """Verifica che tutti i link in document.html siano validi (TST-022)."""
    project_root = Path(__file__).parent.parent
    out_dir = project_root / "temp" / "test_api_guide_am64x"

    _ensure_api_guide_download(project_root, out_dir)

    doc_path = out_dir / "document.html"
    assert_document_links_valid(doc_path)


if __name__ == "__main__":
    raise SystemExit(test_api_guide_limit_downloads_first_30_sections())
