#!/bin/bash

# PC Resource Manager - Run Script
# Sets up environment for GTK4 on macOS

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: Use venv with Homebrew Python for GTK4 bindings + psutil
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    
    # Use the venv python which has psutil
    PYTHON="$SCRIPT_DIR/venv/bin/python"
    
    # Add Homebrew site-packages for GTK4
    export PYTHONPATH="/opt/homebrew/lib/python3.13/site-packages:$PYTHONPATH"
    export GTK_PATH="/opt/homebrew/opt/gtk4/lib/gtk-4.0"
    
    # Unset any explicit backend to let GTK auto-detect
    unset GDK_BACKEND
else
    PYTHON=python3
fi

# Run the application
exec "$PYTHON" "$@"
