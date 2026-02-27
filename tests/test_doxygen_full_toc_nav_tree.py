"""
@file test_doxygen_full_toc_nav_tree.py
@brief Validate full Doxygen export TOC generation from nav tree.
@details Ensures no-limit Doxygen runs preserve nav-tree titles/hierarchy instead of page-title-derived fallbacks.
"""

from __future__ import annotations

from pathlib import Path

import requests
from bs4 import BeautifulSoup

from htmldownloader.cli import DoxygenExportDownloader, Logger


def test_doxygen_full_run_uses_nav_tree_labels_without_limit(tmp_path, monkeypatch) -> None:
    """
    @brief Verify no-limit run uses nav-tree labels for TOC generation.
    @details Reproduces a case where page titles include document prefix and asserts toc.html keeps nav labels and hierarchy.
    @param tmp_path Pytest temporary directory fixture.
    @param monkeypatch Pytest monkeypatch fixture.
    @return None Returns None after successful assertions.
    """
    out_dir = tmp_path / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    from_url = "https://example.com/docs/index.html"
    downloader = DoxygenExportDownloader(
        from_url=from_url,
        out_dir=out_dir,
        session=requests.Session(),
        logger=Logger(verbose=False, debug=False),
    )

    nav_html = """
    <ul>
      <li>
        <div class="item"><span class="label"><a class="index.html:intro" href="index.html#intro">Introduction</a></span></div>
        <ul class="children_ul">
          <li><div class="item"><span class="label"><a class="index.html:getting-started" href="index.html#getting-started">Getting Started</a></span></div></li>
        </ul>
      </li>
      <li><div class="item"><span class="label"><a class="guide.html:api" href="guide.html#api">API Guide</a></span></div></li>
    </ul>
    """

    index_html = """
    <html>
      <head><title>Doc Title: Introduction Page</title></head>
      <body>
        <div id="doc-content">
          <h1 id="intro">Doc Title: Introduction Page</h1>
          <h2 id="getting-started">Getting Started</h2>
          <p>Intro body.</p>
          <a href="guide.html">Open guide</a>
        </div>
      </body>
    </html>
    """
    guide_html = """
    <html>
      <head><title>Doc Title: API Reference</title></head>
      <body>
        <div id="doc-content">
          <h1 id="api">Doc Title: API Reference</h1>
          <p>API body.</p>
        </div>
      </body>
    </html>
    """

    pages = {
        "https://example.com/docs/index.html": index_html,
        "https://example.com/docs/guide.html": guide_html,
    }

    def _fake_fetch_soup(url: str) -> BeautifulSoup:
        """
        @brief Return deterministic HTML for requested URL.
        @details Serves prebuilt HTML fixtures for test URLs and fails on unexpected URL requests.
        @param url URL requested by downloader internals.
        @return BeautifulSoup Parsed HTML fixture.
        """
        html = pages.get(url)
        if html is None:
            raise AssertionError(f"Unexpected URL fetch: {url}")
        return BeautifulSoup(html, "lxml")

    monkeypatch.setattr(downloader, "_scope", lambda: ("example.com", "https://example.com/docs/"))
    monkeypatch.setattr(downloader, "_fetch_soup", _fake_fetch_soup)
    monkeypatch.setattr(downloader, "_fetch_nav_tree_with_playwright", lambda: (nav_html, ""))
    monkeypatch.setattr(downloader, "post_process", lambda: None)

    downloader.run()

    toc_path = out_dir / "toc.html"
    assert toc_path.exists(), "toc.html not generated"
    toc_soup = BeautifulSoup(toc_path.read_text(encoding="utf-8"), "lxml")

    top_level_labels = [
        " ".join(link.get_text(" ", strip=True).split())
        for link in toc_soup.select("body > ul > li > a")
    ]
    assert top_level_labels == ["Introduction", "API Guide"]
    assert all(not label.startswith("Doc Title:") for label in top_level_labels)

    all_labels = [
        " ".join(link.get_text(" ", strip=True).split())
        for link in toc_soup.select("body ul a")
    ]
    assert all_labels == ["Introduction", "Getting Started", "API Guide"]
