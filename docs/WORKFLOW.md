## Execution Units Index
- id: PROC:main
  type: Process
  parent_process: null
  role: CLI runtime process for downloader selection and export orchestration
  entrypoint_symbols:
    - __main__.py::__main__ -> main(...)
    - cli.py::main(...)
  defining_files:
    - src/htmldownloader/__main__.py
    - src/htmldownloader/cli.py
- id: PROC:pip-upgrade
  type: Process
  parent_process: null
  role: On-demand package upgrade child process
  entrypoint_symbols:
    - cli.py::UpgradeAction.__call__(...)
  defining_files:
    - src/htmldownloader/cli.py
- id: PROC:chromium
  type: Process
  parent_process: null
  role: Browser automation child process started by Playwright
  entrypoint_symbols:
    - cli.py::DocumentViewerDownloader.run(...)
    - cli.py::DoxygenExportDownloader._fetch_nav_tree_with_playwright(...)
    - cli.py::ResourceExplorerDownloader._render_with_playwright(...)
  defining_files:
    - src/htmldownloader/cli.py
- id: PROC:gha-build-release
  type: Process
  parent_process: null
  role: GitHub Actions runner process for release workflow
  entrypoint_symbols:
    - .github/workflows/release-uvx.yml::jobs.build-release
  defining_files:
    - .github/workflows/release-uvx.yml

## Execution Units
### PROC:main
- Entrypoint(s):
  - src/htmldownloader/__main__.py:11-12
  - src/htmldownloader/cli.py:5759-5812
- Lifecycle/trigger:
  - start: python module execution (`python -m htmldownloader`) or script entry execution.
  - stop: returns exit code via `SystemExit(main())`.
  - loop_blocking: no explicit infinite loop; blocking on HTTP I/O and Playwright calls.
  - explicit_threads: no explicit threads detected.
