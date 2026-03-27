def is_safe(command):
    dangerous = ["rm -rf", "del /f", "shutdown", "format"]

    for cmd in dangerous:
        if cmd in command.lower():
            return False
    return True
