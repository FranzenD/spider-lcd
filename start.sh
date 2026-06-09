#!/bin/bash

# Start script for Spider LCD app
# Activates venv and starts app.py

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "============================"
echo "🕷️  Spider LCD App Starter. "
echo "============================"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Virtual environment (.venv) not found..."
    echo "🔧 Creating venv..."
    PYTHON_CMD="/usr/local/bin/python3"
    if [ ! -x "$PYTHON_CMD" ]; then
        PYTHON_CMD="/usr/bin/python3"
        echo "⚠️ Falling back to /usr/bin/python3 as /usr/local/bin/python3 was not found or executable."
    fi
    $PYTHON_CMD -m venv "$VENV_DIR"
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install dependencies if missing
echo "📦 Checking dependencies..."
pip install -q -r "$SCRIPT_DIR/requirements.txt"

# Start app.py
echo "🚀 Starting app..."
echo ""
echo "💡 Stop app with Ctrl+C"
echo ""

cd "$SCRIPT_DIR"
python3 src/app.py
