#!/bin/bash

# PC Resource Manager - Run Script
# Uses uv virtual environment with GTK4 support from Homebrew

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # Homebrew paths
    BREW_PREFIX="/opt/homebrew"
    if [[ ! -d "$BREW_PREFIX" ]]; then
        BREW_PREFIX="/usr/local"
    fi
    
    export GTK_PATH="$BREW_PREFIX/opt/gtk4/lib/gtk-4.0"
    export PYTHONPATH="$BREW_PREFIX/lib/python3.14/site-packages:$PYTHONPATH"
    export GI_TYPELIB_PATH="$BREW_PREFIX/lib/girepository-1.0"
    export DYLD_FALLBACK_LIBRARY_PATH="$BREW_PREFIX/lib:$DYLD_FALLBACK_LIBRARY_PATH"
    
    # On macOS, it's often better to let GDK decide, but sometimes setting it helps
    # export GDK_BACKEND=macos
fi

if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating uv virtual environment with Python 3.14..."
    uv venv "$VENV_DIR" --python /opt/homebrew/bin/python3.14
    uv pip install --python "$VENV_DIR/bin/python" psutil
fi

source "$VENV_DIR/bin/activate"

exec python "$@"
