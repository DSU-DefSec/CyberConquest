#!/usr/bin/env python3
# @Name: motors.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-03-25
import random
import time

from adafruit_motor.motor import DCMotor
from adafruit_motorkit import MotorKit


class Windmills:
    def __init__(self):
        self.kit = MotorKit()
        self.probability = 0.5
        self.motors: list[DCMotor] = [self.kit.motor1, self.kit.motor2, self.kit.motor3, self.kit.motor4]

    def set_random_speed(self):
        r = random.random()
        motor = random.choice(self.motors)
        if r < self.probability:
            if motor.throttle == 0:
                if random.random() < 0.5:  # 50% chance for each direction
                    motor.throttle = 1
                else:
                    motor.throttle = -1
            else:
                motor.throttle = None
        else:
            motor.throttle = None

    def set_speed(self, windmill: int, speed: float):
        """Set the speed of a windmill"""
        self.motors[windmill].throttle = max(-1, min(1, speed))

    def stop_all(self):
        for motor in self.motors:
            motor.throttle = None


if __name__ == "__main__":
    mc = Windmills()
    while True:
        mc.set_random_speed()
        time.sleep(1)
