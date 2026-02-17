#!/usr/bin/env bash
#
# @file doxygen.sh
# @brief Generate Doxygen documentation for project sources in src/.
# @details Builds HTML and LaTeX artifacts using system-installed doxygen, derives Markdown
# from generated HTML, and normalizes outputs under doxygen/{html,markdown,pdf}.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/src"
OUTPUT_DIR="${SCRIPT_DIR}/doxygen"
PDF_DIR="${OUTPUT_DIR}/pdf"
LATEX_TMP_DIR="latex_build"
DOXYFILE_TMP="$(mktemp /tmp/htmldownloader-doxygen.XXXXXX)"

cleanup() {
  # @brief Remove temporary Doxygen configuration file.
  # @details Ensures mktemp artifact cleanup on normal exit and error paths.
  rm -f "${DOXYFILE_TMP}"
}

require_command() {
  # @brief Validate required command presence in PATH.
  # @details Fails fast with explicit error when command resolution is not possible.
  local name="$1"
  command -v "${name}" >/dev/null 2>&1 || {
    printf 'ERROR: %s command not found in PATH.\n' "${name}" >&2
    exit 1
  }
}

write_doxyfile() {
  # @brief Emit Doxygen configuration optimized for source-complete extraction.
  # @details Configures recursive Python parsing, graph outputs, HTML and LaTeX generation.
  cat >"${DOXYFILE_TMP}" <<EOF
PROJECT_NAME           = "HtmlDownloader"
PROJECT_BRIEF          = "Generated API documentation"
OUTPUT_DIRECTORY       = ${OUTPUT_DIR}
CREATE_SUBDIRS         = NO
ALLOW_UNICODE_NAMES    = YES
OUTPUT_LANGUAGE        = English
QUIET                  = YES
WARN_IF_UNDOCUMENTED   = YES
WARN_IF_DOC_ERROR      = YES
WARN_NO_PARAMDOC       = YES
WARN_AS_ERROR          = NO

INPUT                  = ${SOURCE_DIR}
RECURSIVE              = YES
FILE_PATTERNS          = *.py
EXCLUDE_PATTERNS       = */__pycache__/*
EXTENSION_MAPPING      = py=Python

EXTRACT_ALL            = YES
EXTRACT_PRIVATE        = YES
EXTRACT_STATIC         = YES
EXTRACT_LOCAL_CLASSES  = YES
EXTRACT_LOCAL_METHODS  = YES
HIDE_UNDOC_MEMBERS     = NO
HIDE_UNDOC_CLASSES     = NO

SOURCE_BROWSER         = YES
INLINE_SOURCES         = YES
REFERENCED_BY_RELATION = YES
REFERENCES_RELATION    = YES
CALL_GRAPH             = YES
CALLER_GRAPH           = YES
CLASS_GRAPH            = YES
COLLABORATION_GRAPH    = YES
DIRECTORY_GRAPH        = YES
GROUP_GRAPHS           = YES
INCLUDE_GRAPH          = YES
INCLUDED_BY_GRAPH      = YES
GRAPHICAL_HIERARCHY    = YES
DOT_IMAGE_FORMAT       = svg
HAVE_DOT               = YES

GENERATE_HTML          = YES
HTML_OUTPUT            = html
GENERATE_TREEVIEW      = YES
FULL_SIDEBAR           = YES
HTML_DYNAMIC_SECTIONS  = YES

GENERATE_LATEX         = YES
LATEX_OUTPUT           = ${LATEX_TMP_DIR}
USE_PDFLATEX           = YES
LATEX_BATCHMODE        = YES
COMPACT_LATEX          = YES
EOF
}

generate_markdown_from_html() {
  # @brief Convert generated HTML pages into Markdown artifacts.
  # @details Performs deterministic HTML tag stripping and writes one markdown file per HTML file.
  mkdir -p "${OUTPUT_DIR}/markdown"
  python3 - <<'PY'
import html
import re
from pathlib import Path

output_dir = Path("doxygen")
html_dir = output_dir / "html"
md_dir = output_dir / "markdown"
md_dir.mkdir(parents=True, exist_ok=True)

for html_path in html_dir.glob("*.html"):
    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    body = re.search(r"<body[^>]*>(.*)</body>", raw, re.IGNORECASE | re.DOTALL)
    content = body.group(1) if body else raw
    content = re.sub(r"<script.*?</script>", "", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<style.*?</style>", "", content, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", "\n", content)
    text = html.unescape(text)
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    title_match = re.search(r"<title>(.*?)</title>", raw, re.IGNORECASE | re.DOTALL)
    title = html.unescape(title_match.group(1).strip()) if title_match else html_path.stem
    markdown = f"# {title}\n\n{text}\n"
    (md_dir / f"{html_path.stem}.md").write_text(markdown, encoding="utf-8")
PY
}

main() {
  # @brief Execute documentation pipeline from source scan to output materialization.
  # @details Validates tools, resets output tree, runs doxygen, builds PDF, derives markdown, and reports destinations.
  require_command "doxygen"
  require_command "make"
  require_command "pdflatex"

  rm -rf "${OUTPUT_DIR}"
  mkdir -p "${OUTPUT_DIR}" "${PDF_DIR}"

  write_doxyfile
  doxygen "${DOXYFILE_TMP}"
  make --silent -i -C "${OUTPUT_DIR}/${LATEX_TMP_DIR}" >/dev/null 2>&1 || true

  if [ ! -f "${OUTPUT_DIR}/${LATEX_TMP_DIR}/refman.pdf" ]; then
    printf '%s\n' "ERROR: PDF generation failed (refman.pdf not found)." >&2
    exit 1
  fi

  cp "${OUTPUT_DIR}/${LATEX_TMP_DIR}/refman.pdf" "${PDF_DIR}/refman.pdf"
  generate_markdown_from_html
  rm -rf "${OUTPUT_DIR:?}/${LATEX_TMP_DIR}"

  printf '%s\n' "Documentation generated in:"
  printf ' - %s\n' "${OUTPUT_DIR}/html"
  printf ' - %s\n' "${OUTPUT_DIR}/markdown"
  printf ' - %s\n' "${PDF_DIR}"
}

trap cleanup EXIT
main "$@"
