"""Guarded file operations used by SysCoreX."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class FileManagerError(RuntimeError):
    """Raised when a requested file operation is invalid or unsafe."""


@dataclass(frozen=True)
class FileEntry:
    name: str
    is_dir: bool
    size: int

    @property
    def size_human(self) -> str:
        from utils import format_bytes
        return format_bytes(self.size)


def list_files(path: str | Path = ".") -> list[FileEntry]:
    target = Path(path).expanduser()
    if not target.exists():
        raise FileManagerError(f"Path does not exist: {target}")
    if not target.is_dir():
        raise FileManagerError(f"Not a directory: {target}")
    try:
        entries = []
        for item in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
            try:
                entries.append(FileEntry(item.name, item.is_dir(), 0 if item.is_dir() else item.stat().st_size))
            except OSError:
                entries.append(FileEntry(item.name, item.is_dir(), 0))
        return entries
    except PermissionError as exc:
        raise FileManagerError(f"Permission denied: {target}") from exc


def create_file(name: str | Path) -> Path:
    target = Path(name).expanduser()
    if target.exists():
        raise FileManagerError(f"Refusing to overwrite existing path: {target}")
    try:
        target.parent.mkdir(parents=False, exist_ok=True)
        with target.open("x", encoding="utf-8"):
            pass
        return target
    except FileExistsError as exc:
        raise FileManagerError(f"File already exists: {target}") from exc
    except IsADirectoryError as exc:
        raise FileManagerError(f"Path is a directory: {target}") from exc


def read_file(name: str | Path, max_bytes: int = 1_000_000) -> str:
    target = Path(name).expanduser()
    if not target.exists() or not target.is_file():
        raise FileManagerError(f"Not a file: {target}")
    try:
        if target.stat().st_size > max_bytes:
            raise FileManagerError(f"File exceeds the {max_bytes:,}-byte read limit.")
        return target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise FileManagerError("File is not valid UTF-8 text; binary files are not displayed.") from exc


def write_file(name: str | Path, content: str, append: bool = False) -> Path:
    target = Path(name).expanduser()
    if not target.exists() and not append:
        # exclusive creation ensures we don't accidentally replace a file created concurrently
        try:
            with target.open("x", encoding="utf-8") as handle:
                handle.write(content)
            return target
        except FileExistsError:
            pass
    if not target.exists() and append:
        raise FileManagerError("Cannot append: file does not exist. Create it first.")
    if not target.is_file():
        raise FileManagerError(f"Not a regular file: {target}")
    try:
        with target.open("a" if append else "w", encoding="utf-8") as handle:
            handle.write(content)
        return target
    except OSError as exc:
        raise FileManagerError(f"Could not write {target}: {exc}") from exc


def delete_file(name: str | Path) -> None:
    target = Path(name).expanduser()
    if not target.exists():
        raise FileManagerError(f"File does not exist: {target}")
    if not target.is_file() and not target.is_symlink():
        raise FileManagerError("Only files and symbolic links can be deleted; directories are not removed.")
    try:
        target.unlink()
    except OSError as exc:
        raise FileManagerError(f"Could not delete {target}: {exc}") from exc
