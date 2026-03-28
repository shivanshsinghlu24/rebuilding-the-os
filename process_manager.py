import psutil

def list_processes():
    print("\nPID\tName\t\tCPU%")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            print(f"{proc.info['pid']}\t{proc.info['name']}\t{proc.info['cpu_percent']}")
        except:
            pass


def kill_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
        print(f"Process {pid} terminated.")
    except Exception as e:
        print("Error:", e)
