#!/usr/bin/python3

from gpiozero import MotionSensor, LED
from time import sleep
import os
from datetime import datetime

pir = MotionSensor(12)
green_led = LED(19)

def start_video_stream(filename):
    os.system(f"libcamera-vid -t 3000 --width 640 --height 480 --framerate 30 --inline --nopreview -o {filename} &")

def stop_video_stream():
    os.system("pkill -f 'libcamera-vid'")

while True:
    print("Continue scanning for motion...")
    pir.wait_for_motion()
    print("Motion detected! LED on and video recording started.")
    green_led.on()
    # Generate a timestamped filename
    filename = f"/home/pi/videos/motion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h264"
    start_video_stream(filename)
    sleep(3)  # LED stays on for 3 seconds
    green_led.off()
    stop_video_stream()
    print(f"LED off and video recording saved to {filename}. Waiting for no motion.")
    pir.wait_for_no_motion()
    print("No motion detected. Scanning for motion again.")

