# HtmlDownloader Execution Workflow

Updated walkthrough of the runtime flow based on the current implementation in `src/htmldownloader/cli.py`.

### Common Initial Stages
- Help/version fast-exit: no args, `-h` or `--help` print the strict help block and exit 0; `--version`/`--ver` print only the version and exit 0; `--upgrade` runs `pip install --upgrade htmldownloader` and exits with its code.
- Argument parsing: required `--from-url`, `--to-dir`; optional `--user-agent`, `--limit`, `--verbose`, `--debug`, `--disable-numbering`.
- Version check: `check_for_new_version` hits GitHub releases with 1s timeout (non-blocking).
- Output/log setup: create destination dir, build logger (verbose/debug), initialize `requests.Session` with User-Agent.
- Downloader detection: register `resource-explorer`, `document-viewer`, `doxygen-export`; detect by URL/HTML probe, instantiate and run.
- Final logging: print selected downloader and saved paths for `toc.html`, `index.html`, `document.html`, `assets/`.

---

### 1. DocumentViewerDownloader (TI document-viewer)
- Playwright boot: launch headless Chromium, attach `NetworkImageRecorder` to capture image responses.
- TOC capture: expand nav repeatedly (`_expand_full_toc`) and scroll containers (`_scroll_toc_container`), pick best nav HTML; fallback to headings-derived TOC if absent; prepend doc-lister title when found.
- TOC trimming & limits: build TOC tree, select section slice from first title starting with "1 " through last "IMPORTANT NOTICE"; display TOC trimmed to start at first numeric and drop trailing Important Notice; apply `--limit` in reading order (pre-order), pruning display TOC accordingly; deduplicate TOC hrefs at display time.
- Section planning: map each TOC entry to a stable local anchor, reuse anchors for duplicate URLs/fragments; prepare section plan respecting limit slice and dedup.
- Card cache: optionally collect pre-loaded `.documentSection[data-url]` cards from the scroll container to avoid extra navigation; reuse cached sections when fragments match.
- Section fetch: for each planned entry, try TOC click + fragment wait, else navigate; auto-scroll for lazy assets; extract fragment-only content; strip TOC/nav elements; ensure heading ids; download referenced assets and rewrite to local paths; strip styles.
- Important Notice handling: drop trailing IMPORTANT NOTICE section if present, else strip TI disclaimer block from the last section.
- Document assembly: wrap sections in `<section id=...>` (inject heading if missing), prepend title from TOC/first section, merge to `document.html`; convert Doxygen-style definition lists and "label : description" paragraphs to bold uppercase labels inline.
- TOC/index generation: derive TOC from cleaned display nodes (or headings fallback), write `toc.html` (frame targets set) and `index.html` frameset.

### 2. DoxygenExportDownloader (Doxygen/static exports)
- Scope setup: compute host/scope dir; fetch index; derive document title from `#titlearea`, `#projectname/#projectnumber`, or fallback title.
- TOC via Playwright: load page, expand nav tree (skipping API Reference), optionally limited by `--limit`; clean inline styles; output nav HTML + outline. In `toc_only` mode, write `toc_raw.html`/`toc_raw.txt` and exit.
- Limited path (when nav HTML present and limit set):
    - Build TOC nodes from nav HTML, truncate to limit in reading order; group fragments per page; fetch only referenced pages; extract section slices between fragments; strip duplicate section titles while preserving ids when needed.
    - Deduplicate identical content by hash, re-pointing TOC hrefs; assemble `<section id=page-N>` with `h1` titles; insert document title paragraph before container.
    - Collect all assets from touched pages, download, rewrite links, strip styles; emit `document.html`, `toc.html`, `index.html` then post-process.
- Full crawl path (fallback):
    - BFS crawl up to 250 HTML pages in scope; optional `--limit` truncates pages list.
    - For each page: extract main content (drop TOC/nav elements), strip duplicate top titles, ensure heading ids, deduplicate sections by content hash, build `<section id=page-N>` with `h1` titles; insert document title paragraph.
    - Build TOC from assembled document, apply `--limit`, download all discovered assets, rewrite links, strip styles; emit `document.html`, `toc.html`, `index.html` then post-process.

### 3. ResourceExplorerDownloader (wrapper)
- Fetch Resource Explorer shell; try modules in order. `RMModuleDoxigen` activates when an iframe under `div.css-1aefuid-contentContainer` is found; builds Doxygen URL relative to `https://dev.ti.com/tirex/explore/` and delegates to `DoxygenExportDownloader` with inherited options (`limit`, `user-agent`, `verbose`, `debug`, `disable-numbering`).
- If initial HTML fails module selection, render with Playwright to locate the iframe and retry; otherwise error.

---

### Post-Processing Pipeline (exact order)
Executed after writing `document.html`, `toc.html`, `index.html`:
1) `_clean_document_style` — remove external stylesheets, style tags, inline `style`/`class` attrs from document and TOC.
2) `_add_document_style` — inject minimal CSS adding borders to tables and standalone images.
3) `_normalize_document_links` — allow only external links with schemes or in-doc anchors that exist; rewrite resolvable fragments; drop others (verbose/debug stats).
4) `_remove_unused_images` — delete unreferenced images under assets/ based on HTML refs (path or filename).
5) `_remove_unused_assets` — delete any asset file not referenced in `document.html` (path or filename).
6) `_normalize_image_position` — move images into assets/ root with UUID suffix, update HTML refs.
7) `_clean_assets_tree` — prune empty asset subdirectories.
8) `_remove_empty_assets_root` — remove top-level assets/ if entirely empty (verbose log on success).
9) `_verify_toc_consistency` — check TOC links point to existing anchors and text matches heading.
10) `_verify_toc_depth` — warn if depth > 6.
11) `_prune_toc_and_clean_headings` — drop TOC entries at depth ≥7, strip numeric prefixes from TOC text and headings; convert pruned-heading targets to bold text.
12) `_enforce_toc_headings` — convert unreferenced headings to bold text; align heading levels to TOC depth (id or container-based).
13) `_test_toc_headings` — verify TOC↔heading coherence (ids/containers, depth match, full coverage); raises on failure.
14) `fix_heading_ref_position` — move referenced ids from containers to first heading inside; ensure TOC fragments point to headings.
15) `_enforce_toc_headings` — re-apply enforcement after id moves.
16) `_deduplicate_toc_entries` — remove duplicate TOC fragments, promoting children.
17) `_enforce_toc_headings` — re-apply enforcement after dedup.
18) `fix_heading_numbering` — strip existing numbering in TOC/headings; if numbering enabled, add hierarchical numbers from TOC structure.
19) `_test_toc_headings` — final TOC↔heading validation with logging.
