#!/usr/bin/env python
# @Name: traffic-server.py
# @Project: CyberConquest/traffic-light
# @Author: Doodleman360
# @Created: 2/22/23
# @Edited by Goofables to be 20% more blinky
import hashlib
import json
import os
import random
import time
from threading import Thread

import board
import neopixel_spi as neopixel
from flask import Flask, render_template, request, session, redirect
from flask_sock import Sock

app = Flask(__name__, template_folder="templates")
app.config["SOCK_SERVER_OPTIONS"] = {"ping_interval": 25}
sock = Sock(app)
app.auth_tokens = []
client_list = []

INITIAL_CONTROL_CODE = [
    [
        "set:0,255,0,0",
        "wait:40",
        "set:0,0,0,0",
        "wait:40",
        "wait:0",
        "wait:40",
    ],
    [
        "wait:0",
        "wait:40",
        "set:255,255,0,0",
        "wait:40",
        "set:0,0,0,0",
        "wait:40",
    ],
    [
        "set:0,0,0,0",
        "wait:40",
        "wait:0",
        "wait:40",
        "set:255,0,0,0",
        "wait:40",
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
        # "wait:40"
    ],
    [
        "set:0,255,0,0",
        "wait:40",
        "set:0,0,0,0",
        "wait:40",
        "wait:0",
        "wait:40",
    ],
    [
        "wait:0",
        "wait:40",
        "set:255,255,0,0",
        "wait:40",
        "set:0,0,0,0",
        "wait:40",
    ],
    [
        "set:0,0,0,0",
        "wait:40",
        "wait:0",
        "wait:40",
        "set:255,0,0,0",
        "wait:40",
    ]
]


class LightController:

    def __init__(self, pixel_count: int, ):
        self.pixels = neopixel.NeoPixel_SPI(
            spi=board.SPI(),  # D1
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
                    print(e)
                self.light_instruction_ptr[i] = (self.light_instruction_ptr[i] + 1) % len(self.light_instructions[i])
            if change:
                self.pixels.show()
                send_update()
            time.sleep(0.05)

    def set_code(self, code: list) -> bool:
        self._temp_instructions = code
        return True

    def set_pixel(self, pixel_id: int, color: tuple[int, int, int, int]):
        self.pixels[pixel_id] = color
        self.pixels.show()
        send_update()

    def get_pixel(self, pixel_id: int) -> tuple[int, int, int, int]:
        return self.pixels[pixel_id]

    def get_pixels(self) -> list[list[int]]:
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
    while True:
        time.sleep(1)
        send_update()


def parse_data(data: dict):
    # try:
    # print(data)
    if "code" in data:
        app.light_controller.set_code(data["code"])
    if "brightness" in data:
        app.light_controller.set_brightness(int(data["brightness"]))
    if "id" in data:
        app.light_controller.set_pixel(
            pixel_id=int(data["id"]),
            color=(int(data["r"]), int(data["g"]), int(data["b"]), int(data["w"]))
        )
    # except TypeError as e:
    #     print(e)
    #     pass
    return True


@app.route("/")
def hello_world():
    if request.args.get("user", None) is not None and request.args.get("user", None) is not None:
        auth_token = hashlib.md5(f"{request.args.get('user')}:{request.args.get('pass')}".encode()).hexdigest()
        if auth_token not in app.auth_tokens:
            return render_template("logon.html", error="No access")
        return redirect(f"{request.base_url}?auth_token={auth_token}", 301)
    if request.args.get("auth_token", "") not in app.auth_tokens:
        return render_template("logon.html")
    return render_template(
        "index.html", currentInstruction=json.dumps(app.light_controller.light_instructions)
    )


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

    app.light_controller = LightController(3)
    app.light_controller.set_code(INITIAL_CONTROL_CODE)
    app.light_controller.start_loop()

    app.send_update_loop_thread.start()

    app.run(host='0.0.0.0', debug=False)
