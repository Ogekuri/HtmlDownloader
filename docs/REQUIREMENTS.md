---
title: "HtmlDownloader Requirements"
description: Software requirements specification
version: "0.47"
date: "2026-02-25"
author: "Ogekuri"
scope:
  paths:
    - "src/**/*.py"
    - ".github/workflows/**/*.yml"
  excludes:
    - ".git/**"
    - ".venv/**"
visibility: "draft"
tags: ["markdown", "requirements"]
---

# HtmlDownloader Requirements
**Version**: 0.47  
**Author**: Ogekuri  
**Date**: 2026-02-25

## 1. Introduction

### 1.1 Document authoring rules
- The SRS MUST be written in English.
- Each requirement line MUST use this format: `- **<ID>**: <RFC2119 keyword> <single-sentence requirement>.`
- RFC 2119 keywords MUST be limited to `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY`.
- Existing requirement IDs MUST remain unchanged and unique.

### 1.2 Project scope
HtmlDownloader is a CLI program that exports online documentation into an offline package composed of `document.html`, `toc.html`, `index.html`, and local `assets/`.

### 1.3 Repository structure
```text
HtmlDownloader/
├── docs/
│   ├── REQUIREMENTS.md
│   ├── REFERENCES.md
│   └── WORKFLOW.md
├── .github/
│   └── workflows/
│       └── release-uvx.yml
├── src/
│   └── htmldownloader/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── version.py
├── requirements.txt
├── pyproject.toml
└── doxygen.sh
```

### 1.4 Performance note
No explicit performance optimizations identified.

## 2. Project Requirements

### 2.1 Project capabilities
- **PRJ-001**: MUST provide a CLI workflow that exports TI `document-viewer` pages into readable offline output.
- **PRJ-002**: MUST support aggregating Doxygen-exported sites into one offline document with an index.
- **PRJ-003**: MUST produce `document.html`, `toc.html`, `index.html`, and `assets/` in the destination directory.
- **PRJ-004**: MUST provide an automated GitHub Actions release pipeline for tagged package releases.

### 2.2 Project constraints
- **CTN-001**: MUST run on Python `>=3.8` and depend on `requests`, `beautifulsoup4`, `lxml`, `playwright`, and `tqdm`.
- **CTN-002**: MUST require Chromium installed through `playwright install chromium` for TI `document-viewer` extraction.
- **CTN-003**: MUST cap Doxygen crawling at 250 HTML pages.
- **CTN-004**: MUST resolve output paths to absolute paths and create missing destination directories.

## 3. Software Requirements

