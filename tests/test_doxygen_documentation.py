"""
@file test_doxygen_documentation.py
@brief Validate Doxygen documentation coverage for Python sources under src/.
@details Enforces presence of module/function/class docstrings and module-level exported variable tags.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src" / "htmldownloader"


def _iter_python_files() -> list[Path]:
    """
    @brief Return project Python source files to audit.
    @details Enumerates non-cache Python files from src/htmldownloader.
    @return list[Path] Ordered list of file paths under audit.
    """
    return sorted(
        path
        for path in SRC_ROOT.rglob("*.py")
        if "__pycache__" not in path.parts
    )


def _module_level_variable_names(tree: ast.Module) -> list[str]:
    """
    @brief Extract module-level variable names defined by assignment.
    @details Collects names from Assign/AnnAssign nodes while skipping private underscore-prefixed names.
    @param tree Parsed module AST.
    @return list[str] Sorted module variable names expected to have @var tags.
    """
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    names.add(target.id)
        elif isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and not target.id.startswith("_"):
                names.add(target.id)
    return sorted(names)


def test_python_sources_have_doxygen_docstrings() -> None:
    """
    @brief Verify module, function, and class Doxygen docstrings.
    @details Checks each Python source file has module docstring and each class/function includes @brief and @details tags.
    @return None Returns None after successful assertions.
    """
    missing: list[str] = []
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        rel = path.relative_to(PROJECT_ROOT)

        module_doc = ast.get_docstring(tree) or ""
        if "@brief" not in module_doc or "@details" not in module_doc:
            missing.append(f"{rel}: module docstring missing @brief/@details")

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                doc = ast.get_docstring(node) or ""
                if "@brief" not in doc or "@details" not in doc:
                    missing.append(
                        f"{rel}:{node.lineno} {node.name} missing @brief/@details"
                    )

    assert not missing, "\n".join(missing)


def test_python_sources_have_module_var_doxygen_tags() -> None:
    """
    @brief Verify module-level exported variables expose Doxygen @var tags.
    @details Matches each exported module variable against `#: @var <name>` metadata comments in source text.
    @return None Returns None after successful assertions.
    """
    missing: list[str] = []
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        rel = path.relative_to(PROJECT_ROOT)
        names = _module_level_variable_names(tree)
        for name in names:
            if not re.search(
                rf"^#:\s*@var\s+{re.escape(name)}\b", source, flags=re.MULTILINE
            ):
                missing.append(f"{rel}: missing #: @var tag for {name}")

    assert not missing, "\n".join(missing)
