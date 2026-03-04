#!/bin/bash

# PC Resource Manager - Run Script
# Uses uv virtual environment with GTK4 support from Homebrew

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

if [[ "$OSTYPE" == "darwin"* ]]; then
    export GTK_PATH="/opt/homebrew/opt/gtk4/lib/gtk-4.0"
    export PYTHONPATH="/opt/homebrew/lib/python3.14/site-packages:$PYTHONPATH"
    unset GDK_BACKEND
fi

if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating uv virtual environment with Python 3.14..."
    uv venv "$VENV_DIR" --python /opt/homebrew/bin/python3.14
    uv pip install --python "$VENV_DIR/bin/python" psutil
fi

source "$VENV_DIR/bin/activate"

exec python "$@"
