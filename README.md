# PC Resource Manager

A cross-platform desktop application for monitoring system resources (CPU, RAM, Disk, Network) and managing processes, built with GTK4 and PyGObject.

## Features

- **Dashboard**: Real-time CPU (per-core), RAM, Swap, Network I/O, Disk I/O, and Battery monitoring
- **Process Manager**: View all running processes, sort by CPU/Memory/Name/PID, and kill processes
- **Disk Monitor**: View disk usage for all partitions
- **System Info**: Display system information (OS, CPU cores, memory)
- **Dark Mode**: Modern dark theme with visual progress bars

## Installation

### macOS (Homebrew)

```bash
# Install GTK4, PyGObject, and create venv with psutil
brew install gtk4 adwaita pygobject3

# Create venv and install psutil
python3 -m venv venv
venv/bin/pip install psutil

# Run the application
./run.sh main.py
```

### Linux

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-psutil
python3 main.py
```

#### Fedora
```bash
sudo dnf install python3-gobject gtk4 python3-psutil
python3 main.py
```

#### Arch Linux
```bash
sudo pacman -S python-gobject gtk4 python-psutil
python3 main.py
```

### Windows (MSYS2)

1. Download and install [MSYS2](https://www.msys2.org/)

2. Open MSYS2 terminal and run:
```bash
pacman -S mingw-w64-x86_64-python \
    mingw-w64-x86_64-python-gobject \
    mingw-w64-x86_64-gtk4 \
    mingw-w64-x86_64-adwaita-icon-theme \
    mingw-w64-x86_64-python-psutil
```

3. Run the application:
```bash
python main.py
```

## Running the Application

```bash
# macOS - use the provided script (sets up GTK4 environment)
./run.sh main.py

# Linux
python3 main.py

# Alternatively on macOS with uv - set PYTHONPATH first
export PYTHONPATH="/opt/homebrew/lib/python3.13/site-packages"
uv run python main.py
```

## Project Structure

```
pc-resource-manager/
├── main.py              # Main GTK4 application
├── monitor_logic.py     # System monitoring logic (psutil)
├── styles.css           # Dark mode CSS styling
├── run.sh               # macOS run script
├── pyproject.toml       # Project configuration (uv)
└── README.md            # This file
```

## Controls

- **Dashboard**: Automatically updates every second
- **Processes**: 
  - Use dropdown to sort by CPU/Memory/Name/PID
  - Click "Refresh" to reload the process list
  - Select a process and click "Kill Selected Process" to terminate
- **Disks**: Shows usage for all mounted partitions
- **System Info**: Displays static system information

## License

MIT License
