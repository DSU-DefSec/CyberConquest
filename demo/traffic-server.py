#!/usr/bin/env python
# @Name: traffic-server.py
# @Project: CyberConquest/traffic-light
# @Author: Doodleman360
# @Created: 2/22/23
# @Edited by Goofables to be 20% more blinky
import dataclasses
import datetime
import json
import os
import random
import threading
import time
import tracemalloc
from threading import Thread

import board
import neopixel
from flask import Flask, render_template, request
from flask_sock import Sock

tracemalloc.start()

app = Flask(__name__, template_folder="templates")
app.config["SOCK_SERVER_OPTIONS"] = {"ping_interval": 25}
sock = Sock(app)
client_list = []

global_pixel_lock = threading.Lock()

INITIAL_CONTROL_CODE = [
    [
        "set:0,255,0,0",
        "wait:50",
        "set:0,0,0,0",
        "wait:25",
        "wait:0",
        "wait:10",

        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",
    ],
    [
        "wait:0",
        "wait:50",
        "set:255,255,0,0",
        "wait:25",
        "set:0,0,0,0",
        "wait:10",

        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",
    ],
    [
        "set:0,0,0,0",
        "wait:50",
        "wait:0",
        "wait:25",
        "set:255,0,0,0",
        "wait:10",

        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",
    ],
    [
        # "set:0,0,0,0",
        # "wait:1",
        # "set:255,0,0,0",
        # "wait:1",
        # "set:0,255,0,0",
        # "wait:1",
        # "set:255,255,0,0",
        # "wait:1",
        # "set:0,0,255,0",
        # "wait:1",
        # "set:255,0,255,0",
        # "wait:1",
        # "set:0,255,255,0",
        # "wait:1",
        # "set:255,255,255,0",
        # "wait:1",
        # "set:0,0,0,255",
        # "wait:1",
        # "set:255,0,0,255",
        # "wait:1",
        # "set:0,255,0,255",
        # "wait:1",
        # "set:255,255,0,255",
        # "wait:1",
        # "set:0,0,255,255",
        # "wait:1",
        # "set:255,0,255,255",
        # "wait:1",
        # "set:0,255,255,255",
        # "wait:1",
        # "set:255,255,255,255",
        # "wait:1",
    ],
    [
        # "shell:curl neverssl.com -s >>/dev/null", # debug testing ONLY
        # "random:",
        # "wait:50"
    ],
    [
        "set:0,255,0,0",
        "wait:50",
        "set:0,0,0,0",
        "wait:25",
        "wait:0",
        "wait:10",

        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",
    ],
    [
        "wait:0",
        "wait:50",
        "set:255,255,0,0",
        "wait:25",
        "set:0,0,0,0",
        "wait:10",

        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",
    ],
    [
        "set:0,0,0,0",
        "wait:50",
        "wait:0",
        "wait:25",
        "set:255,0,0,0",
        "wait:10",

        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",
    ],
    # side2
    [
        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",

        "set:0,0,0,0",
        "wait:50",
        "wait:0",
        "wait:25",
        "set:255,0,0,0",
        "wait:10",
    ],

    [
        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",

        "wait:0",
        "wait:50",
        "set:255,255,0,0",
        "wait:25",
        "set:0,0,0,0",
        "wait:10",
    ],
    [
        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",

        "set:0,255,0,0",
        "wait:50",
        "set:0,0,0,0",
        "wait:25",
        "wait:0",
        "wait:10",
    ],
    [],
    [],
    [
        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",

        "set:0,0,0,0",
        "wait:50",
        "wait:0",
        "wait:25",
        "set:255,0,0,0",
        "wait:10",
    ],

    [
        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",

        "wait:0",
        "wait:50",
        "set:255,255,0,0",
        "wait:25",
        "set:0,0,0,0",
        "wait:10",
    ],
    [
        "wait:0",
        "wait:50",
        "wait:0",
        "wait:25",
        "wait:0",
        "wait:10",

        "set:0,255,0,0",
        "wait:50",
        "set:0,0,0,0",
        "wait:25",
        "wait:0",
        "wait:10",
    ],
]


