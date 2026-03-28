from process_manager import list_processes, kill_process
from file_manager import list_files, create_file, delete_file
from system_monitor import display_stats

def show_menu():
    print("\n==== SysCoreX ====")
    print("1. View System Monitor")
    print("2. List Processes")
    print("3. Kill Process")
    print("4. List Files")
    print("5. Create File")
    print("6. Delete File")
    print("7. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            display_stats()

        elif choice == "2":
            list_processes()

        elif choice == "3":
            pid = int(input("Enter PID: "))
            kill_process(pid)

        elif choice == "4":
            path = input("Enter path (default .): ") or "."
            list_files(path)

        elif choice == "5":
            name = input("Enter file name: ")
            create_file(name)

        elif choice == "6":
            name = input("Enter file name: ")
            delete_file(name)

        elif choice == "7":
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
