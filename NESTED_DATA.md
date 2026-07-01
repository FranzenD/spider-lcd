# Fetching Nested Data

## Three ways to fetch nested data

### 1. Step-by-step (traditional way)

```python
from spider_lcd import APIClient

client = APIClient(base_url="http://localhost:3005/api")
response = client.get("/traffic/gullmarsplan")

# Fetch each level separately
departure = response.get_data("departure", {})
nextDepartureIn = departure.get("nextDepartureIn", "N/A")
route = departure.get("route", {})
designation = route.get("designation", "N/A")

print(f"Line: {designation}, In: {nextDepartureIn}")
```

### 2. With dot notation directly from response (RECOMMENDED!)

```python
from spider_lcd import APIClient

client = APIClient(base_url="http://localhost:3005/api")
response = client.get("/traffic/gullmarsplan")

# Fetch directly with dot notation
nextDepartureIn = response.get_data("departure.nextDepartureIn", "N/A")
designation = response.get_data("departure.route.designation", "N/A")
direction = response.get_data("departure.route.direction", "N/A")

print(f"Line {designation} towards {direction}, in {nextDepartureIn}")
```

### 3. With get_nested utility function

```python
from spider_lcd import APIClient, get_nested

client = APIClient(base_url="http://localhost:3005/api")
response = client.get("/traffic/gullmarsplan")

# Use get_nested directly on response.data
data = response.data
nextDepartureIn = get_nested(data, "departure.nextDepartureIn", "N/A")
designation = get_nested(data, "departure.route.designation", "N/A")

print(f"Line {designation}, in {nextDepartureIn}")
```

## Example with JSON structure

If your API returns:

```json
{
  "departure": {
    "nextDepartureIn": "5 min",
    "route": {
      "designation": "144",
      "direction": "Gullmarsplan"
    },
    "stops": [
      {"name": "Stop 1"},
      {"name": "Stop 2"}
    ]
  }
}
```

Then you can fetch data like this:

```python
# Simple values
time = response.get_data("departure.nextDepartureIn")  # => "5 min"
line = response.get_data("departure.route.designation")  # => "144"
direction = response.get_data("departure.route.direction")  # => "Gullmarsplan"

# If the key doesn't exist, get default value
missing = response.get_data("departure.missing.key", "N/A")  # => "N/A"

# For arrays, fetch the array first then use index
departure = response.get_data("departure", {})
stops = departure.get("stops", [])
first_stop = stops[0]["name"] if stops else "N/A"  # => "Stop 1"
```

## Advantages of dot notation

✅ Shorter code  
✅ Easier to read  
✅ Automatic handling of missing keys  
✅ No KeyError if a key is missing  

## Tips

- Always use a default value (second parameter) for safety
- Dot notation fungerar endast för dict/object, inte för arrayer
- För arrayer måste du hämta arrayen först och sedan indexera