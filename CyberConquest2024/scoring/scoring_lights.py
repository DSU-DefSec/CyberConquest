#!/usr/bin/env python3
# @Name: scoring_server.py
# @Project: CyberConquest/CyberConquest2024/scoring
# @Author: Goofables
# @Created: 2024-03-21
import dataclasses
import datetime
import random
import threading
import time
from threading import Thread

import board
import digitalio
import neopixel
from flask import Flask

PORT = 80
TICK_CYCLE = 2
DOWN_AFTER_FAIL = 10
MAX_SECONDS_BEFORE_GREEN = 10
MAX_SECONDS_BEFORE_CRANE_CHECK = 10
MIN_SPACE_BETWEEN_CARS = 3
NEW_CAR_RAND_CHANCE = 2

GLOBAL_PIXEL_LOCK = threading.Lock()

app = Flask(__name__)


def header_pin(slot: int) -> digitalio.DigitalInOut:
    p = digitalio.DigitalInOut(slot)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP
    return p


@dataclasses.dataclass
class TrafficLight:
    red_pin: digitalio.DigitalInOut
    intersection: int
    is_green: bool = False
    green_time: datetime.datetime = datetime.datetime.now()

    def update(self):
        self.is_green = not bool(self.red_pin.value)
        if self.is_green:
            self.green_time = datetime.datetime.now()

    @property
    def in_violation(self):
        return datetime.datetime.now() - self.green_time > datetime.timedelta(seconds=MAX_SECONDS_BEFORE_GREEN)


@dataclasses.dataclass
class LightsTeam:
    light1: TrafficLight
    light2: TrafficLight

    traffic_down_until: datetime.datetime = datetime.datetime.now()

    def __init__(self, r1_pin, r2_pin, int1, int2):
        self.light1 = TrafficLight(r1_pin, int1)
        self.light2 = TrafficLight(r2_pin, int2)

    @staticmethod
    def down() -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(seconds=DOWN_AFTER_FAIL)

    def update(self):
        self.light1.update()
        self.light2.update()
        if self.light1.is_green and self.light2.is_green:
            self.traffic_down_until = self.down()
        if self.light1.in_violation or self.light2.in_violation:
            self.traffic_down_until = self.down()

    def get_status(self) -> bool:
        """
        @return: traffic, crane
        """
        now = datetime.datetime.now()
        return self.traffic_down_until < now


teams = {
    "1": LightsTeam(header_pin(board.D16), header_pin(board.D20), 230, 425),
    "2": LightsTeam(header_pin(board.D26), header_pin(board.D19), 170, 340),
    "3": LightsTeam(header_pin(board.D0), header_pin(board.D5), 112, 603),
    "4": LightsTeam(header_pin(board.D6), header_pin(board.D13), 515, 50),
    "5": LightsTeam(header_pin(board.D11), header_pin(board.D9), 870, 1341),
    "6": LightsTeam(header_pin(board.D10), header_pin(board.D22), 936, 1435),
    "7": LightsTeam(header_pin(board.D17), header_pin(board.D27), 1000, 1253),
    "8": LightsTeam(header_pin(board.D4), header_pin(board.D3), 1175, 1062),
}
LIGHTS: list[TrafficLight] = []
for name, team in teams.items():
    LIGHTS.append(team.light1)
    LIGHTS.append(team.light2)


class Cars:
    @dataclasses.dataclass
    class Car:
        color: tuple = (0, 0, 0)
        position: float = 0
        velocity: float = 0
        accel: float = 0
        length: int = 0

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

    def car_driving_loop(self):
        while self.active:
            if (
                len(self.cars) == 0
                or self.cars[-1].position > MIN_SPACE_BETWEEN_CARS
                and random.randint(1, NEW_CAR_RAND_CHANCE) == 1
            ):
                self.cars.append(
                    Cars.Car(
                        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                        velocity=0.1,
                        accel=0.01,
                        length=random.randint(0, 2),
                    )
                )
                self.total_spawned += 1
                if self.total_spawned % 10 == 0:
                    print(
                        f"[{datetime.datetime.now()}] Cars spawned: {self.total_spawned}"
                    )  # print(f"Spawned car: {self.cars[-1]}")
            with GLOBAL_PIXEL_LOCK:
                self.pixels.fill(0)
            next_border = -1
            to_del = []
            for c in self.cars:
                next_is_car = False

                for light in LIGHTS:
                    if light.is_green:
                        continue
                    if c.position >= light.intersection:
                        continue

                    if c.position < light.intersection < next_border:
                        next_border = light.intersection

                if 0 < next_border - c.position < 2:
                    c.accel = -0.5 * 3 / (next_border - c.position)

                else:
                    if c.velocity < 0.5:
                        c.accel = random.random() * 0.1
                    else:
                        c.accel = 0.03

                    c.accel *= 0.9**c.length

                c.position += c.velocity
                c.velocity = min(max(c.velocity + c.accel, 0), 1)

                pos = int(c.position)
                body = [(255, 255, 255)] + [c.color] * c.length + [(255, 0, 0)]
                for s in body:
                    if 0 <= pos < len(self.pixels):
                        self.pixels[pos] = s
                    pos -= 1
                next_border = pos

                if pos > len(self.pixels):
                    to_del.append(c)

            for c in to_del:
                self.cars.remove(c)

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


def update_loop():
    last = 0
    cycle = 1
    while True:
        time.sleep(max(0, last - time.time() + cycle))
        for name, team in teams.items():
            team.update()
        last = time.time()


@app.route("/scoring")
def scoring():
    return {n: t.get_status() for n, t in teams.items()}


@app.route("/traffic://<team_ip>/")
def score_traffic(team_ip):
    team_num = team_ip.split(".")[2]
    try:
        return "SCORING" if teams[team_num].get_status() else "DOWN"
    except KeyError:
        return "INVALID TEAM"


if __name__ == "__main__":
    app.send_update_loop_thread = Thread(target=update_loop, daemon=True)
    app.send_update_loop_thread.start()

    app.car_driver = Cars(1500)
    app.car_driver.start_loop()

    app.run(host="0.0.0.0", debug=False, port=PORT)
