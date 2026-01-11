#!/usr/bin/env python3
"""
Test case per verificare il download completo di sprz457 e la presenza di tutti gli elementi della TOC.

Questo test:
1. Scarica il documento da https://www.ti.com/document-viewer/lit/html/sprz457
2. Verifica che toc.html contenga tutti gli elementi richiesti
3. Salva l'output in temp/test_sprz457/

Requisito testato: TST-005
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup
from urllib.parse import urldefrag

from tests.document_links_check import assert_document_links_valid


# Elementi richiesti nella TOC
REQUIRED_TOC_ITEMS = [
    "Usage Notes and Advisories Matrices",
    "Devices Supported",
    "Silicon Usage Notes and Advisories",
    "Silicon Usage Notes",
    "i2287",
    "i2330",
    "i2351",
    "i2424",
    "Silicon Advisories",
    # Tutti gli advisory ID
    "i2049", "i2062", "i2103", "i2184", "i2189", "i2236", "i2185", "i2196",
    "i2207", "i2208", "i2228", "i2232", "i2244", "i2245", "i2091", "i2235",
    "i2303", "i2317", "i2134", "i2257", "i2277", "i2285", "i2310", "i2311",
    "i2313", "i2328", "i2241", "i2279", "i2307", "i2320", "i2329", "i2331",
    "i2243", "i2249", "i2256", "i2274", "i2278", "i2306", "i2363", "i2312",
    "i2371", "i2366", "i2138", "i2253", "i2259", "i2283", "i2305", "i2326",
    "i2368", "i2383", "i2401", "i2409", "i2291", "i2413", "i2414", "i2415",
    "i2417", "i2418", "i2419", "i2420", "i2422", "i2423", "i2431", "i2433",
    "i2434", "i2435", "i2436", "i2160", "i2482",
    "Trademarks",
    "Revision History",
]

EXPECTED_DOCUMENT_TITLE_SPRZ457 = "AM64x/AM243x Processor Silicon Revision 1.0, 2.0"


def run_download(url: str, output_dir: Path) -> bool:
    """
    Esegue il download del documento usando la CLI.
    
    Returns:
        True se il download ha successo, False altrimenti
    """
    print(f"[TEST] Downloading {url} to {output_dir}")
    
    # Trova il percorso dello script CLI
    project_root = Path(__file__).parent.parent
    cli_module = "htmldownloader.cli"
    
    # Esegui il download usando Python module
    cmd = [
        sys.executable,
        "-m",
        cli_module,
        "--from-url", url,
        "--to-dir", str(output_dir)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minuti di timeout
            cwd=str(project_root)
        )
        
        print(f"[TEST] Download stdout:\n{result.stdout}")
        if result.stderr:
            print(f"[TEST] Download stderr:\n{result.stderr}")
        
        if result.returncode != 0:
            print(f"[TEST] Download failed with return code {result.returncode}")
            return False
        
        return True
    except subprocess.TimeoutExpired:
        print("[TEST] Download timeout expired (600s)")
        return False
    except Exception as e:
        print(f"[TEST] Download failed with exception: {e}")
        return False


def verify_toc(toc_file: Path) -> tuple[bool, list[str]]:
    """
    Verifica che toc.html contenga tutti gli elementi richiesti.
    
    Returns:
        (success, missing_items)
    """
    print(f"[TEST] Verifying TOC file: {toc_file}")
    
    if not toc_file.exists():
        print(f"[TEST] FAIL: toc.html not found at {toc_file}")
        return False, ["toc.html file not found"]
    
    # Leggi e analizza il file TOC
    with open(toc_file, 'r', encoding='utf-8') as f:
        toc_content = f.read()
    
    soup = BeautifulSoup(toc_content, 'html.parser')
    toc_text = soup.get_text()

    heading = soup.find("h1")
    if not heading or heading.get_text(strip=True) != "TOC":
        return False, ["toc.html heading must be 'TOC'"]

    first_link = soup.select_one("ul a")
    if not first_link:
        return False, ["missing first TOC link"]
    first_text = " ".join(first_link.get_text(" ", strip=True).split())
    if not first_text.startswith("1 "):
        return False, ["first TOC entry should start with '1 ' (numbering should be present)"]

    if "Apri documento completo" in toc_text:
        return False, ["toc.html must not include 'Apri documento completo'"]
    
    # Verifica presenza di ogni elemento richiesto
    missing = []
    for item in REQUIRED_TOC_ITEMS:
        if item not in toc_text:
            missing.append(item)
            print(f"[TEST] MISSING: '{item}'")
        else:
            print(f"[TEST] FOUND: '{item}'")

    if "IMPORTANT NOTICE" in toc_text.upper():
        missing.append("TOC should not contain IMPORTANT NOTICE")
        print("[TEST] FAIL: 'IMPORTANT NOTICE' must be removed from TOC")
    
    if missing:
        print(f"\n[TEST] FAIL: {len(missing)} items missing from TOC")
        return False, missing
    else:
        print(f"\n[TEST] SUCCESS: All {len(REQUIRED_TOC_ITEMS)} required items found in TOC")
        return True, []


def verify_toc_links_against_document(toc_file: Path, document_file: Path) -> tuple[bool, list[str]]:
    """Verifica che ogni href nella TOC punti a un anchor presente in document.html."""
    print(f"[TEST] Verifying TOC links map to anchors in: {document_file}")

    if not toc_file.exists() or not document_file.exists():
        missing_files = []
        if not toc_file.exists():
            missing_files.append("toc.html")
        if not document_file.exists():
            missing_files.append("document.html")
        return False, missing_files

    toc_soup = BeautifulSoup(toc_file.read_text(encoding='utf-8'), 'html.parser')
    doc_soup = BeautifulSoup(document_file.read_text(encoding='utf-8'), 'html.parser')

    doc_ids = {el.get("id") for el in doc_soup.find_all(True) if el.get("id")}
    missing = []

    for link in toc_soup.find_all("a"):
        href = link.get("href") or ""
        _, frag = urldefrag(href)
        if not frag:
            continue
        if frag not in doc_ids:
            missing.append(frag)
            print(f"[TEST] TOC link missing anchor: #{frag}")

    if missing:
        print(f"[TEST] FAIL: {len(missing)} TOC links without matching anchors")
        return False, missing

    print(f"[TEST] SUCCESS: All TOC links resolve to document anchors ({len(doc_ids)} anchors available)")
    return True, []


def verify_document_content(document_file: Path, toc_file: Optional[Path] = None, expected_title: Optional[str] = None) -> tuple[bool, list[str]]:
    """
    Verifica che document.html contenga il testo richiesto dal test TST-007.
    
    Controlla la presenza di:
    - Sezione "1 Usage Notes and Advisories Matrices"
    - Tabelle "Table 1-1 Usage Notes Matrix" e "Table 1-2 Advisories Matrix"
    - Voci specifiche nella matrice usage notes (i2287, i2330, i2351, i2424)
    - Voci specifiche nella matrice advisory (i2049, i2062, i2103, i2184, i2160, i2482)
    - Sezione "1.1 Devices Supported"
    - Sezione "2 Silicon Usage Notes and Advisories"
    - Sottosezioni "2.1 Silicon Usage Notes" e "2.2 Silicon Advisories"
    - Sezione "Trademarks" con disclaimer
    - Sezione "Revision History" con voci di revisione
    - Sezione "IMPORTANT NOTICE AND DISCLAIMER" con full disclaimer text
    """
    print(f"[TEST] Verifying document.html content: {document_file}")
    
    if not document_file.exists():
        print(f"[TEST] FAIL: document.html not found at {document_file}")
        return False, ["document.html not found"]
    
    # Leggi il contenuto del documento
    with open(document_file, 'r', encoding='utf-8') as f:
        doc_content = f.read()
    
    # Estrai il testo puro
    soup = BeautifulSoup(doc_content, 'html.parser')
    doc_soup = soup
    doc_text = soup.get_text()

    def normalize_text(value: str) -> str:
        value = (value or "").replace("’", "'").replace("“", '"').replace("”", '"')
        value = re.sub(r"\s+", " ", value)
        return value.strip().lower()

    toc_first_title: Optional[str] = None
    if toc_file and toc_file.exists():
        try:
            toc_soup = BeautifulSoup(toc_file.read_text(encoding="utf-8"), "html.parser")
            first_link = toc_soup.select_one("ul a")
            if first_link:
                toc_first_title = normalize_text(first_link.get_text(" ", strip=True))
        except Exception:
            toc_first_title = None

    doc_text_norm = normalize_text(doc_text)

    if 'vedere "' in doc_text.lower() or "→" in doc_text:
        return False, ["document.html contains redirect placeholders"]

    sections = doc_soup.find_all("section")
    if sections:
        first_section_text = normalize_text(sections[0].get_text(" ", strip=True))
        if "usage notes and advisories matrices" not in first_section_text:
            return False, ["document.html does not start from first numerated section"]

    # Controlla la riga di titolo iniziale
    title_candidate: Optional[str] = expected_title or toc_first_title
    if not title_candidate and sections:
        title_candidate = sections[0].get_text(" ", strip=True)
    expected_title_norm = normalize_text(title_candidate) if title_candidate else None
    first_body_text = None
    first_body_tag = None
    if doc_soup.body:
        for child in doc_soup.body.children:
            if getattr(child, "name", None):
                text = normalize_text(child.get_text(" ", strip=True))
                if text:
                    first_body_text = text
                    first_body_tag = child.name
                    break
            elif isinstance(child, str):
                if child.strip():
                    first_body_text = normalize_text(child)
                    first_body_tag = "#text"
                    break
    if expected_title_norm and first_body_text and first_body_text != expected_title_norm:
        return False, ["document.html missing title line derived from TOC/first section"]
    if expected_title_norm and first_body_tag == "section":
        return False, ["document.html title line must precede sections"]

    # Ensure the main section heading is not duplicated
    heading_matches = [
        h for h in doc_soup.find_all(re.compile(r"^h[1-6]$"))
        if normalize_text(h.get_text(" ", strip=True)) == normalize_text("Usage Notes and Advisories Matrices")
    ]
    if len(heading_matches) > 1:
        missing = ["Duplicate heading 'Usage Notes and Advisories Matrices'"]
        print(f"[TEST] FAIL: heading appears {len(heading_matches)} times")
        return False, missing

    subsection_heading = normalize_text("2 Silicon Usage Notes and Advisories")
    subsection_matches = [
        h for h in doc_soup.find_all(re.compile(r"^h[1-6]$"))
        if normalize_text(h.get_text(" ", strip=True)) == subsection_heading
    ]
    if len(subsection_matches) > 1:
        missing = ["Duplicate heading '2 Silicon Usage Notes and Advisories'"]
        print(f"[TEST] FAIL: heading appears {len(subsection_matches)} times")
        return False, missing
    
    # Requisiti testuali da verificare
    required_content = [
        # Sezioni principali
        ("Usage Notes and Advisories Matrices", "Sezione principale TOC"),
        ("Table 1-1 Usage Notes Matrix", "Tabella Usage Notes"),
        ("Table 1-2 Advisories Matrix", "Tabella Advisories"),
        
        # Voci della matrice Usage Notes
        ("i2287", "Usage Note i2287"),
        ("i2330", "Usage Note i2330"),
        ("i2351", "Usage Note i2351"),
        ("i2424", "Usage Note i2424"),
        
        # Voci della matrice Advisories (check per alcuni chiave)
        ("i2049", "Advisory i2049"),
        ("i2062", "Advisory i2062"),
        ("i2103", "Advisory i2103"),
        ("i2184", "Advisory i2184"),
        ("i2160", "Advisory i2160"),
        ("i2482", "Advisory i2482"),
        
        # CRITICAL: Verify Details and Workaround sections are present
        ("Details", "Details sections (usage notes/advisories)"),
        ("Workaround(s)", "Workaround sections (usage notes/advisories)"),
        
        # Specific Details content from usage notes
        ("Two package terminals will be assigned new signal functions", "i2287 Details content"),
        ("DDR Register Configuration Tool provides custom register settings", "i2330 Details content"),
        ("OSPI Direct Access Controller (DAC) doesn't support Continuous Read mode", "i2351 Details content"),
        ("PLL programming sequence has been changed", "i2424 Details content"),
        
        # Specific Details content from advisories
        ("ECC Aggregator module is used to aggregate safety error occurrences", "i2049 Details content"),
        ("RAT error logging is programmed to disable logging", "i2062 Details content"),
        
        # Sottosezioni
        ("1.1 Devices Supported", "Sottosezione Devices Supported"),
        ("2 Silicon Usage Notes and Advisories", "Sezione Silicon Usage Notes and Advisories"),
        ("2.1 Silicon Usage Notes", "Sottosezione 2.1"),
        ("2.2 Silicon Advisories", "Sottosezione 2.2"),
        
        # Sezioni finali del documento
        ("Trademarks", "Sezione Trademarks"),
        ("All trademarks are the property of their respective owners", "Disclaimer trademarks"),
        ("Revision History", "Sezione Revision History"),
    ]
    
    missing = []
    for content_text, description in required_content:
        expected = normalize_text(content_text)
        if expected not in doc_text_norm:
            missing.append(description)
            print(f"[TEST] MISSING: {description} (text: '{content_text}')")
        else:
            print(f"[TEST] FOUND: {description}")
    
    if missing:
        print(f"\n[TEST] FAIL: {len(missing)} content items missing from document.html")
        return False, missing

    if "ti provides technical and reliability data" in doc_text_norm:
        print("\n[TEST] FAIL: TI disclaimer block still present in document.html")
        return False, ["TI disclaimer block should be removed"]

    if "important notice and disclaimer" in doc_text_norm:
        print("\n[TEST] FAIL: IMPORTANT NOTICE AND DISCLAIMER must be absent from document.html")
        return False, ["IMPORTANT NOTICE AND DISCLAIMER should be removed"]

    print(f"\n[TEST] SUCCESS: All {len(required_content)} required content items found in document.html")
    return True, []


def test_sprz457_download_and_verify():
    """
    Test function for pytest/unittest discovery.
    
    Verifica TST-005, TST-006 e TST-007:
    - Download completo del documento sprz457
    - Presenza di tutti gli elementi richiesti nella TOC
    - Corrispondenza link TOC -> anchor in document.html
    - Presenza di contenuti testuali specifici in document.html
    """
    print("\n" + "=" * 80)
    print("TEST: sprz457 Download and TOC Verification (TST-005, TST-006, TST-007)")
    print("=" * 80)
    
    # Setup paths
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "temp" / "test_sprz457"
    
    # Crea la directory di output
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # URL da testare
    test_url = "https://www.ti.com/document-viewer/lit/html/sprz457"
    
    # Step 1: Download
    print("\n[STEP 1] Downloading document...")
    download_success = run_download(test_url, output_dir)
    assert download_success, "Download failed"
    
    # Step 2: Verify TOC content
    print("\n[STEP 2] Verifying TOC content...")
    toc_file = output_dir / "toc.html"
    toc_success, missing_items = verify_toc(toc_file)
    
    assert toc_success, f"TOC verification failed. Missing {len(missing_items)} items: {missing_items[:10]}"
    
    # Step 3: Verify TOC links map to document anchors
    print("\n[STEP 3] Verifying TOC links -> document anchors...")
    doc_file = output_dir / "document.html"
    links_ok, missing_links = verify_toc_links_against_document(toc_file, doc_file)
    
    assert links_ok, f"TOC links verification failed. Missing {len(missing_links)} anchors: {missing_links[:10]}"
    
    # Step 4: Verify document content
    print("\n[STEP 4] Verifying document.html content...")
    content_ok, missing_content = verify_document_content(
        doc_file,
        toc_file,
        expected_title=EXPECTED_DOCUMENT_TITLE_SPRZ457,
    )
    
    assert content_ok, f"Document content verification failed. Missing {len(missing_content)} items: {missing_content}"
    
    # Final result
    print("\n" + "=" * 80)
    print("[TEST RESULT] SUCCESS")
    print(f"All {len(REQUIRED_TOC_ITEMS)} required TOC items verified")
    print(f"All TOC links resolve to document anchors")
    print(f"All required document.html content verified")
    print(f"Output saved to: {output_dir}")
    print("=" * 80)


def test_sprz457_post_links():
    """Verifica che tutti i link in document.html siano validi (TST-020)."""
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "temp" / "test_sprz457"
    test_url = "https://www.ti.com/document-viewer/lit/html/sprz457"

    # Ensure download is present
    if not (output_dir / "document.html").exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        download_success = run_download(test_url, output_dir)
        assert download_success, "Download failed"

    doc_path = output_dir / "document.html"
    assert_document_links_valid(doc_path)


def main():
    """Main test execution for standalone CLI usage."""
    print("=" * 80)
    print("TEST: sprz457 Download and TOC Verification")
    print("=" * 80)
    
    # Setup paths
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "temp" / "test_sprz457"
    
    # Crea la directory di output
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # URL da testare
    test_url = "https://www.ti.com/document-viewer/lit/html/sprz457"
    
    # Step 1: Download
    print("\n[STEP 1] Downloading document...")
    download_success = run_download(test_url, output_dir)
    
    if not download_success:
        print("\n[TEST RESULT] FAIL - Download failed")
        return 1
    
    # Step 2: Verify TOC
    print("\n[STEP 2] Verifying TOC content...")
    toc_file = output_dir / "toc.html"
    toc_success, missing_items = verify_toc(toc_file)

    print("\n[STEP 3] Verifying TOC links -> document anchors...")
    doc_file = output_dir / "document.html"
    links_ok, missing_links = verify_toc_links_against_document(toc_file, doc_file)
    
    print("\n[STEP 4] Verifying document.html content...")
    content_ok, missing_content = verify_document_content(
        doc_file,
        toc_file,
        expected_title=EXPECTED_DOCUMENT_TITLE_SPRZ457,
    )
    
    # Final result
    print("\n" + "=" * 80)
    if download_success and toc_success and links_ok and content_ok:
        print("[TEST RESULT] SUCCESS")
        print(f"All {len(REQUIRED_TOC_ITEMS)} required TOC items verified")
        print(f"All required document.html content verified")
        print(f"Output saved to: {output_dir}")
        return 0
    else:
        print("[TEST RESULT] FAIL")
        if missing_items:
            print(f"\nMissing {len(missing_items)} items from TOC:")
            for item in missing_items[:10]:  # Show first 10
                print(f"  - {item}")
            if len(missing_items) > 10:
                print(f"  ... and {len(missing_items) - 10} more")
        if missing_links:
            print(f"\nMissing anchors for {len(missing_links)} TOC links (showing up to 10):")
            for frag in missing_links[:10]:
                print(f"  - #{frag}")
        if missing_content:
            print(f"\nMissing {len(missing_content)} content items from document.html:")
            for item in missing_content[:10]:  # Show first 10
                print(f"  - {item}")
            if len(missing_content) > 10:
                print(f"  ... and {len(missing_content) - 10} more")
        return 1


if __name__ == "__main__":
    sys.exit(main())
