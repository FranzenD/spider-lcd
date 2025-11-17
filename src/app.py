"""Simple example of using the Spider LCD API client."""

import sys
from pathlib import Path

# Add src directory to path so we can import spider_lcd
sys.path.insert(0, str(Path(__file__).parent / "src"))

from spider_lcd import APIClient
from spider_lcd.exceptions import APIError
from spider_lcd.utils import format_json
import os
from dotenv import load_dotenv
import time


def main():
    """Simple example of making a GET request."""

    # Create API client
    client = APIClient(
        base_url=os.getenv("API_BASE_URL", "http://localhost:3005/api"),
        timeout=10
    )
    
    try:
        while True:
            get_traffic_info(client)
            time.sleep(30)
    except KeyboardInterrupt:
        print("Avslutar...")
        
def get_traffic_info(client):
    """Get and display traffic information."""
    try:
    # Make a GET request
        response = client.get(f"/traffic/{os.getenv('DIRECTION', 'gullmarsplan')}")
        
        if response.success:
            nextDepartureIn = response.get_data("departure.nextDepartureIn", "N/A")
            designation = response.get_data("departure.route.designation", "N/A")
            direction = response.get_data("departure.route.direction", "N/A")
            
            print(f"Linje: {designation}")
            print(f"Mot: {direction}")
            print(f"Om: {nextDepartureIn}")

    except APIError as e:
        print(f"Error: {e}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
    
   
if __name__ == "__main__":
    load_dotenv()
    main()