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
API_BASE_URL=http://localhost:3001/api  # API base address
POLL_INTERVAL=30                         # How often app fetches data (seconds)
```

If you don't specify `.env`, the script uses default values.

In Spider API's `/traffic` admin view, select a stop and save a destination.
The LCD polls `GET /api/traffic` for the next departure toward that destination.
Remove `DIRECTION` from existing LCD configuration and update `API_BASE_URL`
if it still points to the old port. The LCD clears when a destination or an
upcoming departure is unavailable and checks again at the next poll.

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
