#!/usr/bin/python3

from gpiozero import MotionSensor, LED
from time import sleep

pir = MotionSensor(12)
green_led = LED(19)

while True:
    print("Continue scanning for motion...")
    pir.wait_for_motion()
    print("Motion detected! LED on.")
    green_led.on()
    sleep(1)
    green_led.off()
    pir.wait_for_no_motion()
    print("No motion detected. LED off.")

