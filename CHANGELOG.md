# Changelog

## [0.1.2](https://github.com/Ogekuri/HtmlDownloader/compare/v0.1.0..v0.1.2) - 2026-02-27
### ⛰️  Features
- Update workflow.

### 🐛  Bug Fixes
- unify TOC generation for full export [useReq] *(doxygen-export)*
  - Use nav-tree TOC parsing for both limited and full Doxygen runs.
  - Preserve limit behavior while fixing full-export tree/title mismatches.
  - Add regression test for no-limit nav-tree labels/hierarchy.
  - Update WORKFLOW.md and regenerate REFERENCES.md.

### 🚜  Changes
- renumber TOC/document heading IDs to title-N [useReq] *(anchors)*
  - Update SRS anchor requirements from GUID format to progressive title-N format.
  - Implement BaseDownloader post-process renumbering step to rewrite TOC/document fragments.
  - Align Doxygen and Resource Explorer limit tests with progressive title-N anchors.
  - Refresh WORKFLOW and regenerate REFERENCES for updated call graph/evidence.
- BREAKING CHANGE: switch generated IDs to UUID GUID format [useReq] *(anchors)*
  - Update REQUIREMENTS IDs DES-009, REQ-007, and TST-002 for GUID anchors.
  - Implement shared generate_guid_anchor() and apply it in TI/Doxygen download flows.
  - Refactor limit tests to enforce guid-<uuid>-guid-<uuid> anchors and reject page-* IDs.
  - Refresh WORKFLOW.md and regenerate REFERENCES.md.
- serialize toc list items per line [useReq] *(cli)*
  - Update REQ-007 and TST-004 for toc list serialization behavior.
  - Format build_toc_html output with one <li> per dedicated line.
  - Add unit test coverage for toc html serialization.
  - Update WORKFLOW and regenerate REFERENCES for traceability.

### 📚  Documentation
- Update TODO.md file.
- recreate SRS structure in English [useReq] *(requirements)*
  - Preserve existing requirement IDs and canonicalize RFC 2119 syntax.
  - Reorganize sections for parser-oriented structure and atomicity.
  - Add evidence-backed requirements from workflow and runtime behavior.

## [0.1.0](https://github.com/Ogekuri/HtmlDownloader/releases/tag/v0.1.0) - 2026-02-24
### ⛰️  Features
- add req/ dir. *(core)*
- add examples download and test. *(core)*
- add assets cleanup. *(core)*
- implement new version check. *(core)*
- implement --version command. *(core)*

### 🐛  Bug Fixes
- Fix .g.conf file. *(core)*
- fix workflow script. *(core)*
- resolve static-check defects [2026-02-20 14:33:17] *(cli)*
- WORKFLOW.md position. *(core)*

### 🚜  Changes
- add root doxygen generator and spec updates [2026-02-17 15:30:30] *(doxygen)*
- remove pdoc scope and enforce Doxygen coverage [2026-02-17 15:11:29] *(docs)*
- align requirements and doxygen docs [2026-02-15 19:48:02] *(cli)*
- regenerate Doxygen-style source documentation [2026-02-15 19:34:30] *(cli)*

### 📚  Documentation
- regenerate runtime model from source [2026-02-20 15:17:52] *(workflow)*
- regenerate repository index [2026-02-19 17:52:19] *(references)*
- regenerate runtime execution model [2026-02-19 17:48:07] *(workflow)*
- generate REFERENCES.md from source scan [2026-02-15 19:19:55] *(references)*
- update technical call tree from source analysis [2026-02-15 18:55:48] *(workflow)*
- update workflow analysis [2026-02-09 10:19:08] *(core)*
- Update technical workflow documentation from source analysis [2026-02-09 09:20:12] *(docs)*
- Create WORKFLOW.md analysis [2026-02-08 19:01:01] *(core)*


# History

- \[0.1.0\]: https://github.com/Ogekuri/HtmlDownloader/releases/tag/v0.1.0
- \[0.1.2\]: https://github.com/Ogekuri/HtmlDownloader/releases/tag/v0.1.2

[0.1.0]: https://github.com/Ogekuri/HtmlDownloader/releases/tag/v0.1.0
[0.1.2]: https://github.com/Ogekuri/HtmlDownloader/compare/v0.1.0..v0.1.2
