import pytest

from htmldownloader.cli import build_arg_parser, Logger
from htmldownloader.version import __version__


def test_arg_parser_supports_verbose_and_debug():
    parser = build_arg_parser()
    args_verbose = parser.parse_args([
        "--from-url",
        "http://example.com",
        "--to-dir",
        "/tmp/out",
        "--verbose",
    ])
    assert args_verbose.verbose is True
    assert args_verbose.debug is False
    assert args_verbose.limit is None

    args_debug = parser.parse_args([
        "--from-url",
        "http://example.com",
        "--to-dir",
        "/tmp/out",
        "--debug",
    ])
    assert args_debug.debug is True
    assert args_debug.verbose is False
    assert args_debug.limit is None

    args_limit = parser.parse_args([
        "--from-url",
        "http://example.com",
        "--to-dir",
        "/tmp/out",
        "--limit",
        "5",
    ])
    assert args_limit.limit == 5
    assert args_limit.verbose is False
    assert args_limit.debug is False


def test_logger_gating(capsys):
    base_log = Logger()
    base_log.verbose("v hidden")
    base_log.debug("d hidden")
    base_log.check("c hidden")
    captured = capsys.readouterr()
    assert captured.out == ""

    verbose_log = Logger(verbose=True)
    verbose_log.verbose("v shown")
    verbose_log.debug("d hidden")
    verbose_log.check("c shown")
    captured = capsys.readouterr()
    assert "v shown" in captured.out
    assert "c shown" in captured.out
    assert "d hidden" not in captured.out

    debug_log = Logger(debug=True)
    debug_log.verbose("v shown debug")
    debug_log.debug("d shown")
    debug_log.check("c shown debug")
    captured = capsys.readouterr()
    assert "v shown debug" in captured.out
    assert "d shown" in captured.out
    assert "c shown debug" in captured.out


@pytest.mark.parametrize("flag", ["--version", "--ver"])
def test_cli_version_flag_exits_and_prints_version(capsys, flag):
    parser = build_arg_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args([flag])
    assert exc.value.code == 0

    captured = capsys.readouterr()
    assert captured.out == f"{__version__}\n"
    assert captured.err == ""
