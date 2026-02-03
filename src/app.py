"""Simple example of using the Spider LCD API client."""

import sys
from pathlib import Path

# Add src directory to path so we can import spider_lcd
sys.path.insert(0, str(Path(__file__).parent / "src"))

from spider_lcd import AsyncAPIClient
from spider_lcd.exceptions import APIError
import os
from dotenv import load_dotenv
import asyncio


async def main():
    """Simple example of making an async GET request."""

    # Create async API client
    async with AsyncAPIClient(
        base_url=os.getenv("API_BASE_URL", "http://localhost:3005/api"),
        timeout=10
    ) as client:
        try:
            while True:
                await get_traffic_info(client)
                await asyncio.sleep(30)
        except KeyboardInterrupt:
            print("Avslutar...")
        
async def get_traffic_info(client):
    """Get and display traffic information."""
    try:
        # Make an async GET request
        response = await client.get(f"/traffic/{os.getenv('DIRECTION', 'gullmarsplan')}")
        
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
    asyncio.run(main())