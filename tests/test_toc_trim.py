from htmldownloader.cli import DocumentViewerDownloader, TocNode


def _titles(nodes):
    return [n.title for n in nodes]


def test_trim_toc_nodes_starts_at_first_numeric_and_drops_notice():
    nodes = [
        TocNode(title="Doc Title", href="#0"),
        TocNode(title="Preface", href="#1"),
        TocNode(title="1 Start", href="#2"),
        TocNode(title="1.1 Sub", href="#3"),
        TocNode(title="2 Next", href="#4"),
        TocNode(title="IMPORTANT NOTICE", href="#5"),
    ]

    trimmed = DocumentViewerDownloader._trim_toc_nodes(nodes)

    assert _titles(trimmed) == [
        "1 Start",
        "1.1 Sub",
        "2 Next",
    ]


def test_trim_toc_nodes_handles_short_lists():
    short_nodes = [TocNode(title="a", href="#a"), TocNode(title="b", href="#b")]
    trimmed = DocumentViewerDownloader._trim_toc_nodes(short_nodes)
    assert _titles(trimmed) == ["a", "b"]


def test_select_section_nodes_limits_to_numeric_through_notice():
    nodes = [
        TocNode(title="Intro", href="#0"),
        TocNode(title="1 Start", href="#1"),
        TocNode(title="2 Next", href="#2"),
        TocNode(title="IMPORTANT NOTICE", href="#3"),
        TocNode(title="Appendix", href="#4"),
    ]

    selected = DocumentViewerDownloader._select_section_nodes(nodes)

    assert _titles(selected) == ["1 Start", "2 Next", "IMPORTANT NOTICE"]
