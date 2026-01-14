from __future__ import annotations

from pathlib import Path

import requests
from bs4 import BeautifulSoup

from htmldownloader.cli import BaseDownloader, Logger


class DummyDownloader(BaseDownloader):
    name = "dummy"

    def run(self) -> None:  # pragma: no cover
        raise NotImplementedError


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_fix_heading_numbering_removes_and_readds_numbering(tmp_path: Path) -> None:
    toc_html = """
    <html><body>
      <h1>TOC</h1>
      <ul>
        <li>
          <a href="#a">1. Intro</a>
          <ul>
            <li><a href="#b">1.2. Sub</a></li>
          </ul>
        </li>
        <li><a href="#c">2 Next</a></li>
      </ul>
    </body></html>
    """.strip()

    doc_html = """
    <html><body>
      <h1 id="a">1 Intro</h1>
      <h2 id="b">1.2. Sub</h2>
      <h1 id="c">2. Next</h1>
    </body></html>
    """.strip()

    (tmp_path / "toc.html").write_text(toc_html, encoding="utf-8")
    (tmp_path / "document.html").write_text(doc_html, encoding="utf-8")

    dl = DummyDownloader(
        from_url="https://example.invalid",
        out_dir=tmp_path,
        session=requests.Session(),
        logger=Logger(verbose=False, debug=False),
        disable_numbering=False,
    )

    dl.fix_heading_numbering()

    toc_soup = BeautifulSoup(_read_text(tmp_path / "toc.html"), "lxml")
    doc_soup = BeautifulSoup(_read_text(tmp_path / "document.html"), "lxml")

    toc_texts = [" ".join(a.get_text(" ", strip=True).split()) for a in toc_soup.select("ul a")]
    assert toc_texts == ["1 Intro", "1.1 Sub", "2 Next"]

    assert " ".join(doc_soup.find("h1", id="a").get_text(" ", strip=True).split()) == "1 Intro"
    assert " ".join(doc_soup.find("h2", id="b").get_text(" ", strip=True).split()) == "1.1 Sub"
    assert " ".join(doc_soup.find("h1", id="c").get_text(" ", strip=True).split()) == "2 Next"


def test_fix_heading_numbering_disable_numbering_only_removes(tmp_path: Path) -> None:
    toc_html = """
    <html><body>
      <h1>TOC</h1>
      <ul>
        <li><a href="#a">1. Intro</a></li>
        <li><a href="#b">1.2 Sub</a></li>
      </ul>
    </body></html>
    """.strip()

    doc_html = """
    <html><body>
      <h1 id="a">1. Intro</h1>
      <h2 id="b">1.2 Sub</h2>
    </body></html>
    """.strip()

    (tmp_path / "toc.html").write_text(toc_html, encoding="utf-8")
    (tmp_path / "document.html").write_text(doc_html, encoding="utf-8")

    dl = DummyDownloader(
        from_url="https://example.invalid",
        out_dir=tmp_path,
        session=requests.Session(),
        logger=Logger(verbose=False, debug=False),
        disable_numbering=True,
    )

    dl.fix_heading_numbering()

    toc_soup = BeautifulSoup(_read_text(tmp_path / "toc.html"), "lxml")
    doc_soup = BeautifulSoup(_read_text(tmp_path / "document.html"), "lxml")

    toc_texts = [" ".join(a.get_text(" ", strip=True).split()) for a in toc_soup.select("ul a")]
    assert toc_texts == ["Intro", "Sub"]

    assert " ".join(doc_soup.find("h1", id="a").get_text(" ", strip=True).split()) == "Intro"
    assert " ".join(doc_soup.find("h2", id="b").get_text(" ", strip=True).split()) == "Sub"


def test_remove_unused_assets_keeps_only_referenced_assets(tmp_path: Path) -> None:
    assets_dir = tmp_path / "assets"
    (assets_dir / "css").mkdir(parents=True, exist_ok=True)
    (assets_dir / "js").mkdir(parents=True, exist_ok=True)
    (assets_dir / "img").mkdir(parents=True, exist_ok=True)

    used_css = assets_dir / "css" / "used.css"
    unused_css = assets_dir / "css" / "unused.css"
    used_js = assets_dir / "js" / "used.js"
    unused_js = assets_dir / "js" / "unused.js"
    used_img = assets_dir / "img" / "used.png"
    unused_img = assets_dir / "img" / "unused.png"

    for p in (used_css, unused_css, used_js, unused_js, used_img, unused_img):
        p.write_text("x", encoding="utf-8")

    doc_html = """
    <html><body>
      <link rel="stylesheet" href="assets/css/used.css" />
      <script src="assets/js/used.js"></script>
      <img src="assets/img/used.png" />
    </body></html>
    """.strip()

    (tmp_path / "document.html").write_text(doc_html, encoding="utf-8")

    dl = DummyDownloader(
        from_url="https://example.invalid",
        out_dir=tmp_path,
        session=requests.Session(),
        logger=Logger(verbose=False, debug=False),
        disable_numbering=False,
    )

    dl._remove_unused_assets()

    assert used_css.exists()
    assert used_js.exists()
    assert used_img.exists()
    assert not unused_css.exists()
    assert not unused_js.exists()
    assert not unused_img.exists()


def test_remove_unused_assets_matches_by_basename(tmp_path: Path) -> None:
    assets_dir = tmp_path / "assets"
    (assets_dir / "img").mkdir(parents=True, exist_ok=True)

    logo = assets_dir / "img" / "logo.png"
    logo.write_text("x", encoding="utf-8")

    # document.html refers only to the basename, not the full relative path
    doc_html = """
    <html><body>
      <img src="logo.png" />
    </body></html>
    """.strip()

    (tmp_path / "document.html").write_text(doc_html, encoding="utf-8")

    dl = DummyDownloader(
        from_url="https://example.invalid",
        out_dir=tmp_path,
        session=requests.Session(),
        logger=Logger(verbose=False, debug=False),
        disable_numbering=False,
    )

    dl._remove_unused_assets()

    assert logo.exists()
