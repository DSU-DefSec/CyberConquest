#!/usr/bin/env python
# @Name: scoring-server.py
# @Project: CyberConquest/water-tower-scoring
# @Author: Goofables
# @Created: 3/6/23

import json
import time
from enum import Enum
from threading import Thread

import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23008 import MCP23008
from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__, template_folder="templates")
app.config["SOCK_SERVER_OPTIONS"] = {"ping_interval": 25}
sock = Sock(app)
client_list = []

TEAM_COUNT = 0


class GPIOController:
    class State(Enum):
        EMPTY = 0
        SCORING = 1
        OVERFLOW = 2
        BROKEN = 3

    def __init__(self, team_count: int):
        self.team_count = team_count

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp_list: list[MCP23008] = []
        self.raw_pins: list[digitalio.DigitalInOut] = []

        mcp_id = 0x20
        while len(self.raw_pins) < team_count:
            mcp: MCP23008 = MCP23008(self.i2c, address=mcp_id)
            self.mcp_list.append(mcp)
            for i in range(8):
                self.raw_pins.append(mcp.get_pin(i))

        self.overflow_sensors: list[digitalio.DigitalInOut] = []
        self.scoring_sensors: list[digitalio.DigitalInOut] = []

        for t in range(team_count):
            scoring_pin = self.raw_pins[t * 2]
            scoring_pin.direction = digitalio.Direction.INPUT
            self.scoring_sensors.append(scoring_pin)

            overflow_pin = self.raw_pins[t * 2 + 1]
            overflow_pin.direction = digitalio.Direction.INPUT
            self.overflow_sensors.append(overflow_pin)

    def get_team(self, team_id: int) -> str:
        value = (self.overflow_sensors[team_id].value << 1 & 2) + (self.scoring_sensors[team_id].value & 1)
        return GPIOController.State(value).name

    def get_teams(self) -> list:
        # return [self.get_team(t) for t in range(self.team_count)]
        return [GPIOController.State.OVERFLOW.name]


def send_update():
    clients = client_list.copy()
    for client in clients:
        try:
            client.send(json.dumps({"teams": app.gpio_controller.get_teams()}))
        except Exception as e:
            print(e)
            print("Closing connection to client")
            client_list.remove(client)


def send_update_loop():
    while True:
        time.sleep(1)
        send_update()


@app.route("/")
def hello_world():
    return render_template(
        "index.html", currentInstruction=json.dumps(app.gpio_controller.get_teams())
    )


@app.route("/scoring")
def scoring():
    return app.gpio_controller.get_teams()


@sock.route("/sock")
def echo(ws):
    client_list.append(ws)
    while True:
        data = ws.receive()
        if data == "close":
            break
    client_list.remove(ws)


if __name__ == "__main__":
    app.gpio_controller = GPIOController(TEAM_COUNT)

    app.send_update_loop_thread = Thread(target=send_update_loop, daemon=True)
    app.send_update_loop_thread.start()

    app.run(host='0.0.0.0', debug=False)
