"""Small shared utilities."""
from __future__ import annotations

from datetime import datetime, timezone
import logging
import os
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent / "syscorex.log"


def configure_logging() -> None:
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s UTC %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )


def clear_screen() -> None:
    """Clear an interactive terminal; do nothing in non-interactive sessions."""
    if not os.isatty(0) or not os.isatty(1):
        return
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title: str) -> None:
    print("\n" + "=" * 48)
    print(title)
    print("=" * 48)


def log_action(action: str) -> None:
    configure_logging()
    logging.info("%s", action)


def format_bytes(size: int | float) -> str:
    if size < 0:
        return "0 B"
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if value < 1024 or unit == "PB":
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{value:.2f} PB"
