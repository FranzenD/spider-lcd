# Copilot Instructions – spider-lcd

## Project Overview

Python library and application for making HTTP GET requests with JSON handling. The primary use case is polling a local traffic API and displaying departure data.

## Architecture

```
src/spider_lcd/        # Importable package
  client.py            # APIClient (sync, uses requests)
  async_client.py      # AsyncAPIClient (async, uses httpx)
  models.py            # APIResponse (shared by both clients)
  exceptions.py        # APIError
  utils.py             # get_nested(), format_json()
  __init__.py          # Exports all public symbols
src/app.py             # Entry point – async polling loop
```

**Two parallel clients** share `APIResponse` and `APIError`:
- `APIClient` – synchronous, backed by `requests`
- `AsyncAPIClient` – async, backed by `httpx`, **must be used as `async with`**

**There is no `setup.py` or `pyproject.toml`**, so the package is not installed. Scripts must add the `src` directory to `sys.path` manually:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then edit .env
python src/app.py
```

Environment variables (`.env`):
- `API_BASE_URL` – e.g. `http://localhost:3005/api`
- `API_KEY` – optional Bearer token
- `DIRECTION` – e.g. `gullmarsplan`

## Key Conventions

### Dot-notation for nested data
`APIResponse.get_data()` accepts dot-separated paths; the underlying helper is `utils.get_nested()`:

```python
response.get_data("departure.route.designation", "N/A")
```

### Error handling pattern
```python
from spider_lcd.exceptions import APIError

try:
    response = await client.get("/endpoint")
except APIError as e:
    print(e, e.status_code, e.response_data)
```

### AsyncAPIClient lifecycle
Always use as a context manager; calling `.get()` outside a context manager creates a throwaway `httpx.AsyncClient` per request:

```python
async with AsyncAPIClient(base_url=...) as client:
    response = await client.get("/path")
```

### Non-JSON responses
If the server returns non-JSON, `data` is `{"raw_content": "<text>"}`.

### Language
The codebase contains Swedish strings in user-facing output and some code comments. Keep this style for any new user-facing text.
