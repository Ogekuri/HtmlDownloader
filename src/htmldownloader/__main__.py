"""
@file __main__.py
@brief Module implementation for HtmlDownloader runtime.
@details Contains executable logic and internal helpers used by the CLI workflow.
@module_symbols functions=0 classes=0 variables=0
"""
from .cli import main
import sys


if __name__ == "__main__":
    sys.exit(main())
