# Workflow Analysis

## 1. CLI Entry Point and Orchestration
- **CLI Initialization**: The entry point processes arguments, configures the environment, and dispatches the execution to a specific downloader.
- **Components**: `cli.py` (Main module), `DownloaderRegistry`, `Logger`.

- `main()`: `Main entry point` [`src/htmldownloader/cli.py`, `4715-4749`]
  - description: Orchestrates the application lifecycle: parses arguments, initializes logging and session, detects the appropriate downloader for the URL, and executes it. Finally logs the output locations.
  - input: None (uses `sys.argv`)
  - output: `ExitCode: int, 0 for success`
  - calls:
    - `build_arg_parser()`: `Constructs argument parser` [`src/htmldownloader/cli.py`, `4627-4667`]
      - description: Defines CLI arguments including URL, output directory, verbosity, and limit options.
      - input: None
      - output: `parser: ArgumentParser, configured parser`
    - `check_for_new_version()`: `Checks PyPI for updates` [`src/htmldownloader/cli.py`, `98-118`]
      - description: Queries PyPI JSON API to check if a newer version exists and prints a warning if so.
      - input: `program: str, app name; current_version: str, version string`
      - output: None
    - `DownloaderRegistry.detect()`: `Identifies downloader class` [`src/htmldownloader/cli.py`, `1837-1860`]
      - description: Iterates through registered downloader classes to find one that matches the URL or HTML content.
      - input: `url: str, target URL; session: Session, http session`
      - output: `downloader_cls: Type[BaseDownloader], matched class`
    - `BaseDownloader.run()`: `Abstract execution method` [`src/htmldownloader/cli.py`, `794-799`]
      - description: Interface method implemented by subclasses to perform the download logic.
      - input: None
      - output: None

## 2. Document Viewer Downloader Workflow
- **Feature**: Handles dynamic JS-heavy documentation sites (e.g., TI Document Viewer) using Playwright.
- **Components**: `DocumentViewerDownloader`, `NetworkImageRecorder`.

- `DocumentViewerDownloader.run()`: `Executes document viewer download` [`src/htmldownloader/cli.py`, `2872-3323`]
  - description: Launches a Playwright browser, navigates to the URL, expands the full Table of Contents (TOC) via repeated scrolling and clicking, extracts the TOC structure, and then iterates through TOC nodes to capture content.
  - input: None
  - output: None
  - calls:
    - `NetworkImageRecorder.attach()`: `Captures network images` [`src/htmldownloader/cli.py`, `1898-1905`]
      - description: Intercepts network responses to save image assets locally during browsing.
      - input: `page: Page, playwright page`
      - output: None
    - `_expand_full_toc()`: `Expands dynamic TOC` [`src/htmldownloader/cli.py`, `2000-2050`]
      - description: Repeatedly finds and clicks 'expand' buttons in the navigation tree until stable.
      - input: `page: Page, playwright page`
      - output: None
    - `_scroll_toc_container()`: `Scrolls TOC to load items` [`src/htmldownloader/cli.py`, `2060-2100`]
      - description: Scrolls the navigation container to trigger lazy-loading of tree items.
      - input: `page: Page, playwright page`
      - output: None
    - `BaseDownloader.post_process()`: `Runs cleanup pipeline` [`src/htmldownloader/cli.py`, `800-815`]
      - description: Executes a series of normalization and cleanup tasks on the generated files.
      - input: None
      - output: None

## 3. Doxygen Export Downloader Workflow
- **Feature**: Downloads static or semi-static sites with Doxygen-like structure (frameset or flat).
- **Components**: `DoxygenExportDownloader`.

- `DoxygenExportDownloader.run()`: `Executes doxygen export download` [`src/htmldownloader/cli.py`, `4129-4486`]
  - description: Fetches the index, determines the documentation title, extracts the navigation tree (optionally using Playwright if needed), and then crawls each page listed in the TOC to build a single offline document.
  - input: None
  - output: None
  - calls:
    - `_fetch_soup()`: `Downloads and parses HTML` [`src/htmldownloader/cli.py`, `3350-3365`]
      - description: Performs an HTTP GET and returns a BeautifulSoup object.
      - input: `url: str, target url`
      - output: `soup: BeautifulSoup, parsed html`
    - `_fetch_nav_tree_with_playwright()`: `Extracts TOC via browser` [`src/htmldownloader/cli.py`, `3400-3450`]
      - description: Uses Playwright to load the frameset/navigation frame and extract the HTML structure of the TOC.
      - input: None
      - output: `nav_html: str, html of nav; outline: str, text outline`
    - `BaseDownloader.post_process()`: `Runs cleanup pipeline` [`src/htmldownloader/cli.py`, `800-815`]
      - description: Executes a series of normalization and cleanup tasks.
      - input: None
      - output: None

## 4. Resource Explorer Downloader Workflow
- **Feature**: Handles 'Resource Explorer' wrappers, delegating to specific modules for the internal content.
- **Components**: `ResourceExplorerDownloader`, `RMModuleDoxigen`.

- `ResourceExplorerDownloader.run()`: `Executes resource explorer logic` [`src/htmldownloader/cli.py`, `4593-4626`]
  - description: Fetches the main wrapper page, identifies the embedded content module (e.g., Doxygen iframe), and delegates execution to that module. Uses Playwright fallback if simple HTTP fails to reveal content.
  - input: None
  - output: None
  - calls:
    - `_select_module()`: `Detects content module` [`src/htmldownloader/cli.py`, `4560-4580`]
      - description: Inspects HTML to find recognized content patterns (like inner Doxygen frames).
      - input: `html: str, page content`
      - output: `module: ResourceExplorerModule, handler; selection: dict, params`
    - `RMModuleDoxigen.run()`: `Delegates to Doxygen downloader` [`src/htmldownloader/cli.py`, `4520-4535`]
      - description: extracts the inner URL and instantiates a `DoxygenExportDownloader` to handle the actual content.
      - input: `downloader: ResourceExplorerDownloader, parent; selection: dict, params`
      - output: None
      - calls:
        - `DoxygenExportDownloader.run()`: `Executes doxygen download` [`src/htmldownloader/cli.py`, `4129-4486`]
          - description: See Doxygen Export Downloader Workflow.
          - input: None
          - output: None

## 5. Post-Processing Pipeline
- **Feature**: Common cleanup and normalization logic applied after any download.
- **Components**: `BaseDownloader` and internal helper methods.

- `BaseDownloader.post_process()`: `Orchestrates cleanup` [`src/htmldownloader/cli.py`, `800-815`]
  - description: Iterates through `self.post_process_pipeline`, executing methods to clean styles, normalize links, prune unused assets, and verify TOC consistency.
  - input: None
  - output: None
  - calls:
    - `_clean_document_style()`: `Simplifies CSS` [`src/htmldownloader/cli.py`, `1570-1600`]
      - description: Removes most external stylesheets and injects a minimal readability stylesheet.
      - input: None
      - output: None
    - `_normalize_document_links()`: `Fixes internal anchors` [`src/htmldownloader/cli.py`, `1610-1650`]
      - description: Rewrites hrefs to point to the correct internal anchors in the single-page document.
      - input: None
      - output: None
    - `_clean_assets_tree()`: `Removes empty dirs` [`src/htmldownloader/cli.py`, `1700-1730`]
      - description: Walks the assets directory and removes empty subdirectories.
      - input: None
      - output: None
