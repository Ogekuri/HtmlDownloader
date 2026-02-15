"""
@file __init__.py
@brief Module implementation for HtmlDownloader runtime.
@details Contains executable logic and internal helpers used by the CLI workflow.
@module_symbols functions=0 classes=0 variables=1
@variables __all__
"""

from .version import __version__

from .cli import main  # riesportazione del punto di ingresso CLI

#: @var __all__ @brief Module-level variable `__all__`.
__all__ = ["__version__", "main"]
