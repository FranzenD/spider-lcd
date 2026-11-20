"""LCD1602 display wrapper for showing departure information."""

import asyncio
import logging
import unicodedata
from typing import Optional

logger = logging.getLogger(__name__)

_LCD_MAX_COLS = 16
_SCROLL_STEP_SECONDS = 0.35
_SCROLL_PAUSE_SECONDS = 1.0

# HD44780-compatible controllers have eight custom 5x8 glyph slots.
# Use six of them so rendering does not depend on the controller's character ROM.
_SWEDISH_GLYPHS = {
    "å": (0x04, 0x0A, 0x04, 0x0E, 0x01, 0x0F, 0x11, 0x0F),
    "ä": (0x0A, 0x00, 0x0E, 0x01, 0x0F, 0x11, 0x0F, 0x00),
    "ö": (0x0A, 0x00, 0x0E, 0x11, 0x11, 0x11, 0x0E, 0x00),
    "Å": (0x04, 0x0A, 0x04, 0x0E, 0x11, 0x1F, 0x11, 0x11),
    "Ä": (0x0A, 0x00, 0x0E, 0x11, 0x1F, 0x11, 0x11, 0x00),
    "Ö": (0x0A, 0x00, 0x0E, 0x11, 0x11, 0x11, 0x11, 0x0E),
}
_SWEDISH_CHARACTERS = str.maketrans({
    letter: index for index, letter in enumerate(_SWEDISH_GLYPHS)
})

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
        self._scroll_direction: Optional[str] = None
        self._scroll_timer: Optional[asyncio.TimerHandle] = None

    def setup(self) -> None:
        """Set up the LCD hardware connection.

        Tries I2C address 0x27 (PCF8574T) first, then 0x3F (PCF8574AT).
        Does nothing if modules are unavailable.
        """
        if not _MODULES_AVAILABLE:
            return

        try:
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
            self._load_swedish_glyphs()
            self._available = True
            logger.info("LCD1602 initialized.")
        except Exception:
            logger.exception("Failed to initialize LCD hardware. LCD output will be disabled.")
            self._available = False

    def show(self, direction: str, next_departure_in: str) -> None:
        """Display departure information on the LCD.

        Args:
            direction: Destination direction shown on row 1, scrolling if needed.
            next_departure_in: Departure time shown on row 2, e.g. "5 min".
        """
        if not self._available:
            return

        departure_label = (
            next_departure_in if next_departure_in.strip().lower() == "nu"
            else f"Om: {next_departure_in}"
        )
        direction = unicodedata.normalize("NFC", direction)
        if direction != self._scroll_direction:
            self._stop_scrolling()
            self._write_row(0, direction)
            if len(direction) > _LCD_MAX_COLS:
                self._start_scrolling(direction)
        self._write_row(1, departure_label)

    def show_message(self, first_line: str, second_line: str) -> None:
        """Display two lines of text without departure formatting."""
        self._stop_scrolling()
        if not self._available:
            return

        self._write_row(0, first_line)
        self._write_row(1, second_line)

    def _start_scrolling(self, direction: str) -> None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return

        self._scroll_direction = direction
        self._scroll_timer = loop.call_later(
            _SCROLL_PAUSE_SECONDS, self._scroll, loop, direction, 1
        )

    def _scroll(self, loop: asyncio.AbstractEventLoop, direction: str, offset: int) -> None:
        try:
            self._write_row(0, direction[offset:offset + _LCD_MAX_COLS])
        except Exception:
            self._stop_scrolling()
            logger.exception("Failed to scroll the LCD destination.")
            return

        last_offset = len(direction) - _LCD_MAX_COLS
        next_offset = 0 if offset == last_offset else offset + 1
        delay = _SCROLL_PAUSE_SECONDS if offset in (0, last_offset) else _SCROLL_STEP_SECONDS
        self._scroll_timer = loop.call_later(delay, self._scroll, loop, direction, next_offset)

    def _stop_scrolling(self) -> None:
        if self._scroll_timer is not None:
            self._scroll_timer.cancel()
            self._scroll_timer = None
        self._scroll_direction = None

    def _load_swedish_glyphs(self) -> None:
        """Program custom glyphs and restore the cursor to display memory."""
        for index, bitmap in enumerate(_SWEDISH_GLYPHS.values()):
            self._lcd.write4bits(self._lcd.LCD_SETCGRAMADDR | (index * 8))
            for pixel_row in bitmap:
                self._lcd.write4bits(pixel_row, True)
        self._lcd.setCursor(0, 0)

    def _write_row(self, row: int, text: str) -> None:
        text = unicodedata.normalize("NFC", text).translate(_SWEDISH_CHARACTERS)
        self._lcd.setCursor(0, row)
        self._lcd.message(text[:_LCD_MAX_COLS].ljust(_LCD_MAX_COLS))

    def clear(self) -> None:
        """Clear the LCD screen."""
        self._stop_scrolling()
        if not self._available:
            return
        self._lcd.clear()

    def destroy(self) -> None:
        """Clear the LCD screen and turn off the backlight."""
        self._stop_scrolling()
        if not self._available:
            return
        self._lcd.clear()
        self._mcp.output(3, 0)  # turn off backlight

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
