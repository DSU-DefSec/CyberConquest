#!/usr/bin/env python
# @Name: on.py
# @Project: CyberConquest/wind-turbine
# @Author: Gaelin Shupe
# @Created: 3/21/23

from time import sleep

from adafruit_motorkit import MotorKit


kit = MotorKit()
motor = kit.motor1
motor.throttle = 1
