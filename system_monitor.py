import psutil
import time

def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    return cpu, memory, disk


def display_stats():
    while True:
        cpu, memory, disk = get_system_stats()

        print("\n===== SYSTEM MONITOR =====")
        print(f"CPU Usage: {cpu}%")
        print(f"Memory Usage: {memory}%")
        print(f"Disk Usage: {disk}%")

        time.sleep(2)
