"""Shared test helper: validate document.html links.

Rules:
- Every <a href> must be either:
  1) an external URL with an explicit allowed scheme (http/https/ftp/ftps), or
  2) an in-document anchor of the form #<id> where <id> exists in document.html.

Any other href (including other .html links) is not allowed.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup


ALLOWED_EXTERNAL_SCHEMES = {"http", "https", "ftp", "ftps"}


def assert_document_links_valid(doc_path: Path) -> None:
    assert doc_path.exists(), f"document.html non trovato: {doc_path}"

    soup = BeautifulSoup(doc_path.read_text(encoding="utf-8"), "html.parser")

    doc_ids = {
        (el.get("id") or "").strip()
        for el in soup.find_all(True)
        if (el.get("id") or "").strip()
    }

    invalid: list[str] = []

    for a in soup.find_all("a", href=True):
        href = (a.get("href") or "").strip()
        if href == "":
            invalid.append("<empty href>")
            continue

        if href.startswith("#"):
            frag = href[1:].strip()
            if not frag:
                invalid.append("# (empty fragment)")
                continue
            if frag not in doc_ids:
                invalid.append(f"#{frag} (anchor missing)")
            continue

        parsed = urlparse(href)
        scheme = (parsed.scheme or "").lower()
        if scheme in ALLOWED_EXTERNAL_SCHEMES:
            continue

        # Disallow everything else, including relative links and *.html links.
        invalid.append(href)

    assert not invalid, (
        "document.html contiene link non autorizzati (prime voci): "
        + ", ".join(invalid[:12])
        + (", ..." if len(invalid) > 12 else "")
    )
