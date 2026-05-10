# 🚀 Starta Spider LCD App

## Snabbstart

```bash
./start.sh
```

Detta skript kommer att:
1. Aktivera virtual environment (`.venv`)
2. Installera nödvändiga beroenden
3. Starta `app.py`

## Miljövariabler (valfritt)

Du kan skapa en `.env`-fil i projektroten med följande variabler:

```bash
API_BASE_URL=http://localhost:3005/api  # API:s basadress
POLL_INTERVAL=30                         # Hur ofta appen hämtar data (sekunder)
DIRECTION=gullmarsplan                   # T-banestationsnamn
```

Om du inte anger `.env` använder skriptet default-värden.

## Manuellt start

Om du vill starta manuellt:

```bash
# Aktivera venv
source .venv/bin/activate

# Installera beroenden
pip install -r requirements.txt

# Starta appen
python src/app.py
```

## Stoppa appen

Tryck `Ctrl+C` i terminalen för att stoppa appen.
