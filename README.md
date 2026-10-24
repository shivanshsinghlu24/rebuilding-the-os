# SysCoreX — System Management Toolkit

SysCoreX is a lightweight, cross-platform Python command-line utility for inspecting system usage, viewing running processes, and performing guarded file operations. It is a practical systems-programming project, **not a bootable operating system or kernel**.

## Features

- System overview: platform, CPU, memory, and disk usage
- Live resource monitor (press `Ctrl+C` to return to the menu)
- Process listing with PID, CPU and memory usage
- Confirmed process termination with permission/error handling
- Directory listing with file sizes
- Create, read, write, append, and delete text files
- Input validation and safeguards against accidental overwrite/deletion
- Action logging to `syscorex.log`
- Cross-platform disk-root selection for Windows and Unix-like systems
- Basic automated tests

## Requirements

- Python 3.10 or newer
- `pip`
- Windows, macOS, or Linux. Android support depends on the Python environment and permissions.

## Installation

Clone the repository:

```bash
git clone https://github.com/shivanshsinghlu24/rebuilding-the-os.git
cd rebuilding-the-os
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\\Scripts\\Activate.ps1
```

macOS/Linux/Termux:

```bash
source .venv/bin/activate
```

Install the dependency:

```bash
python -m pip install -r requirements.txt
```

## Run

Interactive menu:

```bash
python main.py
```

One-time system overview:

```bash
python main.py --overview
```

Show version:

```bash
python main.py --version
```

## Menu

1. System overview
2. Live system monitor
3. List processes
4. Terminate a process (asks for confirmation)
5. List files
6. Create a file (will not overwrite an existing path)
7. Read a UTF-8 text file (limited to 1 MB)
8. Write or append a UTF-8 text file
9. Delete a file (asks for confirmation; directories are not deleted)
10. Help
0. Exit

## Tests

Run the test suite with:

```bash
python -m unittest discover -s tests -v
```

## Safety and limitations

- SysCoreX does not execute arbitrary shell commands. The original README mentioned natural-language command execution and unsafe-command detection, but those features were not present in the original source and are intentionally not claimed here.
- Process termination may require elevated permissions. SysCoreX does not force-kill a process if it fails to exit within the timeout.
- File deletion is permanent; review the path carefully before confirming.
- CPU percentages can initially show `0.0%` because process CPU sampling is non-blocking.
- System APIs and accessible disk roots vary by operating system and runtime.
- This project does not implement booting, a kernel, a scheduler, virtual memory, drivers, or a filesystem kernel. If the goal is a real OS from scratch, that is a separate project requiring a bootloader/toolchain and a low-level language such as C or Rust plus Assembly.

## Project structure

```text
rebuilding-the-os/
├── main.py
├── system_monitor.py
├── process_manager.py
├── file_manager.py
├── utils.py
├── requirements.txt
├── tests/
│   └── test_file_manager.py
├── README.md
├── LICENSE
└── .gitignore
```

## Contributing

Issues and pull requests are welcome. Run tests before submitting changes.

## License

MIT. See [LICENSE](LICENSE).
