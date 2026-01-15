import requests
from urllib.parse import urldefrag

from bs4 import BeautifulSoup

from htmldownloader.cli import DocumentViewerDownloader


def test_deduplicate_toc_entries_promotes_children(tmp_path):
    toc_html = """<!doctype html>
<html><body><ul>
<li><a href="#a">A</a><ul><li><a href="#a-1">A1</a></li></ul></li>
<li><a href="#b">B</a></li>
<li><a href="#a">A duplicate</a><ul><li><a href="#c">C</a></li></ul></li>
</ul></body></html>
"""

    toc_path = tmp_path / "toc.html"
    toc_path.write_text(toc_html, encoding="utf-8")

    downloader = DocumentViewerDownloader("http://example", tmp_path, requests.Session())
    downloader._deduplicate_toc_entries()

    out = toc_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(out, "lxml")

    frags = []
    for a in soup.select("ul a[href]"):
        _, frag = urldefrag(a.get("href"))
        frags.append(frag)

    assert frags == ["a", "a-1", "b", "c"]
