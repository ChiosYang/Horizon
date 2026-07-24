"""Command-line entry point for the loopback configuration editor."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
import socket
import sys
from collections.abc import Callable, Sequence
import webbrowser

import uvicorn

from .app import create_app
from .security import SessionStore


LOOPBACK_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


class PortUnavailableError(RuntimeError):
    """The requested loopback port could not be reserved."""


def port_number(value: str) -> int:
    """Parse a usable TCP port for argparse."""

    try:
        port = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("port must be an integer") from exc
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return port


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="horizon-config",
        description="Start Horizon's loopback-only configuration editor.",
    )
    parser.add_argument(
        "--port",
        type=port_number,
        default=DEFAULT_PORT,
        help=f"loopback port to use (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("data/config.json"),
        help="configuration file selected at startup (default: data/config.json)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="do not open a browser; print the one-time startup URL instead",
    )
    return parser


def reserve_loopback_socket(port: int) -> socket.socket:
    """Bind the fixed loopback host before presenting the startup URL."""

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        listener.bind((LOOPBACK_HOST, port))
        listener.listen(2048)
        listener.set_inheritable(True)
    except OSError as exc:
        listener.close()
        raise PortUnavailableError(
            f"{LOOPBACK_HOST}:{port} is unavailable. "
            "Choose a free port with --port PORT."
        ) from exc
    return listener


def startup_url(port: int, bootstrap_token: str) -> str:
    """Place the single-use credential in a URL fragment, never a query."""

    return f"http://{LOOPBACK_HOST}:{port}/#bootstrap={bootstrap_token}"


def present_startup_url(
    url: str,
    *,
    no_browser: bool,
    browser_open: Callable[[str], bool] = webbrowser.open,
) -> None:
    """Open the local page or print the URL when manual opening is needed."""

    if no_browser:
        print(f"Open this one-time local URL:\n{url}")
        return

    try:
        opened = browser_open(url)
    except Exception:
        opened = False
    if not opened:
        print(f"Browser auto-open failed. Open this one-time local URL:\n{url}")


def run_server(listener: socket.socket, app: object, port: int) -> None:
    """Run Uvicorn on an already-reserved loopback socket."""

    config = uvicorn.Config(
        app,
        host=LOOPBACK_HOST,
        port=port,
        access_log=False,
        server_header=False,
        log_config=None,
    )
    uvicorn.Server(config).run(sockets=[listener])


def main(argv: Sequence[str] | None = None) -> int:
    """Start the local editor and return a process exit status."""

    args = build_parser().parse_args(argv)
    config_path = args.config.resolve()
    sessions = SessionStore()
    token = sessions.bootstrap_token
    if token is None:  # Defensive: a newly created store always has a token.
        print("Unable to create a local editor startup token.", file=sys.stderr)
        return 1

    try:
        listener = reserve_loopback_socket(args.port)
    except PortUnavailableError:
        print(
            f"Unable to start Horizon Config: {LOOPBACK_HOST}:{args.port} "
            "is already in use. Choose another port with --port PORT.",
            file=sys.stderr,
        )
        return 2

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s %(message)s",
    )
    app = create_app(config_path, session_store=sessions)
    url = startup_url(args.port, token)
    present_startup_url(url, no_browser=args.no_browser)

    try:
        run_server(listener, app, args.port)
    finally:
        listener.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
