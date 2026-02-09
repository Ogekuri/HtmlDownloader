# Workflow Analysis

This document outlines the execution workflow of the `htmldownloader` tool, analyzing the call stack from the entry point to the core logic components.

## 1. Main Execution Flow
*   **CLI Entry Point** (`htmldownloader.cli`)
    *   `main()`: `Entry point for the command line interface` [`src/htmldownloader/cli.py`, 4715-4763]
        *   description: Handles argument parsing, logging setup, downloader registration, and execution initialization.
        *   input: `None` (reads `sys.argv`)
        *   output: `int` (exit code)
        *   calls:
            *   `build_arg_parser()`: `Constructs the argument parser` [`src/htmldownloader/cli.py`, 4627-4667]
                *   description: Defines the CLI arguments (url, output dir, limits, flags).
                *   input: `None`
                *   output: `argparse.ArgumentParser`
            *   `check_for_new_version()`: `Checks for package updates on PyPI` [`src/htmldownloader/cli.py`, 98-117]
                *   description: Queries PyPI/GitHub to see if a newer version is available.
                *   input: `program: str`, `current_version: str`
                *   output: `None`
            *   `DownloaderRegistry.register()`: `Registers a downloader class` [`src/htmldownloader/cli.py`, 1834-1836]
                *   description: Adds a downloader implementation to the registry.
                *   input: `downloader_cls: type[BaseDownloader]`
                *   output: `None`
            *   `DownloaderRegistry.detect()`: `Identifies the appropriate downloader` [`src/htmldownloader/cli.py`, 1837-1860]
                *   description: Matches the URL or HTML content against registered downloaders.
                *   input: `url: str`, `session: requests.Session`
                *   output: `type[BaseDownloader]`
            *   `BaseDownloader.run()`: `Executes the downloading process` [`src/htmldownloader/cli.py`, 794-795]
                *   description: Abstract method implemented by subclasses to perform the specific download logic.
                *   input: `None`
                *   output: `None`

## 2. Document Viewer Downloader (Feature)
*   **Component**: `DocumentViewerDownloader` (inherits `BaseDownloader`)
    *   `run()`: `Orchestrates the scraping of a dynamic document viewer` [`src/htmldownloader/cli.py`, 2872-3050+]
        *   description: Uses Playwright to render the page, extract the TOC, and scrape content sections.
        *   input: `None`
        *   output: `None`
        *   calls:
            *   `NetworkImageRecorder.attach()`: `Captures network images` [`src/htmldownloader/cli.py`, 1882+]
                *   description: Intercepts network requests to save images locally.
                *   input: `page: Page`
                *   output: `None`
            *   `_expand_full_toc()`: `Expands the TOC in the UI` [`src/htmldownloader/cli.py`, 1950+]
                *   description: Clicks expansion buttons in the navigation tree.
                *   input: `page: Page`
                *   output: `None`
            *   `_scroll_toc_container()`: `Scrolls TOC to trigger lazy loading` [`src/htmldownloader/cli.py`, 1950+]
                *   description: Scrolls the navigation container to ensure all elements are rendered.
                *   input: `page: Page`
                *   output: `None`
            *   `_toc_tree_from_html()`: `Parses TOC HTML into nodes` [`src/htmldownloader/cli.py`, 797-798]
                *   description: Converts raw HTML navigation into a structured list of TocNodes.
                *   input: `toc_html: str`
                *   output: `List[TocNode]`
            *   `_limit_by_reading_order()`: `Limits the number of sections` [`src/htmldownloader/cli.py`, 209+]
                *   description: Truncates the list of sections to download based on the --limit argument.
                *   input: `nodes: List[TocNode]`, `limit: int`
                *   output: `List[TocNode]`
            *   `post_process()`: `Runs cleanup and normalization` [`src/htmldownloader/cli.py`, 800-809]
                *   description: Executes a pipeline of text processing and structure verification steps.
                *   input: `None`
                *   output: `None`

## 3. Doxygen Export Downloader (Feature)
*   **Component**: `DoxygenExportDownloader` (inherits `BaseDownloader`)
    *   `run()`: `Downloads static Doxygen-style documentation` [`src/htmldownloader/cli.py`, 4129-4200+]
        *   description: Crawls a Doxygen export site, fetching pages defined in the navigation tree.
        *   input: `None`
        *   output: `None`
        *   calls:
            *   `_scope()`: `Determines the URL scope` [`src/htmldownloader/cli.py`, 3340-3346]
                *   description: Calculates the base URL and host for relative link resolution.
                *   input: `None`
                *   output: `Tuple[str, str]`
            *   `_fetch_soup()`: `Downloads and parses a page` [`src/htmldownloader/cli.py`, 3348-3350]
                *   description: Fetches a URL via HTTP and returns a BeautifulSoup object.
                *   input: `url: str`
                *   output: `BeautifulSoup`
            *   `_fetch_nav_tree_with_playwright()`: `Extracts navigation structure` [`src/htmldownloader/cli.py`, 4135]
                *   description: Uses Playwright to load the side panel and extract the navigation HTML.
                *   input: `None`
                *   output: `Tuple[Optional[str], Optional[str]]`
            *   `limit_toc_nodes()`: `Applies entry limit` [`src/htmldownloader/cli.py`, 209-228]
                *   description: Reduces the TOC size if a limit is specified.
                *   input: `nodes: List[TocNode]`, `max_entries: Optional[int]`
                *   output: `List[TocNode]`
            *   `_iter_toc_nodes()`: `Flattens TOC structure` [`src/htmldownloader/cli.py`, 4150]
                *   description: Yields all TOC nodes in a flat sequence.
                *   input: `nodes: List[TocNode]`
                *   output: `Iterator[TocNode]`
            *   `post_process()`: `Runs cleanup and normalization` [`src/htmldownloader/cli.py`, 800-809]
                *   description: Inherited pipeline for final document cleanup.
                *   input: `None`
                *   output: `None`

## 4. Resource Explorer Downloader (Feature)
*   **Component**: `ResourceExplorerDownloader` (inherits `BaseDownloader`)
    *   `run()`: `Handles TI Resource Explorer pages` [`src/htmldownloader/cli.py`, 4593-4620]
        *   description: Identifies the specific resource module (e.g., Doxygen) and delegates execution.
        *   input: `None`
        *   output: `None`
        *   calls:
            *   `_select_module()`: `Finds a matching sub-module` [`src/htmldownloader/cli.py`, 4552-4560]
                *   description: Iterates through available modules to find one that handles the content.
                *   input: `html: str`, `soup: Optional[BeautifulSoup]`
                *   output: `Optional[Tuple[ResourceExplorerModule, Dict[str, str]]]`
            *   `_render_with_playwright()`: `Renders dynamic content` [`src/htmldownloader/cli.py`, 4611]
                *   description: Fallback to full browser rendering if static analysis fails.
                *   input: `None`
                *   output: `str`
            *   `RMModuleDoxigen.run()`: `Executes Doxygen module logic` [`src/htmldownloader/cli.py`, 4520-4533]
                *   description: Delegates the actual download to an inner DoxygenExportDownloader.
                *   input: `downloader: ResourceExplorerDownloader`, `selection: Dict[str, str]`
                *   output: `None`
                *   calls:
                    *   `DoxygenExportDownloader.run()`: `Executes the Doxygen download` [`src/htmldownloader/cli.py`, 4129]
                        *   description: See Doxygen Export Downloader section.
                        *   input: `None`
                        *   output: `None`
