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
import busio
import digitalio
import neopixel
from adafruit_mcp230xx.mcp23008 import MCP23008
from flask import Flask

PORT = 80
MCP_COUNT = 2  # 5  # 6
TICK_CYCLE = 2
DOWN_AFTER_FAIL = 10
MAX_SECONDS_BEFORE_GREEN = 10
MAX_SECONDS_BEFORE_CRANE_CHECK = 10

MCP_BASE_ID = 0x20

GLOBAL_PIXEL_LOCK = threading.Lock()

app = Flask(__name__)
# app.config["SOCK_SERVER_OPTIONS"] = {"ping_interval": 25}

i2c = busio.I2C(board.D3, board.D2)  # (board.SCL, board.SDA)
mcp_list: list = [MCP23008(i2c, address=MCP_BASE_ID + i) for i in range(MCP_COUNT)]


# for m in mcp_list:
#     for i in range(8):


def pin(m: int, p: int) -> digitalio.DigitalInOut:
    """
    @param m: mcp_id
    @param p: pin_id
    @return: pin
    """
    p = mcp_list[m].get_pin(p)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP
    return p


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
class Team:
    light1: TrafficLight
    light2: TrafficLight
    crane_pin: digitalio.DigitalInOut

    traffic_down_until: datetime.datetime = datetime.datetime.now()
    crane_down_until: datetime.datetime = datetime.datetime.now()
    crane_on_time: datetime.datetime = datetime.datetime.now()
    crane_off_time: datetime.datetime = datetime.datetime.now()

    def __init__(self, r1_pin, r2_pin, int1, int2, crane):
        self.light1 = TrafficLight(r1_pin, int1)
        self.light2 = TrafficLight(r2_pin, int2)
        self.crane_pin = crane

    @staticmethod
    def down() -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(seconds=DOWN_AFTER_FAIL)

    def update(self):
        self.light1.update()
        self.light2.update()
        if self.light1.is_green and self.light1.is_green:
            self.traffic_down_until = self.down()
        if self.light1.in_violation or self.light2.in_violation:
            self.traffic_down_until = self.down()

        if bool(self.crane_pin.value):
            self.crane_on_time = datetime.datetime.now()
        else:
            self.crane_off_time = datetime.datetime.now()

        if datetime.datetime.now() - self.crane_off_time > datetime.timedelta(seconds=MAX_SECONDS_BEFORE_GREEN):
            self.crane_down_until = self.down()
        if datetime.datetime.now() - self.crane_on_time > datetime.timedelta(seconds=MAX_SECONDS_BEFORE_GREEN):
            self.crane_down_until = self.down()

    def get_status(self) -> tuple[int, int]:
        """
        @return: traffic, crane
        """
        now = datetime.datetime.now()
        return self.traffic_down_until < now, self.crane_down_until < now


teams = [
    Team(header_pin(board.D18), header_pin(board.D23), 30, 150, pin(0, 0)),  # T1
    # Team(pin(0, 2), pin(0, 3), 10, 20, header_pin(board.D1)),  # T2
    # Team(pin(0, 4), pin(0, 5), 10, 20, header_pin(board.D2)),  # T3
    # Team(pin(0, 6), pin(0, 7), 10, 20, header_pin(board.D3)),  # T4
    # Team(pin(1, 0), pin(1, 1), 10, 20, header_pin(board.D4)),  # T5
    # Team(pin(1, 2), pin(1, 3), 10, 20, header_pin(board.D5)),  # T6
    # Team(pin(1, 4), pin(1, 5), 10, 20, header_pin(board.D6)),  # T7
    # Team(pin(1, 6), pin(1, 7), 10, 20, header_pin(board.D7)),  # T8
    # Team(pin(2, 0), pin(2, 1), 10, 20, header_pin(board.D8)),  # T9
    # Team(pin(2, 2), pin(2, 3), 10, 20, header_pin(board.D9)),  # T10
]
LIGHTS: list[TrafficLight] = []
for team in teams:
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
            if len(self.cars) == 0 or self.cars[-1].position > 15:
                self.cars.append(
                    Cars.Car(
                        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                        velocity=0.1,
                        accel=0.01,
                        length=random.randint(0, 3),
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
                    if c.velocity < 0.2:
                        c.accel = 0.05
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
        for team in teams:
            team.update()
        last = time.time()


@app.route("/scoring")
def scoring():
    return {str(i): t.get_status() for i, t in enumerate(teams)}


@app.route("/traffic://<team_ip>/")
def score_traffic(team_ip):
    team_num = int(team_ip.split(".")[2])
    return teams[team_num].get_status()[0]


@app.route("/crane://<team_ip>/")
def score_crane(team_ip):
    team_num = int(team_ip.split(".")[2])
    return teams[team_num].get_status()[1]


if __name__ == "__main__":
    app.send_update_loop_thread = Thread(target=update_loop, daemon=True)
    app.send_update_loop_thread.start()

    app.car_driver = Cars(300)
    app.car_driver.start_loop()

    app.run(host="0.0.0.0", debug=False, port=PORT)
