# Spider LCD

A simple Python client for making GET requests to APIs and handling JSON responses.

## Features

- 🚀 Simple and easy to use
- 📡 Make GET requests to any API
- 📦 Automatic JSON parsing
- 🛡️ Basic error handling
- 🔐 Support for API key authentication
- 🎯 Get nested data with dot notation (e.g., `"user.address.city"`)

## Installation

### 1. Create Virtual Environment (Recommended)

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

**Linux/Mac:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables (Optional)

```bash
# Copy the example file
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac

# Edit .env with your settings
```

## Quick Start

### Basic Usage

```python
from spider_lcd import APIClient
from spider_lcd.exceptions import APIError

# Create client
client = APIClient(base_url="https://api.example.com")

try:
    # Make a GET request
    response = client.get("/posts/1")
    
    if response.success:
        print(f"Status: {response.status_code}")
        print(f"Data: {response.data}")
        
        # Get specific field
        title = response.get_data("title")
        print(f"Title: {title}")

except APIError as e:
    print(f"Error: {e}")
```

### Get Nested Data (Dot Notation)

```python
# Instead of multiple steps:
user = response.get_data("user", {})
address = user.get("address", {})
city = address.get("city", "N/A")

# Do this in one step:
city = response.get_data("user.address.city", "N/A")
```

Example from your project:
```python
# Get nested departure information
nextDepartureIn = response.get_data("departure.nextDepartureIn", "N/A")
designation = response.get_data("departure.route.designation", "N/A")
direction = response.get_data("departure.route.direction", "N/A")
```

### With Query Parameters

```python
client = APIClient(base_url="https://api.example.com")

# Pass query parameters
response = client.get("/posts", params={"userId": 1})

if response.success:
    posts = response.data
    print(f"Found {len(posts)} posts")
```

### With API Key

```python
client = APIClient(
    base_url="https://api.example.com",
    api_key="your_api_key_here"
)

response = client.get("/protected-endpoint")
```

### Using Environment Variables

```python
import os
from dotenv import load_dotenv
from spider_lcd import APIClient

# Load from .env file
load_dotenv()

client = APIClient(
    base_url=os.getenv("API_BASE_URL", "http://localhost:3005/api"),
    api_key=os.getenv("API_KEY")
)

response = client.get(f"/traffic/{os.getenv('DIRECTION', 'gullmarsplan')}")
```

### Run the Example

```bash
python example.py
```

## Project Structure

```
spider-lcd/
├── src/spider_lcd/      # Main package
│   ├── __init__.py      # Package exports
│   ├── client.py        # API client
│   ├── models.py        # Response model
│   ├── exceptions.py    # Error handling
│   └── utils.py         # Utilities (includes get_nested)
├── example.py           # Usage examples
├── requirements.txt     # Dependencies
├── .env.example         # Environment variables template
├── .env                 # Your environment variables (not in git)
├── GETTING_STARTED.md   # Quick start guide
├── NESTED_DATA.md       # Guide for nested data access
└── README.md            # This file
```

## API Reference

### APIClient

```python
APIClient(base_url: str, api_key: str = None, timeout: int = 30)
```

**Parameters:**
- `base_url` - Base URL of the API
- `api_key` - Optional API key for authentication
- `timeout` - Request timeout in seconds (default: 30)

**Methods:**
- `get(endpoint, params=None)` - Make a GET request

### APIResponse

**Properties:**
- `status_code` - HTTP status code
- `data` - Parsed JSON data (dict)
- `headers` - Response headers (dict)
- `success` - Whether request succeeded (bool)

**Methods:**
- `get_data(key, default=None)` - Get value from response data (supports dot notation)
- `has_key(key)` - Check if key exists in data

### Utility Functions

```python
from spider_lcd.utils import get_nested, format_json

# Get nested value from dictionary
value = get_nested(data, "user.address.city", default="N/A")

# Pretty print JSON
print(format_json(response.data))
```

## Deactivate Virtual Environment

When you're done working:

```bash
deactivate
```

## Setting Up on a New Machine

```bash
# 1. Clone/copy the project
cd spider-lcd

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup environment variables
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 6. Edit .env with your settings

# 7. Test it
python example.py
```

## License

MIT License - see [LICENSE](LICENSE) file for details.
