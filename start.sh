#!/bin/bash

# Startskript för Spider LCD app
# Aktiverar venv och startar app.py

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "🕷️  Spider LCD App Starter"
echo "========================="

# Kontrollera om venv finns
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Virtual environment (.venv) hittades inte..."
    echo "🔧 Skapar venv..."
    python3 -m venv "$VENV_DIR"
fi

# Aktivera venv
echo "🔌 Aktiverar virtual environment..."
source "$VENV_DIR/bin/activate"

# Installera beroenden om de saknas
echo "📦 Kontrollerar beroenden..."
pip install -q -r "$SCRIPT_DIR/requirements.txt"

# Starta app.py
echo "🚀 Startar app..."
echo ""
echo "📍 Använda API_BASE_URL: ${API_BASE_URL:-http://localhost:3005/api}"
echo "📍 Polling interval: ${POLL_INTERVAL:-30} sekunder"
echo "📍 Riktning: ${DIRECTION:-gullmarsplan}"
echo ""
echo "💡 Stoppa app med Ctrl+C"
echo ""

cd "$SCRIPT_DIR"
python src/app.py