### 3.1 Architecture and implementation
- **DES-001**: MUST implement downloader types as `BaseDownloader` subclasses registered through `DownloaderRegistry`.
- **DES-002**: MUST store downloaded assets under `assets/<host>/<path>` using sanitized filenames and parent directory creation.
- **DES-003**: MUST use Playwright headless for TI extraction, including TOC expansion, section capture, local asset rewriting, and merged offline serialization.
- **DES-004**: MUST perform in-scope Doxygen crawling and build unified offline sections from fetched pages.
- **DES-005**: MUST download assets through reusable HTTP sessions with chunked streaming writes.
- **DES-006**: MUST combine URL matching and optional initial HTML probing to select the downloader or raise an explicit error.
- **DES-007**: MUST remove external stylesheet links, `<style>` blocks, and inline `style` attributes from exported `document.html`.
- **DES-008**: MUST generate `index.html` as a two-frame frameset with `toc.html` on the left and `document.html` on the right.
- **DES-009**: MUST apply optional TOC limiting in reading order, generate `document.html` from the same order, and before saving outputs renumber heading fragments as ordered `title-<n>` anchors with synchronized TOC/document references across downloader modules.
- **DES-010**: MUST extract Doxygen TOC with Playwright and support internal TOC-only execution that writes `toc_raw.html` and `toc_raw.txt`.
- **DES-011**: MUST extract expanded Doxygen TOC from `#nav-tree-contents > ul` and derive a hierarchical textual outline from that HTML.
- **DES-012**: MUST consolidate duplicate Doxygen TOC references so duplicate entries point to preserved exported anchors.
- **DES-013**: MUST remove source-page TOC/navigation elements from extracted Doxygen page content before document merge.
- **DES-014**: MUST execute a shared `post_process` pipeline after downloader output generation.
- **DES-015**: MUST verify TOC consistency by checking fragment target existence and TOC-label versus heading-text correspondence.
- **DES-016**: MUST verify TOC depth and emit a warning when depth exceeds six levels.
- **DES-017**: MUST prune TOC entries at depth `>=7` and strip numeric heading prefixes in TOC labels and document headings.
- **DES-018**: MUST execute `_clean_document_style` at pipeline start to remove stylesheet links, `<style>`, `style`, and `class` attributes from `document.html` and `toc.html`.
- **DES-019**: MUST enforce that TOC fragments resolve to headings or section/div containers containing headings, and exported headings are TOC-referenced.
- **DES-020**: MUST run `_test_toc_headings` to fail when anchors are missing, invalid, depth-mismatched, or headings are unreferenced.
- **DES-021**: MUST run `fix_heading_ref_position` to move fragment IDs from section/div containers onto target headings when needed.
- **DES-022**: MUST run `fix_heading_numbering` to strip prior numbering and reapply numbering from TOC depth unless numbering is disabled.
- **DES-023**: MUST normalize document links so only allowed external schemes or resolvable internal `#id` fragments retain clickable `href` values.
- **DES-024**: MUST implement `ResourceExplorerDownloader` with module selection and delegation.
- **DES-025**: MUST inject CSS borders for tables and non-table images through `_add_document_style`.
- **DES-026**: MUST remove unreferenced files under `assets/` using `document.html` references as retention criteria.
- **DES-027**: MUST deduplicate TOC entries by fragment in reading order and promote children of removed duplicates.
- **DES-028**: MUST convert Doxygen definition-list patterns to inline uppercase bold labels followed by `:` while preserving descriptive content.
- **DES-028.1**: MUST convert split textual definition-list patterns where the `:` marker appears in a separate paragraph.
- **DES-029**: MUST remove `assets/` when empty after output generation and cleanup, and MUST log removal under verbose mode.
- **DES-030**: MUST keep structured Doxygen documentation coverage for exported symbols in Python files under `src/`.
- **DES-031**: MUST include a root `doxygen.sh` script that generates Doxygen HTML, PDF, and Markdown output under `doxygen/` only.
- **DES-032**: MUST continue `post_process` execution after non-`_test_toc_headings` step failures while logging the failure in debug output.
- **DES-033**: MUST normalize asset image placement by moving nested image files to `assets/` root with UUID-suffixed names and updating HTML references.
- **DES-034**: MUST run release workflow on `vMAJOR.MINOR.PATCH` tags and gate release execution to commits contained in `origin/master`.
- **DES-035**: MUST build distributions with Python 3.11 and uv, attest artifacts, build changelog text, and publish release artifacts in GitHub Releases.

