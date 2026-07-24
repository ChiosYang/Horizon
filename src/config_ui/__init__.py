"""Loopback-only browser shell for editing Horizon configuration."""

from .app import create_app
from .security import SessionStore

__all__ = ["SessionStore", "create_app"]
