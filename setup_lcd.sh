#!/bin/bash
# Downloads the required LCD modules from GitHub into src/
# Run once on the Raspberry Pi before starting the application.
#
# Prerequisites:
#   sudo apt-get install python3-smbus i2c-tools
#   sudo raspi-config  -> Interface Options -> I2C -> Enable

set -e

BASE_URL="https://raw.githubusercontent.com/amusarra/raspberry-pi-access-via-ts-cns/54c50654ea22ac432846532c68dbd153b93c25b8/modules"
DEST="$(dirname "$0")/src"

echo "Downloading LCD modules to $DEST ..."

curl -fsSL "$BASE_URL/PCF8574.py" -o "$DEST/PCF8574.py"
curl -fsSL "$BASE_URL/Adafruit_LCD1602.py" -o "$DEST/Adafruit_LCD1602.py"

echo "Done. Modules saved to src/PCF8574.py and src/Adafruit_LCD1602.py"
