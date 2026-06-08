"""Simple example of using the Spider LCD API client."""

import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from spider_lcd import AsyncAPIClient
from spider_lcd.exceptions import APIError

# Configure logging to log to a file with INFO level and a specific format
logging.basicConfig(
    filename='app.log',  # File name for the log file
    level=logging.INFO,   # Minimum logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format for log messages
)
logger = logging.getLogger(__name__)

# Add src directory to path so we can import spider_lcd
sys.path.insert(0, str(Path(__file__).parent))


async def get_traffic_info(client: AsyncAPIClient) -> None:
    """Get and display traffic information."""
    direction = os.getenv("DIRECTION", "gullmarsplan")

    try:
        response = await client.get(f"/traffic/{direction}")

        if response.success:
            next_departure_in = response.get_data("departure.nextDepartureIn", "N/A")
            designation = response.get_data("departure.route.designation", "N/A")
            route_direction = response.get_data("departure.route.direction", "N/A")

            logger.info("Linje: %s", designation)
            logger.info("Mot: %s", route_direction)
            logger.info("Om: %s", next_departure_in)
        else:
            logger.warning("Response was not successful for %s", direction)

    except APIError as e:
        logger.error("API Error: %s (Status: %s)", e, e.status_code)
    except Exception as e:
        logger.error("Unexpected error in get_traffic_info: %s", e)

async def main() -> None:
    """Main entry point - polls traffic info periodically."""
    try:
        poll_interval = int(os.getenv("POLL_INTERVAL", "30"))
        if poll_interval <= 0:
            raise ValueError("POLL_INTERVAL must be greater than zero")
    except ValueError as e:
        logger.error("Invalid POLL_INTERVAL: %s", e)
        return

    try:
        async with AsyncAPIClient(
            base_url=os.getenv("API_BASE_URL", "http://localhost:3005/api"),
            timeout=10
        ) as client:
            try:
                while True:
                    await get_traffic_info(client)
                    await asyncio.sleep(poll_interval)
            except KeyboardInterrupt:
                logger.info("Exiting...")
    except Exception as e:
        logger.critical("Failed to initialize or run API client: %s", e)


if __name__ == "__main__":
    load_dotenv(".env")
    asyncio.run(main())