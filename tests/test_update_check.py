import sys
from types import SimpleNamespace

import pytest

import htmldownloader.cli as cli
from htmldownloader.cli import build_arg_parser, check_for_new_version


class _DummyResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self):
        return self._payload


def test_update_check_prints_message_when_newer_version_available(monkeypatch, capsys):
    seen = {}

    def fake_get(url, timeout, headers=None):
        seen["url"] = url
        seen["timeout"] = timeout
        seen["headers"] = headers
        return _DummyResponse({"tag_name": "v0.0.2"})

    monkeypatch.setattr(cli.requests, "get", fake_get)

    check_for_new_version("htmldownloader", "0.0.1")

    out = capsys.readouterr().out
    assert "A new version of htmldownloader is available" in out
    assert "current 0.0.1" in out
    assert "latest 0.0.2" in out
    assert "htmldownloader --upgrade" in out

    assert seen["url"] == "https://api.github.com/repos/Ogekuri/HtmlDownloader/releases/latest"
    assert seen["timeout"] == cli.GITHUB_API_TIMEOUT_S


def test_update_check_is_silent_on_request_failure(monkeypatch, capsys):
    def fake_get(*args, **kwargs):
        raise RuntimeError("network down")

    monkeypatch.setattr(cli.requests, "get", fake_get)

    check_for_new_version("htmldownloader", "0.0.1")
    assert capsys.readouterr().out == ""


def test_update_check_is_silent_on_unparseable_version(monkeypatch, capsys):
    def fake_get(url, timeout, headers=None):
        return _DummyResponse({"tag_name": "not-a-version"})

    monkeypatch.setattr(cli.requests, "get", fake_get)

    check_for_new_version("htmldownloader", "0.0.1")
    assert capsys.readouterr().out == ""


def test_upgrade_flag_invokes_pip_and_exits(monkeypatch):
    calls = []

    def fake_run(argv):
        calls.append(argv)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    parser = build_arg_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--upgrade"])

    assert exc.value.code == 0
    assert calls == [
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "htmldownloader",
        ]
    ]
