"""
@file test_doxygen_script.py
@brief Validate root-level doxygen.sh documentation generation workflow.
@details Executes doxygen.sh and verifies HTML/PDF/Markdown artifacts under doxygen/.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

#: @var PROJECT_ROOT
#: @brief Absolute repository root directory.
#: @details Resolved from test file location for stable path joins.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

#: @var SCRIPT_PATH
#: @brief Absolute path of root-level doxygen.sh script.
#: @details Used as subprocess executable target.
SCRIPT_PATH = PROJECT_ROOT / "doxygen.sh"

#: @var OUTPUT_ROOT
#: @brief Absolute path of generated doxygen output root.
#: @details Contains html, markdown, and pdf output folders.
OUTPUT_ROOT = PROJECT_ROOT / "doxygen"


def _has_required_tools() -> bool:
    """
    @brief Check availability of required external commands.
    @details Verifies doxygen, make, and pdflatex command resolution in current PATH.
    @return bool True when all required commands are available; otherwise False.
    """
    required = ("doxygen", "make", "pdflatex")
    return all(shutil.which(name) for name in required)


@pytest.mark.skipif(not _has_required_tools(), reason="Missing doxygen/make/pdflatex tools")
def test_doxygen_script_generates_expected_outputs() -> None:
    """
    @brief Assert doxygen.sh generates HTML, PDF, and Markdown outputs.
    @details Runs root-level script, then validates required output directories and canonical files.
    @return None Returns None after assertions complete.
    @exception subprocess.CalledProcessError Raised when script exits with non-zero status.
    """
    subprocess.run(["bash", str(SCRIPT_PATH)], check=True, cwd=str(PROJECT_ROOT))

    assert (OUTPUT_ROOT / "html" / "index.html").is_file()
    assert (OUTPUT_ROOT / "pdf" / "refman.pdf").is_file()
    assert any((OUTPUT_ROOT / "markdown").glob("*.md"))
