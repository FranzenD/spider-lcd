# Getting Started with Spider LCD

## Quick Setup (3 steps)

### 1. Install Requirements
```bash
pip install requests
```

### 2. Run the Example
```bash
python example.py
```

### 3. Use in Your Code

Create a new Python file:

```python
# Add this at the top to import the module
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from spider_lcd import APIClient

# Create a client
client = APIClient(base_url="https://api.example.com")

# Make a GET request
response = client.get("/endpoint")

# Use the data
if response.success:
    print(response.data)
```

## Common Use Cases

### Get JSON data from an API
```python
client = APIClient(base_url="https://jsonplaceholder.typicode.com")
response = client.get("/posts/1")
print(response.data)
```

### Use query parameters
```python
response = client.get("/posts", params={"userId": 1, "limit": 10})
```

### With authentication
```python
client = APIClient(
    base_url="https://api.example.com",
    api_key="your_key_here"
)
response = client.get("/protected-endpoint")
```

That's it! You're ready to make GET requests and read JSON data.