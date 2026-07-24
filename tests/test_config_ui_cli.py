from __future__ import annotations

from pathlib import Path
import socket
from unittest.mock import Mock
from urllib.parse import urlsplit

import pytest

from src.config_ui import cli


def test_parser_freezes_loopback_options_without_remote_host_flag():
    parser = cli.build_parser()
    option_strings = {
        option
        for action in parser._actions
        for option in action.option_strings
    }

    assert "--port" in option_strings
    assert "--config" in option_strings
    assert "--no-browser" in option_strings
    assert "--host" not in option_strings


@pytest.mark.parametrize("value", ["0", "65536", "-1", "not-a-number"])
def test_parser_rejects_invalid_ports(value: str):
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["--port", value])


def test_startup_url_keeps_token_in_fragment():
    url = cli.startup_url(8765, "one-time-secret")
    parsed = urlsplit(url)

    assert parsed.scheme == "http"
    assert parsed.hostname == cli.LOOPBACK_HOST
    assert parsed.port == 8765
    assert parsed.query == ""
    assert parsed.fragment == "bootstrap=one-time-secret"


def test_reserve_loopback_socket_reports_occupied_port():
    occupied = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    occupied.bind((cli.LOOPBACK_HOST, 0))
    occupied.listen(1)
    port = occupied.getsockname()[1]

    try:
        with pytest.raises(cli.PortUnavailableError, match="--port PORT"):
            cli.reserve_loopback_socket(port)
    finally:
        occupied.close()


def test_no_browser_prints_manual_url_without_calling_browser(capsys: pytest.CaptureFixture[str]):
    opener = Mock(return_value=True)
    url = "http://127.0.0.1:8765/#bootstrap=token"

    cli.present_startup_url(url, no_browser=True, browser_open=opener)

    opener.assert_not_called()
    assert url in capsys.readouterr().out


@pytest.mark.parametrize("side_effect", [False, RuntimeError("browser failed")])
def test_browser_open_failure_is_nonfatal_and_prints_url(
    side_effect: bool | Exception,
    capsys: pytest.CaptureFixture[str],
):
    opener = Mock(
        side_effect=side_effect if isinstance(side_effect, Exception) else None,
        return_value=side_effect if isinstance(side_effect, bool) else None,
    )
    url = "http://127.0.0.1:8765/#bootstrap=token"

    cli.present_startup_url(url, no_browser=False, browser_open=opener)

    assert url in capsys.readouterr().out


def test_successful_browser_open_does_not_print_token(capsys: pytest.CaptureFixture[str]):
    opener = Mock(return_value=True)

    cli.present_startup_url(
        "http://127.0.0.1:8765/#bootstrap=token",
        no_browser=False,
        browser_open=opener,
    )

    assert capsys.readouterr().out == ""


def test_main_resolves_config_once_and_uses_reserved_loopback_socket(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    listener = Mock()
    captured: dict[str, object] = {}

    def fake_reserve(port: int) -> Mock:
        captured["reserved_port"] = port
        return listener

    def fake_present(url: str, *, no_browser: bool) -> None:
        captured["url"] = url
        captured["no_browser"] = no_browser

    def fake_run(listener_arg: object, app: object, port: int) -> None:
        captured["listener"] = listener_arg
        captured["app"] = app
        captured["server_port"] = port

    config_path = tmp_path / "selected.json"
    monkeypatch.setattr(cli, "reserve_loopback_socket", fake_reserve)
    monkeypatch.setattr(cli, "present_startup_url", fake_present)
    monkeypatch.setattr(cli, "run_server", fake_run)

    result = cli.main(
        [
            "--port",
            "9876",
            "--config",
            str(config_path),
            "--no-browser",
        ]
    )

    assert result == 0
    assert captured["reserved_port"] == 9876
    assert captured["server_port"] == 9876
    assert captured["listener"] is listener
    assert captured["no_browser"] is True
    assert str(captured["url"]).startswith(
        f"http://{cli.LOOPBACK_HOST}:9876/#bootstrap="
    )
    assert "?" not in str(captured["url"])
    app = captured["app"]
    assert app.state.config_service.config_path == config_path.resolve()
    listener.close.assert_called_once()


def test_main_fails_actionably_when_port_is_occupied(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    def unavailable(_port: int) -> socket.socket:
        raise cli.PortUnavailableError("occupied")

    monkeypatch.setattr(cli, "reserve_loopback_socket", unavailable)

    result = cli.main(["--port", "9876", "--no-browser"])

    captured = capsys.readouterr()
    assert result == 2
    assert "127.0.0.1:9876 is already in use" in captured.err
    assert "--port PORT" in captured.err
    assert "bootstrap=" not in captured.err
