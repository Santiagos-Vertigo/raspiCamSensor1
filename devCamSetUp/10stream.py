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

def display_message_and_countdown(message, countdown, line_message, line_countdown):
    lcd.text(message, line_message)
    for i in range(countdown, 0, -1):
        lcd.text(f"Recording {i}s", line_countdown)
        sleep(1)
    lcd.text("", line_message)  # Clear message after countdown
    lcd.text("", line_countdown)  # Clear countdown after countdown

def start_video_stream():
    os.system("libcamera-vid -t 0 --width 640 --height 480 --framerate 30 --inline --nopreview -o - | ffmpeg -re -i - -c:v copy -f flv rtmp://localhost/live/stream &")

def stop_video_stream():
    os.system("pkill -f 'libcamera-vid'")

try:
    while True:
        print("Continue scanning for motion...")
        pir.wait_for_motion()
        print("Motion detected! LED on, video streaming started, and scrolling text displayed.")
        green_led.on()
        
        start_video_stream()
        
        # Display message and countdown
        display_message_and_countdown("Hi Diego", 10, 1, 2)

        green_led.off()
        stop_video_stream()
        
        print("LED off and video streaming stopped. Waiting for no motion.")
        pir.wait_for_no_motion()
        print("No motion detected. Scanning for motion again.")
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()

