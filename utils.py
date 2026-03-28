import os
import datetime

def clear_screen():
    # Clears terminal screen (cross-platform)
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    print("\n" + "=" * 40)
    print(f"{title}")
    print("=" * 40)


def log_action(action):
    # Simple logging system
    with open("syscorex.log", "a") as log:
        log.write(f"{datetime.datetime.now()} - {action}\n")


def format_bytes(size):
    # Convert bytes to KB, MB, GB
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
