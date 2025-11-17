# Hämta Nästlad Data (Nested Data)

## Tre sätt att hämta nästlad data

### 1. Steg-för-steg (traditionellt sätt)

```python
from spider_lcd import APIClient

client = APIClient(base_url="http://localhost:3005/api")
response = client.get("/traffic/gullmarsplan")

# Hämta varje nivå separat
departure = response.get_data("departure", {})
nextDepartureIn = departure.get("nextDepartureIn", "N/A")
route = departure.get("route", {})
designation = route.get("designation", "N/A")

print(f"Linje: {designation}, Om: {nextDepartureIn}")
```

### 2. Med dot notation direkt från response (REKOMMENDERAT!)

```python
from spider_lcd import APIClient

client = APIClient(base_url="http://localhost:3005/api")
response = client.get("/traffic/gullmarsplan")

# Hämta direkt med punktnotation
nextDepartureIn = response.get_data("departure.nextDepartureIn", "N/A")
designation = response.get_data("departure.route.designation", "N/A")
direction = response.get_data("departure.route.direction", "N/A")

print(f"Linje {designation} mot {direction}, om {nextDepartureIn}")
```

### 3. Med get_nested utility-funktionen

```python
from spider_lcd import APIClient, get_nested

client = APIClient(base_url="http://localhost:3005/api")
response = client.get("/traffic/gullmarsplan")

# Använd get_nested direkt på response.data
data = response.data
nextDepartureIn = get_nested(data, "departure.nextDepartureIn", "N/A")
designation = get_nested(data, "departure.route.designation", "N/A")

print(f"Linje {designation}, om {nextDepartureIn}")
```

## Exempel med JSON-struktur

Om ditt API returnerar:

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

Så kan du hämta data så här:

```python
# Enkla värden
time = response.get_data("departure.nextDepartureIn")  # => "5 min"
line = response.get_data("departure.route.designation")  # => "144"
direction = response.get_data("departure.route.direction")  # => "Gullmarsplan"

# Om nyckeln inte finns, få default-värde
missing = response.get_data("departure.missing.key", "N/A")  # => "N/A"

# För arrayer, hämta först arrayen sen använd index
departure = response.get_data("departure", {})
stops = departure.get("stops", [])
first_stop = stops[0]["name"] if stops else "N/A"  # => "Stop 1"
```

## Fördelar med dot notation

✅ Kortare kod  
✅ Lättare att läsa  
✅ Automatisk hantering av saknade nycklar  
✅ Inga KeyError om en nyckel saknas  

## Tips

- Använd alltid ett default-värde (andra parametern) för säkerhet
- Dot notation fungerar endast för dict/object, inte för arrayer
- För arrayer måste du hämta arrayen först och sedan indexera