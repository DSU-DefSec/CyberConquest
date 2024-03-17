#!/usr/bin/env python
# @Name: water-pump-pi.py
# @Project: CyberConquest/water-tower
# @Author: Goofables
# @Created: 3/4/23


from time import sleep

import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit

GPIO.setmode(GPIO.BCM)
PIN_NUM = 21
GPIO.setup(PIN_NUM, GPIO.IN)

kit = MotorKit()
motor = kit.motor1

print("Running...")

while True:
    try:
        if GPIO.input(PIN_NUM) > 0:
            #print("Pump off")
            motor.throttle = 0
            sleep(5)
        else:
            #print("Pump on")
            motor.throttle = 1
        sleep(2)
    except OSError:
        print("OSError")
