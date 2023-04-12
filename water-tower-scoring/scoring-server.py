#!/usr/bin/env python
# @Name: scoring-server.py
# @Project: CyberConquest/water-tower-scoring
# @Author: Goofables
# @Created: 3/6/23
import dataclasses
import json
import time
from enum import Enum
from threading import Thread

import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23008 import MCP23008
from flask import Flask, render_template

MCP_COUNT = 6
MCP_BASE_ID = 0x20

app = Flask(__name__, template_folder="templates")
app.config["SOCK_SERVER_OPTIONS"] = {"ping_interval": 25}

client_list = []

i2c = busio.I2C(board.SCL, board.SDA)
raw_pins: list = []
mcp_list: list = [MCP23008(i2c, address=MCP_BASE_ID + i) for i in range(MCP_COUNT)]
for m in mcp_list:
    for i in range(8):
        raw_pins.append(m.get_pin(i))


def pin(mcp_id: int, pin_id: int) -> digitalio.DigitalInOut:
    p = mcp_list[mcp_id].get_pin(pin_id)
    p.direction = digitalio.Direction.INPUT
    return p


@dataclasses.dataclass
class Team:
    scoring: digitalio.DigitalInOut
    overflow: digitalio.DigitalInOut


teams = [
    Team(pin(0, 6), pin(0, 7)),
    Team(pin(5, 4), pin(5, 1)),
    Team(pin(4, 0), pin(4, 1)),
    Team(pin(3, 1), pin(3, 0)),
    Team(pin(2, 1), pin(2, 0)),

    Team(pin(1, 1), pin(1, 0)),
    Team(pin(0, 3), pin(0, 2)),
    Team(pin(0, 1), pin(0, 0)),#7
]


class State(Enum):
    EMPTY = 0
    SCORING = 1
    OVERFLOW = 2
    BROKEN = 3


def get_team(team_id: int) -> str:
    value = (teams[team_id].overflow.value << 1 & 2) + (teams[team_id].scoring.value & 1)
    return State(value).name


def get_teams() -> list:
    return [get_team(t) for t in range(len(teams))]
    # return [State.OVERFLOW.name]


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


@app.route("/scoring")
def scoring():
    return get_teams()


@app.route("/team://<team_ip>/")
def scoring2(team_ip):
    team_num = int(team_ip.split(".")[2])
    return get_team(team_num)


if __name__ == "__main__":
    app.send_update_loop_thread = Thread(target=send_update_loop, daemon=True)
    app.send_update_loop_thread.start()

    app.run(host='0.0.0.0', debug=False, port=80)
