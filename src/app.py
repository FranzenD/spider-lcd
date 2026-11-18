"""Simple example of using the Spider LCD API client."""

import sys
import argparse
from pathlib import Path

# Add src directory to path so we can import spider_lcd and lcd_display
sys.path.insert(0, str(Path(__file__).parent / "src"))

from spider_lcd import AsyncAPIClient
from spider_lcd.exceptions import APIError
from lcd_display import LCDDisplay
import os
from dotenv import load_dotenv
import asyncio

lcd = LCDDisplay()
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="Visa mer detaljerad output")
args = parser.parse_args()

async def main():
    """Simple example of making an async GET request."""
    lcd.setup()

    try:
        # Create async API client
        async with AsyncAPIClient(
            base_url=os.getenv("API_BASE_URL", "http://localhost:3001/api"),
            timeout=10
        ) as client:
            while True:
                await get_traffic_info(client)
                await asyncio.sleep(30)
    except KeyboardInterrupt:
        print("Avslutar...")
    finally:
        lcd.destroy()


async def get_traffic_info(client):
    """Get and display traffic information."""
    try:
        response = await client.get("/traffic")
    except APIError as error:
        lcd.clear()
        if error.status_code == 409:
            print("Spara en destination i Spider API:s adminvy.")
        elif error.status_code == 404:
            print("Inga kommande avgångar mot den sparade destinationen.")
        else:
            print(f"Fel vid hämtning av avgång: {error}")
        return

    next_departure_in = response.get_data("departure.nextDepartureIn")
    direction = response.get_data("departure.route.direction")
    if not all(isinstance(value, str) and value.strip() for value in (direction, next_departure_in)):
        lcd.clear()
        print("Spider API returnerade ingen giltig avgång.")
        return

    if args.verbose:
        designation = response.get_data("departure.route.designation", "N/A")
        print(f"Linje: {designation}")
        print(f"Mot: {direction}")
        print(next_departure_in if next_departure_in.strip().lower() == "nu" else f"Om: {next_departure_in}")

    lcd.show(direction, next_departure_in)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
