#!/usr/bin/python3

from gpiozero import MotionSensor, LED
from time import sleep
import os

pir = MotionSensor(12)
green_led = LED(19)

def start_video_stream():
    os.system("libcamera-vid -t 0 --width 640 --height 480 --framerate 30 --inline --nopreview -o - | feh -x -B black -F -Z - &")

def stop_video_stream():
    os.system("pkill -f 'libcamera-vid'")

while True:
    print("Continue scanning for motion...")
    pir.wait_for_motion()
    print("Motion detected! LED on and video stream activated.")
    green_led.on()
    start_video_stream()
    sleep(3)  # LED stays on for 3 seconds
    green_led.off()
    stop_video_stream()
    print("LED off and video stream deactivated. Waiting for no motion.")
    pir.wait_for_no_motion()
    print("No motion detected. Scanning for motion again.")

