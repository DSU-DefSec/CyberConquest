#!/usr/bin/env python
# @Name: chase.py.py
# @Project: CyberConquest/demo
# @Author: Gaelin Shupe
# @Created: 4/2/23

import time
import dataclasses
import board
import neopixel
import random

class Cars:
    @dataclasses.dataclass
    class Car:
        position: float = 0
        speed: float = 0
        color: tuple = (0, 0, 0)

    def __init__(self, pixel_count: int):
        self.pixels = neopixel.NeoPixel(
            board.D21,  # D1
            n=pixel_count,
            bpp=3,
            pixel_order=neopixel.GRB,
            auto_write=False,
            brightness=0.1
        )
        self.speed_limit = 0.1
        self.cars: list = []
        self.active = True

    def car_driving_loop(self):
        while self.active:
            if len(self.cars) == 0 or self.cars[-1].position > 10:
                self.cars.append(
                    self.Car(0, 0.5, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                )
                print(f"Spawned car: {self.cars[-1]}")
            self.pixels.fill(0)
            last_car_border = -1
            to_del = []
            for c in self.cars:
                c.position += c.velocity
                pos = int(c.position)
                body = [(255, 255, 255), c.color, (255, 0, 0)]
                for s in body:
                    if 0 <= pos < len(self.pixels):
                        self.pixels[pos] = s
                    pos -= 1

                if pos > len(self.pixels):
                    to_del.append(c)

            for c in to_del:
                self.cars.remove(c)

            self.pixels.show()
            time.sleep(0.05)

    def __del__(self):
        self.active = False


    def set_brightness(self, brightness: int):
        self.pixels.brightness = brightness / 100


c = Cars(300)
c.car_driving_loop()