#!/bin/bash

# Start script for Spider LCD app
# Activates venv and starts app.py

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "🕷️  Spider LCD App Starter"
echo "=========================="

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Virtual environment (.venv) not found..."
    echo "🔧 Creating venv..."
    python3 -m venv "$VENV_DIR"
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
echo "📍 Using API_BASE_URL: ${API_BASE_URL:-http://localhost:3005/api}"
echo "📍 Polling interval: ${POLL_INTERVAL:-30} seconds"
echo "📍 Direction: ${DIRECTION:-gullmarsplan}"
echo ""
echo "💡 Stop app with Ctrl+C"
echo ""

cd "$SCRIPT_DIR"
python src/app.py
