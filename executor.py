import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True)
    except Exception as e:
        print("Error:", e)
