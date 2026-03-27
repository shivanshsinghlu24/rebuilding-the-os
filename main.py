from command_parser import parse_command
from executor import execute_command
from monitor import show_system_stats
from security import is_safe

def main():
    print("Welcome to SmartShell (Type 'exit' to quit)\n")

    while True:
        user_input = input(">> ")

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "monitor":
            show_system_stats()
            continue

        command = parse_command(user_input)

        if is_safe(command):
            execute_command(command)
        else:
            print("⚠️ Warning: Potentially unsafe command blocked!")

if __name__ == "__main__":
    main()