- Internal Call-Trace Tree:
  - `main(...)`: bootstrap CLI runtime and dispatch downloader [`src/htmldownloader/__main__.py`]
    - `main(...)`: parse arguments, initialize runtime, run selected downloader [`src/htmldownloader/cli.py`]
      - `build_arg_parser(...)`: build option schema and actions [`src/htmldownloader/cli.py`]
      - `print_strict_help(...)`: print strict help for empty/help invocation branch [`src/htmldownloader/cli.py`]
      - `check_for_new_version(...)`: update-notice preflight branch [`src/htmldownloader/cli.py`]
        - `_get_latest_version_from_github(...)`: fetch latest release tag [`src/htmldownloader/cli.py`]
        - `_is_version_newer(...)`: semantic tuple comparison [`src/htmldownloader/cli.py`]
          - `_parse_version_tuple(...)`: parse dotted version parts [`src/htmldownloader/cli.py`]
      - `DownloaderRegistry.register(...)`: register candidate downloader classes [`src/htmldownloader/cli.py`]
      - `DownloaderRegistry.detect(...)`: select downloader class by URL/probe [`src/htmldownloader/cli.py`]
      - `ResourceExplorerDownloader.run(...)`: branch when detected class is ResourceExplorer [`src/htmldownloader/cli.py`]
        - `_select_module(...)`: module detection over fetched HTML [`src/htmldownloader/cli.py`]
          - `RMModuleDoxigen.select(...)`: detect embedded Doxygen iframe URL [`src/htmldownloader/cli.py`]
        - `_render_with_playwright(...)`: JS-render fallback HTML acquisition [`src/htmldownloader/cli.py`]
        - `RMModuleDoxigen.run(...)`: delegate to DoxygenExport downloader [`src/htmldownloader/cli.py`]
          - `DoxygenExportDownloader.run(...)`: execute Doxygen export flow [`src/htmldownloader/cli.py`]
      - `DocumentViewerDownloader.run(...)`: branch when detected class is DocumentViewer [`src/htmldownloader/cli.py`]
        - `_expand_full_toc(...)`: expand TOC nodes [`src/htmldownloader/cli.py`]
        - `_scroll_toc_container(...)`: reveal lazy TOC entries [`src/htmldownloader/cli.py`]
        - `_pick_best_outerhtml(...)`: capture TOC/content DOM candidates [`src/htmldownloader/cli.py`]
        - `_toc_tree_from_html(...)`: parse TOC HTML to `TocNode` [`src/htmldownloader/cli.py`]
        - `_select_section_nodes(...)`: choose section extraction set [`src/htmldownloader/cli.py`]
        - `_trim_toc_nodes(...)`: trim display TOC (`IMPORTANT NOTICE` policy) [`src/htmldownloader/cli.py`]
        - `_limit_by_reading_order(...)`: apply optional limit [`src/htmldownloader/cli.py`]
        - `_prune_toc_to_allowed(...)`: prune TOC to selected nodes [`src/htmldownloader/cli.py`]
        - `_dedup_toc_nodes_by_href(...)`: remove duplicate href nodes [`src/htmldownloader/cli.py`]
        - `_click_toc_link(...)`: trigger section navigation [`src/htmldownloader/cli.py`]
        - `_wait_for_fragment(...)`: wait for fragment realization [`src/htmldownloader/cli.py`]
        - `_extract_fragment_only(...)`: isolate fragment-specific section [`src/htmldownloader/cli.py`]
        - `_remove_toc_elements(...)`: remove navigation artifacts [`src/htmldownloader/cli.py`]
        - `iter_asset_urls(...)`: enumerate asset URLs [`src/htmldownloader/cli.py`]
        - `local_path_for_url(...)`: map asset URL to local path [`src/htmldownloader/cli.py`]
        - `download_one(...)`: stream asset file [`src/htmldownloader/cli.py`]
        - `rewrite_asset_links_inplace(...)`: rewrite links to local assets [`src/htmldownloader/cli.py`]
        - `_convert_doxygen_definition_lists(...)`: convert definition list patterns [`src/htmldownloader/cli.py`]
        - `build_toc_html(...)`: emit toc.html payload [`src/htmldownloader/cli.py`]
        - `build_frameset_index(...)`: emit index.html payload [`src/htmldownloader/cli.py`]
        - `post_process(...)`: shared cleanup/validation pipeline [`src/htmldownloader/cli.py`]
      - `DoxygenExportDownloader.run(...)`: branch when detected class is Doxygen export [`src/htmldownloader/cli.py`]
        - `_scope(...)`: derive host and scoped root [`src/htmldownloader/cli.py`]
        - `_fetch_soup(...)`: fetch and parse HTML pages [`src/htmldownloader/cli.py`]
        - `_document_title(...)`: derive document title [`src/htmldownloader/cli.py`]
          - `_page_title(...)`: fallback title extraction [`src/htmldownloader/cli.py`]
        - `_fetch_nav_tree_with_playwright(...)`: acquire expanded nav tree [`src/htmldownloader/cli.py`]
          - `_expand_nav_tree(...)`: dispatch expansion strategy [`src/htmldownloader/cli.py`]
            - `_expand_nav_tree_limited(...)`: bounded expansion branch [`src/htmldownloader/cli.py`]
            - `_expand_nav_tree_full(...)`: full expansion branch [`src/htmldownloader/cli.py`]
          - `_cleanup_nav_tree_styles(...)`: normalize nav styles [`src/htmldownloader/cli.py`]
        - `_toc_nodes_from_nav_html(...)`: parse nav HTML to TOC nodes [`src/htmldownloader/cli.py`]
        - `_extract_section_html(...)`: per-fragment extraction from page soup [`src/htmldownloader/cli.py`]
        - `_links_to_html_pages(...)`: discover in-scope crawl targets [`src/htmldownloader/cli.py`]
        - `_extract_main(...)`: normalize page main content [`src/htmldownloader/cli.py`]
          - `_remove_toc_elements(...)`: remove navigation nodes [`src/htmldownloader/cli.py`]
        - `_build_toc(...)`: build TOC from unified document [`src/htmldownloader/cli.py`]
        - `iter_asset_urls(...)`: enumerate asset URLs [`src/htmldownloader/cli.py`]
        - `download_one(...)`: stream asset files [`src/htmldownloader/cli.py`]
        - `rewrite_asset_links_inplace(...)`: rewrite links to local assets [`src/htmldownloader/cli.py`]
        - `build_toc_html(...)`: emit toc.html payload [`src/htmldownloader/cli.py`]
        - `build_frameset_index(...)`: emit index.html payload [`src/htmldownloader/cli.py`]
        - `post_process(...)`: shared cleanup/validation pipeline [`src/htmldownloader/cli.py`]
