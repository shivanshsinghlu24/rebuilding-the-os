"""SysCoreX: a cross-platform Python system-management toolkit."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from file_manager import FileManagerError, create_file, delete_file, list_files, read_file, write_file
from process_manager import ProcessManagerError, list_processes, terminate_process
from system_monitor import display_stats, get_system_stats
from utils import log_action, print_header

MENU = """\n==== SysCoreX ====
1. System overview
2. Live system monitor
3. List processes
4. Terminate a process
5. List files
6. Create a file
7. Read a text file
8. Write/append a text file
9. Delete a file
10. Help
0. Exit
"""


def ask(prompt: str) -> str:
    return input(prompt).strip()


def run_menu() -> int:
    print_header("SysCoreX | System Management Toolkit")
    print("Tip: type a menu number. Type 0 to exit.\n")
    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        try:
            if choice in {"0", "10", "help", "h"}:
                if choice == "0":
                    print("Goodbye!")
                    return 0
                show_help()
            elif choice == "1":
                stats = get_system_stats()
                print_header("System Overview")
                print(f"Platform: {stats.platform}")
                print(f"CPU cores: {stats.cpu_count} (logical)")
                print(f"CPU usage: {stats.cpu_percent:.1f}%")
                print(f"Memory: {stats.memory_used} / {stats.memory_total} ({stats.memory_percent:.1f}%)")
                print(f"Disk ({stats.disk_path}): {stats.disk_used} / {stats.disk_total} ({stats.disk_percent:.1f}%)")
                log_action("Viewed system overview")
            elif choice == "2":
                display_stats()
                log_action("Used live system monitor")
            elif choice == "3":
                rows = list_processes()
                print_header(f"Processes ({len(rows)})")
                print(f"{'PID':>8}  {'CPU %':>6}  {'MEM %':>6}  NAME")
                for row in rows:
                    print(f"{row.pid:>8}  {row.cpu_percent:>6.1f}  {row.memory_percent:>6.1f}  {row.name}")
                log_action("Listed processes")
            elif choice == "4":
                raw = ask("PID to terminate: ")
                pid = int(raw)
                confirm = ask(f"Terminate process {pid}? Type 'yes' to confirm: ").lower()
                if confirm == "yes":
                    terminate_process(pid)
                    print(f"Termination requested for PID {pid}.")
                    log_action(f"Requested termination of PID {pid}")
                else:
                    print("Cancelled.")
            elif choice == "5":
                path = ask("Directory path (default .): ") or "."
                entries = list_files(path)
                print_header(f"Files in {Path(path).resolve()}")
                for entry in entries:
                    kind = "DIR " if entry.is_dir else "FILE"
                    size = "—" if entry.is_dir else entry.size_human
                    print(f"{kind:4}  {size:>10}  {entry.name}")
                log_action(f"Listed directory {Path(path).resolve()}")
            elif choice == "6":
                path = ask("New file path: ")
                create_file(path)
                print(f"Created: {path}")
                log_action(f"Created file {path}")
            elif choice == "7":
                path = ask("Text file path: ")
                print(read_file(path))
                log_action(f"Read file {path}")
            elif choice == "8":
                path = ask("Text file path: ")
                mode = ask("Mode: [w] overwrite or [a] append (default a): ").lower() or "a"
                if mode not in {"w", "a"}:
                    print("Choose 'w' or 'a'.")
                    continue
                print("Enter text. A line containing only .END finishes input.")
                lines = []
                while True:
                    line = input()
                    if line == ".END":
                        break
                    lines.append(line)
                write_file(path, "\n".join(lines) + ("\n" if lines else ""), append=(mode == "a"))
                print("File saved.")
                log_action(f"{'Appended to' if mode == 'a' else 'Wrote'} file {path}")
            elif choice == "9":
                path = ask("File path to delete: ")
                confirm = ask(f"Permanently delete {path}? Type 'yes' to confirm: ").lower()
                if confirm == "yes":
                    delete_file(path)
                    print("File deleted.")
                    log_action(f"Deleted file {path}")
                else:
                    print("Cancelled.")
            else:
                print("Invalid option. Enter a listed number or 10 for help.")
        except (ValueError, FileManagerError, ProcessManagerError, OSError, PermissionError) as exc:
            print(f"Error: {exc}")
        except KeyboardInterrupt:
            print("\nInterrupted. Returning to menu; choose 0 to exit.")
        except Exception as exc:  # keep the interactive shell usable for unexpected OS-specific errors
            print(f"Unexpected error ({type(exc).__name__}): {exc}")


def show_help() -> None:
    print_header("Help & Safety")
    print("SysCoreX provides system monitoring, process inspection and basic file operations.")
    print("It does not execute arbitrary shell commands and is not a bootable operating system.")
    print("Process termination and file deletion are destructive; review targets before confirming.")
    print("Use only on devices and files you are authorized to manage.")


def main() -> int:
    parser = argparse.ArgumentParser(description="SysCoreX system-management toolkit")
    parser.add_argument("--version", action="version", version="SysCoreX 1.0.0")
    parser.add_argument("--overview", action="store_true", help="print a one-time system overview and exit")
    args = parser.parse_args()
    if args.overview:
        stats = get_system_stats()
        print(f"SysCoreX system overview | {stats.platform}")
        print(f"CPU: {stats.cpu_percent:.1f}% | Memory: {stats.memory_percent:.1f}% | Disk: {stats.disk_percent:.1f}% ({stats.disk_path})")
        return 0
    try:
        return run_menu()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
