# PC Resource Manager

A cross-platform desktop application for monitoring system resources (CPU, RAM, Disk, Network) and managing processes, built with GTK4 and PyGObject.

## Features

- **Dashboard**: 
  - Real-time **CPU (per-core)** monitoring with individual progress bars
  - **Live Graphs** for CPU and RAM usage history
  - **Memory & Swap**: Detailed breakdown of physical and swap memory usage
  - **Network I/O**: Real-time upload/download speeds with history graphs
  - **Disk I/O**: Live read/write performance monitoring
- **Process Manager**: 
  - Comprehensive list of running processes
  - Sort by CPU, Memory, Name, or PID
  - Search/Filter capabilities and one-click process termination
- **GPU Monitoring**: Multi-vendor support (NVIDIA, AMD, Intel, Apple Silicon) for load and memory tracking
- **Storage**: Detailed disk usage for all mounted partitions
- **System Info**: Deep-dive into OS, kernel, and hardware specifications
- **Modern UI**: Polished GTK4/Adwaita interface with:
  - Linear gradients and glassmorphism effects
  - Responsive card-based layout
  - High-performance custom drawing for real-time graphs
  - Native dark mode support

## Installation

### macOS (Homebrew)

```bash
# Install GTK4 and PyGObject via Homebrew
brew install gtk4 adwaita pygobject3

# Run the application (run.sh creates uv venv with psutil automatically)
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
# macOS - use the provided script (creates uv venv and sets up GTK4 environment)
./run.sh main.py

# Linux
python3 main.py
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

- **Dashboard**: 
  - Real-time updates every 1 second
  - Interactive **live graphs** for CPU, RAM, Network, and Disk I/O
  - Per-core CPU utilization with individual visual progress bars
- **Processes**: 
  - Use the **Sort** dropdown to prioritize by CPU, Memory, Name, or PID
  - Click "Refresh" to update the process snapshot
  - Select any process and use the "Kill Process" button (with confirmation) to safely terminate it
- **Storage**: Real-time disk capacity monitoring for all mounted devices
- **System**: Detailed overview of hardware and OS specifications

## License

MIT License
