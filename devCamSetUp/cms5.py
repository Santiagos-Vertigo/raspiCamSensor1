#!/usr/bin/python3

from gpiozero import MotionSensor, LED
from time import sleep
import os
from datetime import datetime
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from sys import exit

pir = MotionSensor(12)
green_led = LED(19)
lcd = LCD()

def safe_exit(signum, frame):
    lcd.clear()
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

def scroll_text(text, line, width, delay=0.3):
    text = ' ' * width + text + ' ' * width
    for i in range(len(text) - width + 1):
        lcd.text(text[i:i + width], line)
        sleep(delay)

def start_streaming():
    os.system("libcamera-vid -t 10000 --width 640 --height 480 --framerate 30 --inline --nopreview -o - | ffmpeg -re -i - -c:v copy -f flv rtmp://192.168.1.241/live/stream &")

def stop_streaming():
    os.system("pkill -f 'libcamera-vid'")

try:
    while True:
        print("Continue scanning for motion...")
        pir.wait_for_motion()
        print("Motion detected! LED on, video streaming started, and scrolling text displayed.")
        green_led.on()
        
        start_streaming()
        
        # Start scrolling text
        scroll_text("Hello, Raspberry Pi!", 1, 16)  # Adjust width according to your display

        sleep(10)  # Stream video for 10 seconds
        green_led.off()
        stop_streaming()
        
        print("LED off and video streaming stopped. Waiting for no motion.")
        pir.wait_for_no_motion()
        print("No motion detected. Scanning for motion again.")
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()

