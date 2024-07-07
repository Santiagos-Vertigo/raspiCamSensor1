#!/usr/bin/python3

from gpiozero import LED
from time import sleep

green_led = LED(19)

while True:
    green_led.on()
    sleep(1)
    green_led.off()
    sleep(1)

