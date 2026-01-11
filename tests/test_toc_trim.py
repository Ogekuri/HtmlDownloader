from htmldownloader.cli import DocumentViewerDownloader, TocNode


def _titles(nodes):
    return [n.title for n in nodes]


def _flatten_titles(nodes):
    out = []
    for n in nodes:
        out.append(n.title)
        out.extend(_flatten_titles(n.children))
    return out


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


def test_limit_toc_nodes_truncates_preorder():
    nodes = [
        TocNode(
            title="1 Root",
            href="#1",
            children=[
                TocNode(title="1.1 Child", href="#1.1"),
                TocNode(title="1.2 Child", href="#1.2"),
            ],
        ),
        TocNode(
            title="2 Root",
            href="#2",
            children=[TocNode(title="2.1 Child", href="#2.1")],
        ),
    ]

    limited = DocumentViewerDownloader._limit_by_reading_order(nodes, 3)

    assert _titles(limited) == ["1 Root", "1.1 Child", "1.2 Child"]
    assert len(limited) == 3


def test_limit_by_reading_order_keeps_flat_order_without_duplicates():
    nodes = [
        TocNode(title="Intro", href="#0"),
        TocNode(
            title="1 Start",
            href="#1",
            children=[
                TocNode(title="1.1 Child", href="#1.1"),
                TocNode(title="1.2 Child", href="#1.2"),
            ],
        ),
        TocNode(title="2 Next", href="#2"),
        TocNode(title="IMPORTANT NOTICE", href="#3"),
    ]

    flat = DocumentViewerDownloader._select_section_nodes(nodes)
    limited = DocumentViewerDownloader._limit_by_reading_order(flat, 4)

    assert _titles(limited) == ["1 Start", "1.1 Child", "1.2 Child", "2 Next"]


def test_prune_toc_to_allowed_keeps_paths():
    root = TocNode(
        title="1 Root",
        href="#1",
        children=[
            TocNode(title="1.1 Child", href="#1.1"),
            TocNode(title="1.2 Child", href="#1.2"),
        ],
    )
    sibling = TocNode(title="2 Root", href="#2")
    nodes = [root, sibling]

    allowed = {id(root.children[1])}  # keep only 1.2 Child
    pruned = DocumentViewerDownloader._prune_toc_to_allowed(nodes, allowed)

    assert _flatten_titles(pruned) == ["1.2 Child"]
    assert all(n.title != "2 Root" for n in pruned)
