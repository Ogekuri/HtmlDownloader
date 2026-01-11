#!/usr/bin/env python3
"""Shared test helper: validate toc.html ↔ document.html heading references.

Rules (as per DES-021):
- Every href fragment in toc.html must reference a heading h1..h6.
- Every heading h1..h6 in document.html must be referenced directly by toc.html via its own id.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urldefrag

from bs4 import BeautifulSoup


_HEADING_RE = re.compile(r"^h[1-6]$")


def _read_html(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def _collect_toc_fragment_ids(toc_soup: BeautifulSoup) -> set[str]:
    ids: set[str] = set()
    for a in toc_soup.find_all("a", href=True):
        href = (a.get("href") or "").strip()
        _, frag = urldefrag(href)
        frag = (frag or "").strip()
        if frag:
            ids.add(frag.lower())
    return ids


def _iter_headings(doc_soup: BeautifulSoup) -> Iterable:
    yield from doc_soup.find_all(_HEADING_RE)


def assert_toc_headings_consistent(toc_path: Path, doc_path: Path) -> None:
    assert toc_path.exists(), f"toc.html non trovato: {toc_path}"
    assert doc_path.exists(), f"document.html non trovato: {doc_path}"

    toc_soup = _read_html(toc_path)
    doc_soup = _read_html(doc_path)

    toc_ids = _collect_toc_fragment_ids(toc_soup)
    assert toc_ids, "toc.html non contiene alcun href con fragment (#...)"

    # Build a quick lookup for document ids.
    doc_by_id: dict[str, object] = {}
    for el in doc_soup.find_all(True):
        el_id = (el.get("id") or "").strip()
        if el_id:
            doc_by_id.setdefault(el_id.lower(), el)

    missing_toc_targets: list[str] = []
    bad_toc_targets: list[str] = []

    for frag_id in sorted(toc_ids):
        target = doc_by_id.get(frag_id)
        if not target:
            missing_toc_targets.append(frag_id)
            continue

        name = (getattr(target, "name", "") or "").lower()
        if not _HEADING_RE.match(name):
            bad_toc_targets.append(f"{frag_id} (tag={name or 'unknown'})")

    assert not missing_toc_targets, (
        "toc.html contiene href verso id non presenti in document.html: "
        f"{missing_toc_targets[:10]}"
        + (" ..." if len(missing_toc_targets) > 10 else "")
    )
    assert not bad_toc_targets, (
        "toc.html contiene href verso target non valido (non heading e non container con heading): "
        f"{bad_toc_targets[:10]}"
        + (" ..." if len(bad_toc_targets) > 10 else "")
    )

    # Now verify: every heading is referenced directly by id.
    unreferenced_headings: list[str] = []
    for h in _iter_headings(doc_soup):
        hid = (h.get("id") or "").strip()
        hid_l = hid.lower() if hid else ""

        referenced = bool(hid_l and hid_l in toc_ids)

        if not referenced:
            title = " ".join(h.get_text(" ", strip=True).split())
            unreferenced_headings.append(
                f"{h.name}#{hid or '<no-id>'} {title!r}".strip()
            )

    assert not unreferenced_headings, (
        "document.html contiene heading non referenziati dalla TOC: "
        f"{unreferenced_headings[:10]}"
        + (" ..." if len(unreferenced_headings) > 10 else "")
    )
