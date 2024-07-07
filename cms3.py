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

def start_video_stream(filename):
    os.system(f"libcamera-vid -t 3000 --width 640 --height 480 --framerate 30 --inline --nopreview -o {filename} &")

def stop_video_stream():
    os.system("pkill -f 'libcamera-vid'")

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

try:
    video_directory = "/home/diego/Desktop/videos"
    ensure_directory_exists(video_directory)
    
    while True:
        print("Continue scanning for motion...")
        pir.wait_for_motion()
        print("Motion detected! LED on, video recording started, and scrolling text displayed.")
        green_led.on()
        
        # Generate a timestamped filename
        filename = os.path.join(video_directory, f"motion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264")
        start_video_stream(filename)
        
        # Start scrolling text
        scroll_text("Hello, Raspberry Pi!", 1, 16)  # Adjust width according to your display

        sleep(3)  # LED stays on for 3 seconds
        green_led.off()
        stop_video_stream()
        
        print(f"LED off and video recording saved to {filename}. Waiting for no motion.")
        pir.wait_for_no_motion()
        print("No motion detected. Scanning for motion again.")
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()

