def parse_command(user_input):
    mappings = {
        "show files": "dir",
        "list files": "dir",
        "current directory": "cd",
        "make folder": "mkdir",
        "remove file": "del"
    }

    for key in mappings:
        if key in user_input.lower():
            return mappings[key]

    return user_input
