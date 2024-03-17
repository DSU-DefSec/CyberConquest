#!/usr/bin/env python
# @Name: motor-demo.py
# @Project: CyberConquest/demo
# @Author: Gaelin Shupe
# @Created: 3/30/23

import random
from time import sleep

from adafruit_motorkit import MotorKit

def speed_pick(motor):
    r = random.random()
    if r < 0.5:
        if motor.throttle == 0:
            if random.random() < 0.5:
                motor.throttle =  1
            else:
                motor.throttle =  -1
        else:
            motor.throttle = 0
    else:
        motor.throttle =  0

kit = MotorKit()
while True:
    speed_pick(kit.motor1)
    sleep(1)
    speed_pick(kit.motor2)
    sleep(1)
    speed_pick(kit.motor3)
    sleep(1)
    speed_pick(kit.motor4)
    sleep(1)
