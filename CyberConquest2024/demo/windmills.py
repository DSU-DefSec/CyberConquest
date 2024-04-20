#!/usr/bin/env python3
# @Name: motors.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-03-25
import random
import time

from adafruit_motorkit import MotorKit


class Windmills:
    def __init__(self):
        self.kit = MotorKit()


class MotorController:
    def __init__(self):
        self.kit = MotorKit()
        self.probability = 0.5

    def set_random_speed(self):
        r = random.random()
        motor = random.choice([self.kit.motor1, self.kit.motor2, self.kit.motor3, self.kit.motor4])
        if r < self.probability:
            if motor.throttle == 0:
                if random.random() < self.probability:
                    motor.throttle = 1
                else:
                    motor.throttle = -1
            else:
                motor.throttle = 0
        else:
            motor.throttle = 0


if __name__ == "__main__":
    mc = MotorController()
    while True:
        mc.set_random_speed()
        time.sleep(1)
