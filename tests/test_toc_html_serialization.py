from bs4 import BeautifulSoup

from htmldownloader.cli import TocNode, build_toc_html


def test_build_toc_html_serializes_one_list_item_per_line():
    toc_nodes = [
        TocNode(title="1 Root", href="#root"),
        TocNode(
            title="2 Parent",
            href="#parent",
            children=[
                TocNode(title="2.1 Child", href="#child-1"),
                TocNode(title="2.2 Child", href="#child-2"),
            ],
        ),
    ]

    toc_html = build_toc_html(toc_nodes)
    li_count = len(BeautifulSoup(toc_html, "lxml").find_all("li"))
    li_lines = [line for line in toc_html.splitlines() if "<li>" in line]

    assert li_count == 4
    assert len(li_lines) == li_count
    assert all(line.count("<li>") == 1 for line in li_lines)
