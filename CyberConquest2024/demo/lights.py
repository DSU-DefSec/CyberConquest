#!/usr/bin/env python3
# @Name: lights.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-03-25

import dataclasses
import datetime
import random
import threading
from threading import Thread

import board
import digitalio
import neopixel

PORT = 80
MIN_SPACE_BETWEEN_CARS = 10
NEW_CAR_RAND_CHANCE = 2

GLOBAL_PIXEL_LOCK = threading.Lock()

@dataclasses.dataclass
class TrafficLight:
    red_pin: digitalio.DigitalInOut
    orange_pin: digitalio.DigitalInOut
    green_pin: digitalio.DigitalInOut
    intersection: int
    is_green: bool = False
    green_time: datetime.datetime = datetime.datetime.now()

    def update(self):
        self.is_green = not bool(self.red_pin.value)
        if self.is_green:
            self.green_time = datetime.datetime.now()

LIGHTS = [
    TrafficLight(board.D0, board.D1, board.D2, 100),
    TrafficLight(board.D3, board.D4, board.D5, 100),
    TrafficLight(board.D6, board.D7, board.D8, 100),
    TrafficLight(board.D9, board.D10, board.D11, 100),
]

class Cars:
    @dataclasses.dataclass
    class Car:
        color: tuple = (0, 0, 0)
        position: float = 0
        velocity: float = 0
        accel: float = 0
        length: int = 0
        cid: int = 0

    def __init__(self, pixel_count: int):
        self.pixels = neopixel.NeoPixel(
            board.D21,  # D1
            n=pixel_count,
            bpp=3,
            pixel_order=neopixel.GRB,
            auto_write=False,
            brightness=0.1,
        )
        self.speed_limit = 0.1
        self.cars: list[Cars.Car] = []
        self.active = True
        self.total_spawned = 0
        self.loop_thread = None

    def newcar(self, pos: int = 0):
        self.cars.append(
            Cars.Car(
                color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                velocity=0.1,
                accel=0.01,
                length=random.randint(0, 2),
                position=pos,
                cid=self.total_spawned,
            )
        )
        self.total_spawned += 1
        if self.total_spawned % 10 == 0:
            print(f"[{datetime.datetime.now()}] Cars spawned: {self.total_spawned}")

    def car_driving_loop(self):
        for i in range(100):
            self.newcar(1500 - i * 50)
        while self.active:
            if (
                len(self.cars) == 0
                or self.cars[-1].position > MIN_SPACE_BETWEEN_CARS
                and random.randint(1, NEW_CAR_RAND_CHANCE) == 1
            ):
                self.newcar()
            with GLOBAL_PIXEL_LOCK:
                self.pixels.fill(0)
            next_border = -1
            to_del = []
            for car in self.cars:
                next_is_car = False
                collide = False
                for light in LIGHTS:
                    if light.is_green:
                        continue

                    if light.intersection + car.length + 2 > car.position >= light.intersection:
                        for car2 in self.cars:
                            if (
                                car.cid != car2.cid
                                and light.intersection + car2.length + 2 > car2.position >= light.intersection
                            ):
                                collide = True
                                to_del.append(car)
                                print(f"{car.cid} <> {car2.cid}")
                                # with GLOBAL_PIXEL_LOCK:
                                #    for p in range(int(car.position - car.length * 2), int(car.position + car.length)):
                                #         self.pixels[p] = (255,0,0)
                                # self.pixels.show()
                                # # time.sleep(0.2)
                                # with GLOBAL_PIXEL_LOCK:
                                #    for p in range(int(car.position - car.length * 2), int(car.position + car.length)):
                                #         self.pixels[p] = (0,255,0)
                                # self.pixels.show()
                                # # time.sleep(0.2)

                    if car.position >= light.intersection:
                        continue

                    if car.position < light.intersection < next_border:
                        next_border = light.intersection

                if 0 < next_border - car.position < 2:
                    car.accel = -0.5 * 3 / (next_border - car.position)

                else:
                    if car.velocity < 0.5:
                        car.accel = random.random() * 0.1
                    else:
                        car.accel = 0.03

                    car.accel *= 0.9**car.length

                car.position += car.velocity
                car.velocity = min(max(car.velocity + car.accel, 0), 1)

                pos = int(car.position)
                body = [(255, 255, 255)] + [car.color] * car.length + [(255, 0, 0)]
                for s in body:
                    if 0 <= pos < len(self.pixels):
                        self.pixels[pos] = s if not collide else (255, 0, 0)
                    pos -= 1
                next_border = pos

                if pos > len(self.pixels):
                    to_del.append(car)

            for c in to_del:
                try:
                    self.cars.remove(c)
                except:
                    pass

            with GLOBAL_PIXEL_LOCK:
                try:
                    self.pixels.show()
                except Exception as e:
                    print(f"Error writing to cars: {e}")  # time.sleep(0.05)

    def __del__(self):
        self.active = False
        if self.loop_thread is not None:
            self.loop_thread.join()
            self.loop_thread = None

    def start_loop(self):
        self.loop_thread = Thread(target=self.car_driving_loop, daemon=True)
        self.loop_thread.start()

    def set_brightness(self, brightness: int):
        self.pixels.brightness = brightness / 100