#!/usr/bin/python3

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from sys import exit
from time import sleep

lcd = LCD()

def safe_exit(signum, frame):
    lcd.clear()
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

def scroll_text(text, line, width, delay=0.15):
    text = ' ' * width + text + ' ' * width
    for i in range(len(text) - width + 1):
        lcd.text(text[i:i + width], line)
        sleep(delay)

try:
    while True:
        scroll_text("Hello, Diego!!!", 1, 16)  # 16 is the width of the display
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()

