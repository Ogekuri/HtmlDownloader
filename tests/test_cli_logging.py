from htmldownloader.cli import build_arg_parser, Logger


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

    args_debug = parser.parse_args([
        "--from-url",
        "http://example.com",
        "--to-dir",
        "/tmp/out",
        "--debug",
    ])
    assert args_debug.debug is True
    assert args_debug.verbose is False


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
