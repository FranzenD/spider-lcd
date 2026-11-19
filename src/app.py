import asyncio
import logging
import os
import signal
from pathlib import Path

from dotenv import load_dotenv
from spider_api import AsyncAPIClient
from spider_api.exceptions import APIError
from lcd_display import LCDDisplay

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
lcd = LCDDisplay()

async def get_traffic_info(client: AsyncAPIClient) -> None:
    try:
        response = await client.get("/traffic")
        route_direction = response.get_data("departure.route.direction")
        next_departure_in = response.get_data("departure.nextDepartureIn")
        if not all(
            isinstance(value, str) and value.strip()
            for value in (route_direction, next_departure_in)
        ):
            logger.warning("Spider API returnerade ingen giltig avgång.")
            lcd.clear()
            return

        designation = response.get_data("departure.route.designation", "N/A")
        logger.info("Linje: %s", designation)
        logger.info("Mot: %s", route_direction)
        logger.info("Om: %s", next_departure_in)
        lcd.show(route_direction, next_departure_in)
    except APIError as error:
        if error.status_code == 409:
            logger.warning("Spara en destination i Spider API:s adminvy.")
            lcd.clear()
        elif error.status_code == 404:
            logger.info("Inga kommande avgångar mot den sparade destinationen.")
            lcd.clear()
        else:
            logger.error("API Error: %s (Status: %s)", error, error.status_code)
            lcd.show("Ett fel inträffade", "Försöker igen...")
    except Exception:
        logger.exception("Unexpected error in get_traffic_info")
        lcd.show("Ett fel inträffade", "Försöker igen...")


def _setup_signal_handlers_for_loop(loop: asyncio.AbstractEventLoop, stop_event: asyncio.Event):
    try:
        loop.add_signal_handler(signal.SIGINT, stop_event.set)
        loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    except NotImplementedError:
        # Windows or other loop that does not support add_signal_handler
        signal.signal(signal.SIGINT, lambda *_: stop_event.set())
        signal.signal(signal.SIGTERM, lambda *_: stop_event.set())

async def main() -> None:
    lcd.setup()
    stop_event = asyncio.Event()

    # Register signal handlers when we have a running loop
    loop = asyncio.get_running_loop()
    _setup_signal_handlers_for_loop(loop, stop_event)

    try:
        poll_interval = int(os.getenv("POLL_INTERVAL", "30"))
        if poll_interval <= 0:
            logger.warning("POLL_INTERVAL must be greater than zero. Using default: 30")
            poll_interval = 30
    except ValueError:
        logger.warning("Invalid POLL_INTERVAL format. Using default: 30")
        poll_interval = 30

    try:
        async with AsyncAPIClient(
            base_url=os.getenv("API_BASE_URL", "http://localhost:3001/api"),
            timeout=10
        ) as client:
            while not stop_event.is_set():
                await get_traffic_info(client)
                # Wait either until stop_event is set or until timeout (poll_interval)
                try:
                    await asyncio.wait_for(stop_event.wait(), timeout=poll_interval)
                except asyncio.TimeoutError:
                    pass
    except Exception:
        logger.exception("Failed to initialize or run API client")

if __name__ == "__main__":
    load_dotenv(".env")
    try:
        asyncio.run(main())
        logger.info("Application finished gracefully.")
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, shutting down...")
    except Exception:
        logger.exception("Unhandled exception in main.")
    finally:
        lcd.destroy()
        logger.info("LCD display cleaned up.")