- External Boundaries:
  - network/http: `requests.get`, `requests.Session.get`.
  - browser automation: Playwright API and Chromium runtime.
  - filesystem: output directory creation and HTML/asset writes.
  - subprocess spawn: `subprocess.run` via upgrade action.

### PROC:pip-upgrade
- Entrypoint(s):
  - src/htmldownloader/cli.py:574-604
- Lifecycle/trigger:
  - start: argparse action branch `--upgrade`.
  - stop: process exits with `parser.exit(proc.returncode)`.
  - loop_blocking: blocking child process execution until pip returns.
  - explicit_threads: no explicit threads detected.
- Internal Call-Trace Tree:
  - `UpgradeAction.__call__(...)`: run self-upgrade command and forward exit code [`src/htmldownloader/cli.py`]
- External Boundaries:
  - child process execution: `python -m pip install --upgrade htmldownloader`.

### PROC:chromium
- Entrypoint(s):
  - src/htmldownloader/cli.py:3659-3661
  - src/htmldownloader/cli.py:4666-4668
  - src/htmldownloader/cli.py:5593-5595
- Lifecycle/trigger:
  - start: `p.chromium.launch(headless=True)` inside Playwright contexts.
  - stop: explicit `browser.close()` or context manager exit.
  - loop_blocking: event-driven browser loop managed by Playwright runtime.
  - explicit_threads: no explicit threads detected in repository source.
- Internal Call-Trace Tree:
  - no internal functions defined under `src/` or `.github/workflows/` execute inside this process.
- External Boundaries:
  - Playwright transport/channel between Python process and browser process.

### PROC:gha-build-release
- Entrypoint(s):
  - .github/workflows/release-uvx.yml:13-48
- Lifecycle/trigger:
  - start: Git tag push matching `v*`.
  - stop: workflow job completion/failure.
  - loop_blocking: step-sequential job execution.
  - explicit_threads: no explicit threads detected.
- Internal Call-Trace Tree:
  - no internal functions defined under `src/` or `.github/workflows/`; workflow file defines step orchestration only.
- External Boundaries:
  - GitHub Actions hosted runner.
  - third-party actions (`actions/checkout`, `actions/setup-python`, `astral-sh/setup-uv`, `actions/attest-build-provenance`, `softprops/action-gh-release`).

## Communication Edges
- id: EDGE:main-to-pip-upgrade
  source: PROC:main
  destination: PROC:pip-upgrade
  direction: PROC:main -> PROC:pip-upgrade
  mechanism: child_process_spawn
  endpoint_or_channel: subprocess argv (`sys.executable -m pip install --upgrade htmldownloader`)
  payload_or_data_shape: argv:list[str], exit_code:int
  evidence:
    - src/htmldownloader/cli.py:592-603
- id: EDGE:main-to-chromium-document-viewer
  source: PROC:main
  destination: PROC:chromium
  direction: PROC:main -> PROC:chromium
  mechanism: playwright_browser_launch
  endpoint_or_channel: Playwright sync API browser context
  payload_or_data_shape: page commands (goto/evaluate/wait), HTML snapshots (str)
  evidence:
    - src/htmldownloader/cli.py:3659-3710
    - src/htmldownloader/cli.py:3914-3921
- id: EDGE:main-to-chromium-doxygen-nav
  source: PROC:main
  destination: PROC:chromium
  direction: PROC:main -> PROC:chromium
  mechanism: playwright_browser_launch
  endpoint_or_channel: Playwright sync API browser context
  payload_or_data_shape: nav expansion commands, nav HTML (`#nav-tree-contents ul`)
  evidence:
    - src/htmldownloader/cli.py:4655-4684
    - src/htmldownloader/cli.py:4686-4704
- id: EDGE:main-to-chromium-resource-explorer
  source: PROC:main
  destination: PROC:chromium
  direction: PROC:main -> PROC:chromium
  mechanism: playwright_browser_launch
  endpoint_or_channel: Playwright sync API browser context
  payload_or_data_shape: rendered page HTML for iframe/frame discovery
  evidence:
    - src/htmldownloader/cli.py:5585-5619
- id: EDGE:gha-runner-to-main-build
  source: PROC:gha-build-release
  destination: PROC:main
  direction: PROC:gha-build-release -> PROC:main
  mechanism: build_step_execution
  endpoint_or_channel: `python -m build` workflow step
  payload_or_data_shape: source tree input -> `dist/*` artifacts
  evidence:
    - .github/workflows/release-uvx.yml:34-40