### 3.2 CLI and functional behavior
- **REQ-001**: MUST require `--from-url` and `--to-dir`, accept optional `--user-agent`, and create the destination directory when missing.
- **REQ-002**: MUST auto-detect downloader type and MUST fail explicitly when downloader type cannot be determined.
- **REQ-003**: MUST export TI content from the first TOC entry starting with `1 ` through `IMPORTANT NOTICE`, excluding the trailing TI disclaimer block.
- **REQ-004**: MUST export Doxygen pages within detected scope, rewrite assets to local paths, and generate `document.html`, `toc.html`, and `index.html`.
- **REQ-005**: MUST print selected downloader and output paths to stdout, and MUST print progress/check logs only when verbose or debug is enabled.
- **REQ-006**: MUST sanitize URL-derived filenames by replacing invalid filesystem characters and query-derived unsafe patterns.
- **REQ-007**: MUST generate a hierarchical TOC with `target="doc"` and title `TOC`, no extra "open full document" link, one serialized `<li>` per line, generated anchors in `title-<n>` format, and MUST NOT use `page-N`.
- **REQ-008**: MUST expose `--verbose` and `--debug`, with debug implying verbose and including additional diagnostic detail.
- **REQ-009**: MUST expose `--limit <max>` as a positive integer and MUST reject non-positive values at argument validation.
- **REQ-010**: MUST prepend Doxygen `document.html` with a document title extracted from `#titlearea`, `#projectname`, and `#projectnumber` when available.
- **REQ-012**: MUST execute post-processing automatically after downloader output generation.
- **REQ-013**: MUST expose `--disable-numbering` to disable numbering addition while keeping numbering-prefix removal.
- **REQ-014**: MUST report link-normalization aggregate counts in verbose logs and representative resolution examples in debug logs.
- **REQ-015**: MUST choose `ResourceExplorerDownloader` for `https://dev.ti.com/tirex/explore/node` URLs and fail if no compatible module activates.
- **REQ-016**: MUST activate `RMModuleDoxigen` when an iframe/frame exists under `div.css-1aefuid-contentContainer` and delegate execution to `DoxygenExportDownloader`.
- **REQ-017**: MUST expose `--version` and `--ver` that print only the current version and exit with code 0.
- **REQ-018**: MUST perform release-version availability check using `GET https://api.github.com/repos/Ogekuri/HtmlDownloader/releases/latest` with a 1-second timeout and no failure message on check errors.
- **REQ-019**: MUST print the upgrade advisory message when a newer remote version is detected.
- **REQ-020**: MUST expose `--upgrade` to run `python -m pip install --upgrade htmldownloader` and exit with subprocess status code.
- **REQ-021**: MUST skip `tests/test_examples_downloads.py` during default `pytest` runs unless explicitly enabled.
- **REQ-022**: MUST run Doxygen definition-list conversion in the TI downloader after document assembly and before post-processing.
- **REQ-023**: MUST print strict help text and exit 0 when executed without parameters.
- **REQ-024**: MUST print strict help with header, usage, example, fixed core options, and dynamically enumerated parser options.
- **REQ-025**: MUST keep Doxygen documentation coverage for Python exported symbols under `src/` in parser-friendly structured form.
- **REQ-026**: MUST have `./doxygen.sh` invoke system Doxygen and emit HTML, PDF, and Markdown documentation outputs for `src/`.
- **REQ-027**: MUST generate `toc.html` and `index.html` wrappers with `lang="it"` and Italian fallback text as implemented by template builders.

### 3.3 Evidence for newly added requirements
- Evidence [PRJ-004, DES-034, DES-035]: `.github/workflows/release-uvx.yml`, job `check-branch` and `build-release`, excerpt: `on.push.tags: v[0-9]+.[0-9]+.[0-9]+`, `if: needs.check-branch.outputs.is_master == 'true'`, `python-version: "3.11"`, `uses: actions/attest-build-provenance@v1`, `uses: softprops/action-gh-release@v2`.
- Evidence [DES-032]: `src/htmldownloader/cli.py`, symbol `BaseDownloader.post_process`, excerpt: `except Exception as e ... if func.__name__ == "_test_toc_headings": raise`.
- Evidence [DES-033]: `src/htmldownloader/cli.py`, symbol `_normalize_image_position`, excerpt: move nested assets with `uuid.uuid4().hex` and replace references in `document.html`, `toc.html`, `index.html`.
- Evidence [REQ-027]: `src/htmldownloader/cli.py`, symbols `build_toc_html` and `build_frameset_index`, excerpt: `<html lang="it">` and fallback text `Il browser non supporta i frame...`.

## 4. Test Requirements

