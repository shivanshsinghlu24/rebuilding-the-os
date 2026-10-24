"""Safe, defensive process inspection and termination helpers."""
from __future__ import annotations

from dataclasses import dataclass
import os
import psutil


class ProcessManagerError(RuntimeError):
    """Raised when a process operation cannot be completed safely."""


@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float


def list_processes() -> list[ProcessInfo]:
    """Return process information, skipping processes that disappear mid-scan."""
    rows: list[ProcessInfo] = []
    for proc in psutil.process_iter(attrs=["pid", "name", "memory_percent"]):
        try:
            info = proc.info
            # Non-blocking CPU sampling; readings may be 0.0 on the first sample.
            cpu = proc.cpu_percent(interval=None)
            rows.append(ProcessInfo(
                pid=int(info["pid"]),
                name=info.get("name") or "<unknown>",
                cpu_percent=float(cpu),
                memory_percent=float(info.get("memory_percent") or 0.0),
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, TypeError, ValueError):
            continue
    return sorted(rows, key=lambda item: item.pid)


def terminate_process(pid: int, timeout: float = 3.0) -> None:
    """Request termination and wait briefly; refuse to terminate this process."""
    if not isinstance(pid, int) or pid <= 0:
        raise ProcessManagerError("PID must be a positive integer.")
    if pid == os.getpid():
        raise ProcessManagerError("Refusing to terminate SysCoreX itself.")
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        try:
            proc.wait(timeout=timeout)
        except psutil.TimeoutExpired:
            raise ProcessManagerError(f"PID {pid} did not exit within {timeout:g}s. It was not force-killed.")
    except psutil.NoSuchProcess as exc:
        raise ProcessManagerError(f"Process {pid} no longer exists.") from exc
    except psutil.AccessDenied as exc:
        raise ProcessManagerError(f"Permission denied when terminating PID {pid}.") from exc