class LightController:

    def __init__(self, pixel_count: int):
        self.pixels = neopixel.NeoPixel(
            board.D10,  # D1
            n=pixel_count,
            bpp=4,
            pixel_order=neopixel.GRBW,
            auto_write=False,
            brightness=0.1
        )
        self.light_instruction_ptr: list = []
        self.light_instruction_time: list = []
        self.light_instructions: list = []
        self.active = True
        self.loop_thread: Thread = None
        self._temp_instructions: list = []

    def light_control_loop(self):
        while self.active:
            if self.light_instructions != self._temp_instructions:
                self.light_instructions = self._temp_instructions
                self.light_instruction_ptr = [0] * len(self.pixels)
                self.light_instruction_time = [0] * len(self.pixels)

            change = False
            for i in range(len(self.pixels)):
                if len(self.light_instructions) <= i: continue
                if len(self.light_instructions[i]) == 0: continue
                try:
                    instruction, arg = self.light_instructions[i][self.light_instruction_ptr[i]].split(":")
                    if instruction == "set":
                        self.pixels[i] = [int(a) for a in arg.split(",")]
                        change = True
                    elif instruction == "random":
                        self.pixels[i] = [
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255) if arg == "w" else 0
                        ]
                        change = True
                    elif instruction == "wait":
                        if self.light_instruction_time[i] < int(arg):
                            self.light_instruction_time[i] += 1
                            continue
                        else:
                            self.light_instruction_time[i] = 0
                    elif instruction == "shell":  # it's a feature
                        os.system(arg)
                except Exception as e:
                    print(f"Exception: {e}")
                self.light_instruction_ptr[i] = (self.light_instruction_ptr[i] + 1) % len(self.light_instructions[i])
            if change:
                self.sync_updates()
            time.sleep(0.05)

    def set_code(self, code: list) -> bool:
        self._temp_instructions = code
        return True

    def set_pixel(self, pixel_id: int, color: tuple):
        self.pixels[pixel_id] = color
        self.sync_updates()

    def get_pixel(self, pixel_id: int) -> tuple:
        return self.pixels[pixel_id]

    def get_pixels(self) -> list:
        return [list(a) for a in self.pixels]

    def __del__(self):
        self.active = False
        if self.loop_thread is not None:
            self.loop_thread.join()
            self.loop_thread = None

    def start_loop(self):
        self.loop_thread = Thread(target=self.light_control_loop, daemon=True)
        self.loop_thread.start()

    def set_brightness(self, brightness: int):
        self.pixels.brightness = brightness / 100

    def update_pixel(self, pixel_id: int, red: int = None, green: int = None, blue: int = None, white: int = None):
        """
        Wtf even is thread safety??
        """
        val = self.pixels[pixel_id]
        if red is None: red = val[0]
        if green is None: green = val[1]
        if blue is None: blue = val[2]
        if white is None: white = val[3]
        self.pixels[pixel_id] = (red, green, blue, white)

        self.sync_updates(False)

    def sync_updates(self, send_updates=True):
        with global_pixel_lock:
            try:
                self.pixels.show()
            except:
                print("Error writing to trafficlight")
        if send_updates:
            send_update()


def light_green(pixels, vel):
    if [255, 0, 0, 0] in pixels:
        return False
    if [255, 255, 0, 0] in pixels:
        return vel > 0.5
    # return not ([255, 0, 0, 0] in pixels or [255, 255, 0, 0] in pixels)
    return [0, 255, 0, 0] in pixels


@dataclasses.dataclass
class Car:
    position: float = 0
    velocity: float = 0
    accel: float = 0
    color: tuple = (0, 0, 0)
    length: int = 0


