
from gpiozero import MotionSensor

pir = MotionSensor(12) 

while True:
    print("Continue scanning for humans...")
    pir.wait_for_motion()

    print("Moving human detected! Destroy human")
    pir.wait_for_no_motion()

    print("human deactivated...")
