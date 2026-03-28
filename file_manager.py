import os

def list_files(path="."):
    files = os.listdir(path)
    for f in files:
        print(f)


def create_file(name):
    with open(name, 'w') as f:
        pass
    print(f"{name} created.")


def delete_file(name):
    try:
        os.remove(name)
        print(f"{name} deleted.")
    except Exception as e:
        print("Error:", e)