### 4.1 Verification requirements
- **TST-001**: MUST verify TI export generates readable `document.html`, `index.html`, and `assets/` with local images and navigable heading anchors.
- **TST-002**: MUST verify Doxygen export respects the 250-page cap, generates section anchors in `title-<n>` format, and rewrites assets to local references.
- **TST-003**: MUST verify required CLI arguments, automatic downloader selection, and explicit error when no downloader matches.
- **TST-004**: MUST verify style stripping, TOC hierarchy, TOC title, TOC `<li>` line-by-line serialization, frame targeting, and two-frame `index.html` layout for both downloader families.
- **TST-005**: MUST verify TI TOC starts from the first numeric section, excludes trailing IMPORTANT NOTICE entry, and contains expected intermediate sections.
- **TST-006**: MUST verify each TI TOC link resolves to an existing `document.html` anchor and opens correctly in frame `doc`.
- **TST-007**: MUST verify TI output begins from first numeric section and excludes TI disclaimer paragraphs while preserving intended major section content.
- **TST-008**: MUST verify duplicated TI sections are not duplicated in `document.html` and duplicate TOC entries point to preserved anchors.
- **TST-009**: MUST verify TI `document.html` starts with one title line derived from TOC-first title or first section title.
- **TST-010**: MUST verify `--limit` truncates TOC and document sections consistently for both downloader families.
- **TST-011**: MUST verify Doxygen `--limit 30` preserves exactly the first 30 expected TOC/document entries in reading order and hierarchy.
- **TST-012**: MUST verify Doxygen document title extraction appears as first line in `document.html` for the AM64x API guide sample.
- **TST-013**: MUST verify internal Doxygen TOC-only flow generates `toc_raw.html` and `toc_raw.txt` matching reference fixtures, excluding API Reference subtree validation.
- **TST-014**: MUST verify TOC extraction from selector `#nav-tree-contents > ul` matches expected raw TOC fixtures under the defined test conditions.
- **TST-015**: MUST verify Doxygen duplicate TOC entries resolve to correct anchors and source TOC blocks are removed from merged page content.
- **TST-016**: MUST verify each Doxygen heading is TOC-referenced and each TOC fragment points to a heading or heading-containing container.
- **TST-017**: MUST verify each TI heading is TOC-referenced and each TOC fragment points to a heading or heading-containing container.
- **TST-018**: MUST verify `fix_heading_ref_position` results in TOC fragments targeting heading IDs, not section/div container IDs.
- **TST-019**: MUST verify numbering cleanup/rebuild behavior with and without `--disable-numbering` for both TOC labels and document headings.
- **TST-020**: MUST verify `tests/test_sprz457.py::test_sprz457_post_links` accepts only explicit-scheme external links or valid internal `#id` links.
- **TST-021**: MUST verify `tests/test_spradj8.py::test_spradj8_post_links` enforces the same link-normalization constraints as TST-020.
- **TST-022**: MUST verify `tests/test_api_guide_limit.py::test_api_guide_post_links` enforces the same link-normalization constraints as TST-020.
- **TST-023**: MUST verify Resource Explorer + RMModuleDoxigen delegation, `--limit 30` output integrity, and `resource-explorer` selection reporting.
- **TST-024**: MUST verify `--version` and `--ver` exit 0 and print only `<version>\n`.
- **TST-025**: MUST verify version-check behavior for API failure and newer-version success paths with expected output text.
- **TST-026**: MUST verify `--upgrade` executes pip-upgrade subprocess and exits with subprocess return code without requiring other arguments.
- **TST-027**: MUST verify `_deduplicate_toc_entries` removes duplicate fragments and promotes children while preserving reading order.
- **TST-028**: MUST verify TOC/heading coverage, unique fragments, label-heading correspondence, and limit conformance across all URLs in `examples.sh`.
- **TST-029**: MUST verify default `pytest` skips `tests/test_examples_downloads.py`, and explicit enabling executes it.
- **TST-030**: MUST verify exported symbols in `src/` comply with `.req/docs/Document_Source_Code_in_Doxygen_Style.md` Doxygen documentation requirements.
- **TST-031**: MUST verify `./doxygen.sh` generates expected Doxygen artifacts and configuration behavior under `doxygen/`.
- **TST-032**: MUST verify release workflow gating on `origin/master` and successful artifact publication for matching semantic-version tags.

## 5. Revision History
| Date | Version | Change summary |
|------|---------|----------------|
| 2026-02-25 | 0.48 | Replaced generated anchor format with ordered `title-<n>` IDs and required synchronized TOC/document renumbering across downloader modules. |
| 2026-02-25 | 0.47 | Updated anchor-generation requirements to mandate `guid-<uuid>-guid-<uuid>` format for generated downloader anchors and aligned verification expectations. |
| 2026-02-25 | 0.46 | Recreated SRS in English with preserved IDs, canonical atomic format, and evidence-backed additions from `src/` and `.github/workflows/`. |
| 2026-02-17 | 0.45 | Prior draft baseline before req-recreate restructuring. |
