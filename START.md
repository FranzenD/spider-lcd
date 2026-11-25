# 🚀 Start Spider LCD App

## Quick Start

```bash
./start.sh
```

This script will:
1. Activate virtual environment (`.venv`)
2. Install required dependencies
3. Start `app.py`

## Environment Variables (optional)

You can create a `.env` file in the project root with the following variables:

```bash
API_BASE_URL=http://localhost:3005/api  # API base address
POLL_INTERVAL=30                         # How often app fetches data (seconds)
DIRECTION=gullmarsplan                   # T-bank station name
```

If you don't specify `.env`, the script uses default values.

## Manual start

If you want to start manually:

```bash
# Activate venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start app
python src/app.py
```

## Stop app

Press `Ctrl+C` in the terminal to stop the app.
