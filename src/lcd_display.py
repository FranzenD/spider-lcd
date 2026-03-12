"""LCD1602 display wrapper for showing departure information."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

_LCD_MAX_COLS = 16

try:
    from PCF8574 import PCF8574_GPIO
    from Adafruit_LCD1602 import Adafruit_CharLCD
    _MODULES_AVAILABLE = True
except ImportError:
    _MODULES_AVAILABLE = False
    logger.warning(
        "PCF8574 or Adafruit_LCD1602 modules not found. "
        "Run setup_lcd.sh to download them. LCD output disabled."
    )

_PCF8574T_ADDRESS = 0x27
_PCF8574AT_ADDRESS = 0x3F


class LCDDisplay:
    """Wrapper around the I2C LCD1602 display.

    Degrades gracefully if the required modules (PCF8574, Adafruit_LCD1602)
    are not installed – all methods become no-ops in that case.
    """

    def __init__(self) -> None:
        """Initialize the LCD display driver."""
        self._available: bool = False
        self._mcp: Optional[object] = None
        self._lcd: Optional[object] = None

    def setup(self) -> None:
        """Set up the LCD hardware connection.

        Tries I2C address 0x27 (PCF8574T) first, then 0x3F (PCF8574AT).
        Does nothing if modules are unavailable.
        """
        if not _MODULES_AVAILABLE:
            return

        mcp = self._connect_mcp()
        if mcp is None:
            logger.error(
                "No I2C device found at 0x27 or 0x3F. "
                "Check wiring and that I2C is enabled (raspi-config)."
            )
            return

        self._mcp = mcp
        self._lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)
        self._mcp.output(3, 1)  # turn on backlight
        self._lcd.begin(16, 2)
        self._available = True
        logger.info("LCD1602 initialized.")

    def show(self, direction: str, next_departure_in: str) -> None:
        """Display departure information on the LCD.

        Args:
            direction: Destination direction shown on row 1 (truncated to 16 chars).
            next_departure_in: Departure time shown on row 2, e.g. "5 min".
        """
        if not self._available:
            return

        row1 = direction[:_LCD_MAX_COLS]
        row2 = f"Om: {next_departure_in}"[:_LCD_MAX_COLS]

        self._lcd.setCursor(0, 0)
        self._lcd.message(row1.ljust(_LCD_MAX_COLS))
        self._lcd.setCursor(0, 1)
        self._lcd.message(row2.ljust(_LCD_MAX_COLS))

    def clear(self) -> None:
        """Clear the LCD screen."""
        if not self._available:
            return
        self._lcd.clear()

    def _connect_mcp(self) -> Optional[object]:
        """Try to connect to PCF8574 at known I2C addresses.

        Returns:
            A PCF8574_GPIO instance, or None if no device is found.
        """
        for address in (_PCF8574T_ADDRESS, _PCF8574AT_ADDRESS):
            try:
                return PCF8574_GPIO(address)
            except Exception as e:
                logger.debug(f"Failed to connect to I2C address {hex(address)}: {e}")
                continue
        return None
