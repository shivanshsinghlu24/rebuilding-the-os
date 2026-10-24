"""Cross-platform system statistics and live monitor."""
from __future__ import annotations

import platform
import time
from dataclasses import dataclass

import psutil

from utils import format_bytes


@dataclass(frozen=True)
class SystemStats:
    platform: str
    cpu_count: int
    cpu_percent: float
    memory_used: str
    memory_total: str
    memory_percent: float
    disk_path: str
    disk_used: str
    disk_total: str
    disk_percent: float


def get_disk_path() -> str:
    """Return a root path that is appropriate for the current OS."""
    return "C:\\" if platform.system() == "Windows" else "/"


def get_system_stats() -> SystemStats:
    memory = psutil.virtual_memory()
    disk_path = get_disk_path()
    disk = psutil.disk_usage(disk_path)
    return SystemStats(
        platform=f"{platform.system()} {platform.release()}",
        cpu_count=psutil.cpu_count(logical=True) or 1,
        cpu_percent=psutil.cpu_percent(interval=0.2),
        memory_used=format_bytes(memory.used),
        memory_total=format_bytes(memory.total),
        memory_percent=memory.percent,
        disk_path=disk_path,
        disk_used=format_bytes(disk.used),
        disk_total=format_bytes(disk.total),
        disk_percent=disk.percent,
    )


def display_stats(interval: float = 2.0) -> None:
    """Display live stats until the user presses Ctrl+C or input is interrupted."""
    print("Live monitor started. Press Ctrl+C to return to the menu.")
    try:
        while True:
            stats = get_system_stats()
            print("\n===== SYSTEM MONITOR =====")
            print(f"Platform: {stats.platform}")
            print(f"CPU usage: {stats.cpu_percent:.1f}% ({stats.cpu_count} logical cores)")
            print(f"Memory usage: {stats.memory_used} / {stats.memory_total} ({stats.memory_percent:.1f}%)")
            print(f"Disk usage: {stats.disk_used} / {stats.disk_total} ({stats.disk_percent:.1f}%) on {stats.disk_path}")
            time.sleep(max(0.2, interval))
    except KeyboardInterrupt:
        print("\nMonitor stopped.")
