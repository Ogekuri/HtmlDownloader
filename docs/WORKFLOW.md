# Software Workflow Analysis

## 1. Core Workflow
This section outlines the high-level execution flow initiated by the user.

*   **Entry Point Execution**
    *   `htmldownloader.__main__`: Entry point script. [<src/htmldownloader/__main__.py>, lines 1-7]
    *   `cli.main()`: Main execution logic. [<src/htmldownloader/cli.py>, lines 4715-4759]
        *   description: Parses arguments, initializes environment, detects downloader, and executes the download process.
        *   input: `sys.argv` (command line arguments)
        *   output: Exit code (0 for success, non-zero for error)
        *   calls:
            *   `build_arg_parser()`: configures argument parser.
            *   `check_for_new_version()`: checks GitHub for updates.
            *   `Logger()`: initializes logging.
            *   `requests.Session()`: initializes HTTP session.
            *   `DownloaderRegistry()`: initializes downloader registry.
            *   `DownloaderRegistry.register()`: registers `ResourceExplorerDownloader`, `DocumentViewerDownloader`, `DoxygenExportDownloader`.
            *   `DownloaderRegistry.detect()`: identifies appropriate downloader for the URL.
            *   `downloader.run()`: executes the selected downloader strategy.

## 2. Downloader Detection
*   **Registry & Detection**
    *   `DownloaderRegistry`: Registry class for managing downloader strategies. [<src/htmldownloader/cli.py>, lines 1830-1850]
    *   `detect()`: Selects the correct downloader class. [<src/htmldownloader/cli.py>, lines 1837-1850]
        *   description: Checks registered downloaders against the URL; if ambiguous, fetches the page content to probe.
        *   input: `url`, `session`
        *   output: `type[BaseDownloader]` subclass
        *   calls:
            *   `matches_url()`: on each registered class.
            *   `session.get()`: fetches page content if URL matching is insufficient.
            *   `probe_html()`: on each registered class using fetched content.

## 3. Texas Instruments Document Viewer Workflow
This workflow handles dynamic JavaScript-heavy documentation pages (e.g., TI datasheets).

*   **Initialization & Setup**
    *   `DocumentViewerDownloader`: Handler for TI document viewer pages. [<src/htmldownloader/cli.py>, lines 1925-3320]
    *   `run()`: Orchestrates the scraping process using Playwright. [<src/htmldownloader/cli.py>, lines 2872-3320]
        *   description: Launches browser, captures TOC, iterates sections, and saves content.
        *   calls:
            *   `NetworkImageRecorder()`: initializes network asset interceptor.
            *   `sync_playwright()`: starts Playwright session.
            *   `page.goto()`: navigates to the target URL.
            *   `_expand_full_toc()`: expands sidebar navigation to reveal all links.
            *   `_scroll_toc_container()`: ensures lazy-loaded TOC items are visible.
            *   `_pick_best_outerhtml()`: captures the Table of Contents HTML.
            *   `_toc_tree_from_html()`: parses TOC HTML into `TocNode` structure.

*   **Content Extraction Loop**
    *   `DocumentViewerDownloader.run()` (continued loop over `section_plan`)
        *   description: Iterates through each section identified in the TOC to capture content.
        *   calls:
            *   `_best_card_for_fragment()`: checks if content is already cached in "cards".
            *   `_click_toc_link()`: simulates click on sidebar to load content.
            *   `_wait_for_fragment()`: waits for the specific section content to load.
            *   `page.goto()`: direct navigation if clicking fails.
            *   `_auto_scroll()`: scrolls page to trigger lazy-loading of images.
            *   `_pick_best_outerhtml()`: captures the section's HTML content.
            *   `_remove_toc_elements()`: cleans up navigation elements from captured HTML.
            *   `_extract_fragment_only()`: isolates the target section content.

*   **Output Generation**
    *   `DocumentViewerDownloader` (finalization)
        *   calls:
            *   `build_toc_html()`: Generates `toc.html`. [<src/htmldownloader/cli.py>, line 652]
            *   `build_frameset_index()`: Generates `index.html` frameset. [<src/htmldownloader/cli.py>, line 699]
            *   `post_process()`: Runs cleaning pipeline. [<src/htmldownloader/cli.py>, line 800]

## 4. Doxygen Export Workflow
This workflow handles static Doxygen-generated sites.

*   **Initialization & Navigation**
    *   `DoxygenExportDownloader`: Handler for Doxygen documentation. [<src/htmldownloader/cli.py>, lines 3324-4485]
    *   `run()`: Orchestrates the crawling process. [<src/htmldownloader/cli.py>, lines 4129-4485]
        *   description: Crawls Doxygen site structure and downloads pages/assets.
        *   calls:
            *   `_scope()`: determines crawl scope (host and base directory).
            *   `_fetch_soup()`: downloads and parses the index page.
            *   `_fetch_nav_tree_with_playwright()`: captures the navigation structure (uses Playwright to handle JS tree).
            *   `_toc_nodes_from_nav_html()`: parses navigation HTML into `TocNode` structure.

*   **Page Processing Loop**
    *   `DoxygenExportDownloader.run()` (loop over `flat_nodes`)
        *   description: Iterates through all pages found in the navigation tree.
        *   calls:
            *   `_fetch_soup()`: downloads HTML content for each page.
            *   `_extract_main()`: isolates the main content area.
            *   `rewrite_asset_links_inplace()`: updates links to point to local assets. [<src/htmldownloader/cli.py>, line 476]
            *   `download_one()`: downloads linked assets (images, css) to local disk. [<src/htmldownloader/cli.py>, line 176]
            *   `iter_asset_urls()`: finds all assets in the page. [<src/htmldownloader/cli.py>, line 444]

*   **Output Generation**
    *   `DoxygenExportDownloader` (finalization)
        *   calls:
            *   `build_toc_html()`: Generates `toc.html`.
            *   `build_frameset_index()`: Generates `index.html`.
            *   `post_process()`: Runs cleaning pipeline.

## 5. Resource Explorer Workflow
This workflow handles TI Resource Explorer wrapper pages.

*   **Module Selection & Delegation**
    *   `ResourceExplorerDownloader`: Wrapper detection for Resource Explorer. [<src/htmldownloader/cli.py>, lines 4536-4625]
    *   `run()`: Detects inner content type and delegates. [<src/htmldownloader/cli.py>, lines 4593-4620]
        *   description: Handles initial wrapper page, often finding an iframe with the real content.
        *   calls:
            *   `_select_module()`: attempts to find a supported module (e.g., Doxygen) in static HTML.
            *   `_render_with_playwright()`: renders page if static check fails.
            *   `RMModuleDoxigen.run()`: Delegates execution if Doxygen module is found. [<src/htmldownloader/cli.py>, lines 4520-4530]
                *   calls: `DoxygenExportDownloader(...).run()`: Instantiates and runs the Doxygen downloader.

## 6. Post-Processing Pipeline
Shared cleaning and validation steps for all downloaders.

*   **Pipeline Execution**
    *   `BaseDownloader.post_process()`: Executes list of cleanup functions. [<src/htmldownloader/cli.py>, lines 800-809]
    *   `BaseDownloader` methods (examples):
        *   `_clean_document_style()`: removes unwanted CSS/style tags.
        *   `_normalize_document_links()`: ensures internal links point to correct anchors.
        *   `_remove_unused_images()`: deletes downloaded images not referenced in HTML.
        *   `_verify_toc_consistency()`: checks if TOC links match document anchors.
        *   `fix_heading_numbering()`: normalizes section numbering.
