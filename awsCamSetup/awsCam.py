#!/usr/bin/python3

from gpiozero import MotionSensor, LED
from time import sleep
import os
from datetime import datetime
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from sys import exit
import boto3

# Initialize Boto3 S3 client
s3_client = boto3.client('s3', region_name='us-east-1')

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
        lcd.text(f"Recorded {i}s", line_countdown)
        sleep(1)
    lcd.text("", line_message)  # Clear message after countdown
    lcd.text("", line_countdown)  # Clear countdown after countdown

def start_video_stream(filename):
    os.system(f"libcamera-vid -t 10000 --width 640 --height 480 --framerate 30 --inline --nopreview -o {filename} &")

def stop_video_stream(filename):
    os.system("pkill -f 'libcamera-vid'")
    upload_to_s3('camtestbucket1', filename)

def upload_to_s3(bucket, file_path):
    try:
        s3_client.upload_file(file_path, bucket, os.path.basename(file_path))
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
    except Exception as e:
        print("Failed to upload to S3:", e)

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
        
        # Display message and countdown
        display_message_and_countdown("You are being recorded", 10, 1, 2)
        
        sleep(10)  # Simulate recording duration
        green_led.off()
        stop_video_stream(filename)
        
        print(f"LED off and video recording saved to {filename}. Waiting for no motion.")
        pir.wait_for_no_motion()
        print("No motion detected. Scanning for motion again.")
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
