#!/usr/bin/python3

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from sys import exit

lcd = LCD()

def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    lcd.text("Hello, World!", 1)       # Alphanumeric and punctuation
    lcd.text("1234567890", 2)          # Digits
    lcd.text("Temp: 25°C", 3)          # Special character (degree symbol)
    lcd.text("A+B=C", 4)               # Mathematical symbols
    pause()
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()