class Cars:

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
        self.total_spawned = 0

    def car_driving_loop(self):
        while self.active:
            if len(self.cars) == 0 or self.cars[-1].position > 15:
                self.cars.append(
                    Car(
                        0,
                        0.1,
                        0.01,
                        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                        random.randint(0, 3)
                    )
                )
                self.total_spawned += 1
                if self.total_spawned % 10 == 0:
                    print(f"[{datetime.datetime.now()}] Cars spawned: {self.total_spawned}")
                # print(f"Spawned car: {self.cars[-1]}")
            with global_pixel_lock:
                self.pixels.fill(0)
            last_car_border = -1
            last_car_acl = 0
            last_car_speed = 0
            to_del = []
            for c in self.cars:
                next_is_car = False

                if c.position < 25:
                    next_green = light_green(app.light_controller.pixels[8:], c.velocity)
                    next_pos = 24
                elif c.position > 254:
                    next_green = True
                    next_pos = 500
                else:
                    next_green = light_green(app.light_controller.pixels[:8], c.velocity)
                    next_pos = 127 if c.position < 128 else 254

                if -1 < last_car_border < next_pos:
                    next_pos = last_car_border
                    if next_pos < c.position + 5:
                        next_green = False
                        next_is_car = True

                if not next_green and next_pos - c.position < 2:
                    # p = p + v*t + at^2
                    # if not next_is_car :
                    c.accel = -0.5 * 3 / (next_pos - c.position)
                    # else:
                    #     c.accel = last_car_acl*0.9

                else:
                    if c.velocity < 0.2:
                        c.accel = 0.05
                    else:
                        c.accel = 0.03

                    c.accel *= 0.9 ** c.length

                c.position += c.velocity
                c.velocity = min(max(c.velocity + c.accel, 0), 1)

                pos = int(c.position)
                body = [(255, 255, 255)] + [c.color] * c.length + [(255, 0, 0)]
                for s in body:
                    if 0 <= pos < len(self.pixels):
                        self.pixels[pos] = s
                    pos -= 1
                last_car_border = pos
                last_car_acl = c.accel
                last_car_speed = c.velocity

                if pos > len(self.pixels):
                    to_del.append(c)

            for c in to_del:
                self.cars.remove(c)

            with global_pixel_lock:
                try:
                    self.pixels.show()
                except:
                    print("Error writing to cars")
            time.sleep(0.05)

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


def send_update():
    clients = client_list.copy()
    for client in clients:
        try:
            client.send(json.dumps({"leds": app.light_controller.get_pixels()}))
        except Exception as e:
            print(e)
            print("Closing connection to client")
            client_list.remove(client)


def send_update_loop():
    c = 0
    while True:
        time.sleep(1)
        send_update()
        if c % 600 == 0:
            with open(f"mem.{datetime.datetime.now().timestamp()}.dump", "w") as f:
                snapshot = tracemalloc.take_snapshot()
                f.writelines([a.__str__() + "\n" for a in snapshot.statistics('lineno')[:10]])
        c += 1


def parse_data(data: dict):
    if "code" in data:
        app.light_controller.set_code(data["code"])
    if "brightness" in data:
        app.light_controller.set_brightness(int(data["brightness"]))
    if "id" in data:
        app.light_controller.set_pixel(
            pixel_id=int(data["id"]),
            color=(int(data["r"]), int(data["g"]), int(data["b"]), int(data["w"]))
        )
    return True


@app.route("/")
def hello_world():
    return render_template(
        "index.html", currentInstruction=json.dumps(app.light_controller.light_instructions)
    )


@app.route("/stats")
def stats():
    snapshot = tracemalloc.take_snapshot()
    return "\n".join([a.__str__() for a in snapshot.statistics('lineno')[:10]])


@app.route("/", methods=["POST"])
def post_data():
    # print(request.data)
    return "OK" if parse_data(request.json) else "BAD"


@sock.route("/sock")
def echo(ws):
    client_list.append(ws)
    while True:
        data = ws.receive()
        if data == "close":
            break

        parse_data(json.loads(data))

    client_list.remove(ws)


if __name__ == "__main__":
    app.send_update_loop_thread = Thread(target=send_update_loop, daemon=True)

    app.light_controller = LightController(16)
    app.light_controller.set_code(INITIAL_CONTROL_CODE)
    app.light_controller.start_loop()

    app.car_driver = Cars(300)
    app.car_driver.start_loop()

    app.send_update_loop_thread.start()

    app.run(host='0.0.0.0', debug=False)
