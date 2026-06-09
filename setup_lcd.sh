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

SHA256_PCF8574="cb55c7119201ba9e2619a59d292caeb9c69d2534b29b2eb253bb825f4a46040b"
SHA256_LCD="41b4a0e620874b0d77e0712d84efc4beae988b155c0eef43acb078dce41f8668"

verify_checksum() {
    local file="$1"
    local expected="$2"
    local actual
    actual=$(sha256sum "$file" | awk '{print $1}')
    if [ "$actual" != "$expected" ]; then
        echo "Checksum mismatch for $file"
        echo "  Expected: $expected"
        echo "  Got:      $actual"
        rm -f "$file"
        exit 1
    fi
}

echo "Downloading LCD modules to $DEST ..."

curl -fsSL "$BASE_URL/PCF8574.py" -o "$DEST/PCF8574.py"
verify_checksum "$DEST/PCF8574.py" "$SHA256_PCF8574"

curl -fsSL "$BASE_URL/Adafruit_LCD1602.py" -o "$DEST/Adafruit_LCD1602.py"
verify_checksum "$DEST/Adafruit_LCD1602.py" "$SHA256_LCD"

echo "Done. Modules saved to src/PCF8574.py and src/Adafruit_LCD1602.py"
