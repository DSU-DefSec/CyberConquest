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
from socket import AF_INET, socket, SOCK_DGRAM, IPPROTO_UDP, error
from struct import unpack
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

        self.pixels.show()

    def sync_updates(self):
        self.pixels.show()
        send_update()


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


def api_loop():
    class ApiServer:
        def __init__(self):
            self.socket = socket(family=AF_INET, type=SOCK_DGRAM, proto=IPPROTO_UDP)
            self.socket.bind(("0.0.0.0", 53))
            self.active = True

        def cleanup(self):
            self.active = False
            if self.socket is not None:
                self.socket.close()
            self.socket = None

        def __del__(self):
            self.cleanup()

        def run_loop(self):
            while self.active:
                try:
                    raw_bytes = self.socket.recv(65535)

                    if len(raw_bytes) % 2 > 0: raw_bytes = raw_bytes[:-1]
                    for i in range(0, len(raw_bytes), 2):
                        """ Theres your docs. lol
                        0                   1            
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6
                        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        |com|R|col| pix |     value     |
                        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        """


                        instruction = int(raw_bytes[i])
                        value = int(raw_bytes[i + 1])

                        com = instruction & 0b11000000
                        ref = instruction & 0b00100000
                        col = instruction & 0b00011000
                        pix = instruction & 0b00000111
                        if com == 0:
                            if col == 0: app.light_controller.update_pixel(pix,red=value)
                            if col == 1: app.light_controller.update_pixel(pix,green=value)
                            if col == 2: app.light_controller.update_pixel(pix,blue=value)
                            if col == 3: app.light_controller.update_pixel(pix,white=value)
                        if com == 1:
                            app.light_controller.set_brightness(value)
                        if com == 2:
                            resp = ""
                            for a in app.light_controller.get_pixels():
                                for b in a:
                                    resp += chr(b)
                            self.socket.send(resp.encode())

                    # app.light_controller.sync_updates()

                except error as e:
                    print(f"[API] Connection failed: {e}")
                except Exception as e:
                    print(f"[API] Command error: {e}")
            self.cleanup()

    def parse_data(self, address: tuple, raw_bytes: bytes):
        self.log_data(address, raw_bytes)


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
    app.undocumented_api_thread = Thread(target=api_loop, daemon=True)

    with open("traffic-light/users.json") as f:
        for user, pas in json.load(f).items():
            app.auth_tokens.append(hashlib.md5(f"{user}:{pas}".encode()).hexdigest())
    app.light_controller = LightController(8)
    app.light_controller.set_code(INITIAL_CONTROL_CODE)
    app.light_controller.start_loop()

    app.send_update_loop_thread.start()
    app.undocumented_api_thread.start()

    app.run(host='0.0.0.0', debug=False)
