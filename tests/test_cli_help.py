import sys

from htmldownloader.cli import main
from htmldownloader.version import __version__


def test_cli_no_args_prints_strict_help_and_exits(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["htmldownloader"])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 0
    # Check header and key sections are present and in order
    out = captured.out
    assert out.startswith(f"htmldownloader ({__version__})\n\nUsage:\n"), "Header and Usage missing or malformed"
    assert "Example/Examples:" in out
    assert "Options:" in out
    # Core options lines
    assert "-h, --help" in out
    assert "--version, --ver" in out
    assert "--verbose" in out
    assert "--debug" in out