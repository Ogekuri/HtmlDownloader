#!/usr/bin/env python3
"""Test generico sui download definiti in examples.sh."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urldefrag, urlparse

import pytest
from bs4 import BeautifulSoup


DEFAULT_TIMEOUT = 900
_DOWNLOADED: set[tuple[str, int | None]] = set()
BACKSLASH_SCOPE_DIRS = {
    "out_www.ti.com_document-viewer_am6442_datasheet",
    "out_software-dl.ti.com_ind_comms_sdk_am64x_latest_docs_api_guide_am64x",
    "out_software-dl.ti.com_motor_control_sdk_am243x_11_00_00_06_docs_api_guide_am243x",
    "out_dev.ti.com_tirex_explore_node",
}
BACKSLASH_TOKEN_RE = re.compile(r"[A-Z0-9]{2,}\\[A-Z0-9]{2,}")

RUN_EXAMPLES_DOWNLOADS = os.environ.get("RUN_EXAMPLES_DOWNLOADS", "").lower()
pytestmark = pytest.mark.skipif(
    RUN_EXAMPLES_DOWNLOADS not in {"1", "true", "yes"},
    reason=(
        "Questo test richiede l'abilitazione esplicita: "
        "eseguire `RUN_EXAMPLES_DOWNLOADS=1 pytest tests/test_examples_downloads.py`"
    ),
)


def _read_html(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def _normalize_text(text: str) -> str:
    return " ".join((text or "").split()).lower()


def _parse_examples(script_path: Path) -> tuple[int, list[dict[str, object]]]:
    text = script_path.read_text(encoding="utf-8")

    n_value = 5
    match_n = re.search(r"^\s*N\s*=\s*(\d+)", text, re.M)
    if match_n:
        n_value = int(match_n.group(1))

    blocks = list(re.finditer(r"urls=\(\s*([^)]*?)\)", text, re.S))
    entries: list[dict[str, object]] = []
    for idx, block in enumerate(blocks):
        block_text = block.group(1)
        urls = re.findall(r"\"([^\"]+)\"", block_text)

        next_start = blocks[idx + 1].start() if idx + 1 < len(blocks) else len(text)
        segment = text[block.end():next_start]

        limit = None
        match_limit = re.search(r"--limit\s+(\d+)", segment)
        if match_limit:
            limit = int(match_limit.group(1))

        for url in urls:
            entries.append({"url": url, "limit": limit})

    return n_value, entries


def _make_last(url: str, n_value: int) -> str:
    clean = url.split("#", 1)[0]
    clean = clean.split("?", 1)[0]
    clean = clean.rstrip("/")

    if clean.endswith(".html"):
        clean = clean.rsplit("/", 1)[0]

    parsed = urlparse(clean)
    host = parsed.netloc
    path = parsed.path.lstrip("/")
    segments = [seg for seg in path.split("/") if seg]

    start = 0
    if len(segments) > n_value:
        start = len(segments) - n_value

    out = ""
    for idx in range(start, len(segments)):
        seg = segments[idx]
        if not seg:
            continue
        out = f"{out}_{seg}" if out else seg

    return f"{host}_{out}"


def _ensure_download(project_root: Path, url: str, limit: int | None, out_dir: Path) -> None:
    key = (url, limit)
    if key in _DOWNLOADED and (out_dir / "toc.html").exists() and (out_dir / "document.html").exists():
        return

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "htmldownloader.cli",
        "--from-url",
        url,
        "--to-dir",
        str(out_dir),
    ]
    if limit is not None:
        cmd.extend(["--limit", str(limit)])

    env = os.environ.copy()
    src_path = project_root / "src"
    env["PYTHONPATH"] = f"{src_path}{os.pathsep}{env.get('PYTHONPATH', '')}"

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=DEFAULT_TIMEOUT,
        cwd=str(project_root),
        env=env,
    )

    assert result.returncode == 0, (
        f"CLI failed for {url}: rc={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
    )

    _DOWNLOADED.add(key)


def _collect_toc_entries(toc_soup: BeautifulSoup) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for link in toc_soup.select("ul a[href]"):
        href = (link.get("href") or "").strip()
        _, frag = urldefrag(href)
        frag = (frag or "").strip()
        if not frag:
            continue
        entries.append(
            {
                "frag": frag,
                "frag_l": frag.lower(),
                "text": _normalize_text(link.get_text(" ", strip=True)),
                "depth": len(link.find_parents("ul")),
            }
        )
    return entries


def _collect_heading_info(doc_soup: BeautifulSoup) -> tuple[dict[str, dict[str, object]], list[str]]:
    heading_by_id: dict[str, dict[str, object]] = {}
    duplicates: list[str] = []
    order = 0

    for h in doc_soup.find_all(re.compile(r"^h[1-6]$")):
        hid = (h.get("id") or "").strip()
        if not hid:
            continue
        hid_l = hid.lower()
        if hid_l in heading_by_id:
            duplicates.append(hid)
            continue
        heading_by_id[hid_l] = {
            "text": _normalize_text(h.get_text(" ", strip=True)),
            "level": int(h.name[1]),
            "order": order,
        }
        order += 1

    return heading_by_id, duplicates


def _check_backslash_corruption(
    url: str,
    out_dir: Path,
    toc_soup: BeautifulSoup,
    doc_soup: BeautifulSoup,
) -> list[str]:
    if out_dir.name not in BACKSLASH_SCOPE_DIRS:
        return []

    hits: list[str] = []
    for link in toc_soup.select("ul a[href]"):
        text = link.get_text(" ", strip=True)
        if "\\" in text and BACKSLASH_TOKEN_RE.search(text):
            hits.append(f"toc: {text}")
    for h in doc_soup.find_all(re.compile(r"^h[1-6]$")):
        text = h.get_text(" ", strip=True)
        if "\\" in text and BACKSLASH_TOKEN_RE.search(text):
            hits.append(f"doc: {text}")

    if hits:
        return [f"backslash corruption in headings/toc for {url}: {hits[:8]}"]
    return []


def _check_output(url: str, out_dir: Path, limit: int | None) -> list[str]:
    toc_path = out_dir / "toc.html"
    doc_path = out_dir / "document.html"

    issues: list[str] = []

    if not toc_path.exists():
        issues.append(f"missing toc.html for {url}")
        return issues
    if not doc_path.exists():
        issues.append(f"missing document.html for {url}")
        return issues

    toc_soup = _read_html(toc_path)
    doc_soup = _read_html(doc_path)

    toc_entries = _collect_toc_entries(toc_soup)
    if not toc_entries:
        issues.append(f"no toc entries with fragments for {url}")
        return issues

    heading_by_id, heading_dups = _collect_heading_info(doc_soup)

    toc_fragments = [entry["frag_l"] for entry in toc_entries]
    toc_unique = set(toc_fragments)

    frag_counts: dict[str, int] = {}
    for frag in toc_fragments:
        frag_counts[frag] = frag_counts.get(frag, 0) + 1
    dup_toc = [frag for frag, count in frag_counts.items() if count > 1]
    if dup_toc:
        dup_preview = sorted(dup_toc)[:8]
        issues.append(f"duplicated toc fragments for {url}: {dup_preview}")

    if heading_dups:
        issues.append(f"duplicated heading ids for {url}: {heading_dups[:8]}")

    missing_in_doc = [frag for frag in toc_unique if frag not in heading_by_id]
    if missing_in_doc:
        issues.append(f"toc fragments missing in document for {url}: {sorted(missing_in_doc)[:8]}")

    extra_in_doc = [hid for hid in heading_by_id.keys() if hid not in toc_unique]
    if extra_in_doc:
        issues.append(f"headings missing in toc for {url}: {sorted(extra_in_doc)[:8]}")

    mismatched_text = []
    depth_mismatch = []
    for entry in toc_entries:
        info = heading_by_id.get(entry["frag_l"])
        if not info:
            continue
        if entry["text"] != info["text"]:
            mismatched_text.append(
                f"{entry['frag']} toc='{entry['text']}' doc='{info['text']}'"
            )
        expected_level = min(max(int(entry["depth"]), 1), 6)
        if info["level"] != expected_level:
            depth_mismatch.append(
                f"{entry['frag']} toc_depth={entry['depth']} heading=h{info['level']}"
            )

    if mismatched_text:
        issues.append(f"toc/heading text mismatch for {url}: {mismatched_text[:5]}")
    if depth_mismatch:
        issues.append(f"toc/heading depth mismatch for {url}: {depth_mismatch[:5]}")

    if not missing_in_doc and not extra_in_doc and not dup_toc:
        order_indexes = [heading_by_id[entry["frag_l"]]["order"] for entry in toc_entries]
        if order_indexes != sorted(order_indexes):
            issues.append(f"toc order does not match document order for {url}")

    if limit is not None:
        if len(toc_unique) > limit:
            issues.append(f"toc entries exceed limit for {url}: {len(toc_unique)} > {limit}")
        if len(heading_by_id) > limit:
            issues.append(f"heading count exceeds limit for {url}: {len(heading_by_id)} > {limit}")

    issues.extend(_check_backslash_corruption(url, out_dir, toc_soup, doc_soup))

    return issues


def test_examples_downloads_toc_alignment():
    project_root = Path(__file__).parent.parent
    script_path = project_root / "examples.sh"

    n_value, entries = _parse_examples(script_path)
    assert entries, "examples.sh does not contain any urls"

    failures: list[str] = []

    for entry in entries:
        url = entry["url"]
        limit = entry["limit"]
        out_dir = project_root / "temp" / f"out_{_make_last(url, n_value)}"

        _ensure_download(project_root, url, limit, out_dir)
        failures.extend(_check_output(url, out_dir, limit))

    assert not failures, "\n".join(failures)


if __name__ == "__main__":
    raise SystemExit(test_examples_downloads_toc_alignment())
