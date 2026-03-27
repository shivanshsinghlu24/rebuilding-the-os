import psutil

def show_system_stats():
    print("\n--- System Stats ---")
    print("CPU Usage:", psutil.cpu_percent(), "%")
    print("Memory Usage:", psutil.virtual_memory().percent, "%")
    print("--------------------\n")
