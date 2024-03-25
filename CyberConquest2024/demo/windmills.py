#!/usr/bin/env python3
# @Name: motors.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-03-25
import random

from adafruit_motorkit import MotorKit

class MotorController:
    def __init__(self):
        self.kit = MotorKit()

    def set_random_speed(self):
        r = random.random()
        motor = random.choice([self.kit.motor1, self.kit.motor2, self.kit.motor3, self.kit.motor4])
        if r < 0.5:
            if motor.throttle == 0:
                if random.random() < 0.5:
                    motor.throttle = 1
                else:
                    motor.throttle = -1
            else:
                motor.throttle = 0
        else:
            motor.throttle = 0