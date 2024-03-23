#!/usr/bin/env python3
# @Name: scoring_server.py
# @Project: CyberConquest/CyberConquest2024/scoring
# @Author: Goofables
# @Created: 2024-03-21
import dataclasses
import datetime
import threading
import time
from threading import Thread

import board
import digitalio
from flask import Flask

PORT = 80
DOWN_AFTER_FAIL = 10
MAX_SECONDS_BEFORE_CRANE_CHECK = 45
MIN_SPACE_BETWEEN_CARS = 30
NEW_CAR_RAND_CHANCE = 20

GLOBAL_PIXEL_LOCK = threading.Lock()

app = Flask(__name__)


def header_pin(slot: int) -> digitalio.DigitalInOut:
    p = digitalio.DigitalInOut(slot)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP
    return p


@dataclasses.dataclass
class CraneTeam:
    crane_pin: digitalio.DigitalInOut

    crane_down_until: datetime.datetime = datetime.datetime.now()
    crane_on_time: datetime.datetime = datetime.datetime.now()
    crane_off_time: datetime.datetime = datetime.datetime.now()

    def __init__(self, crane):
        self.crane_pin = crane

    @staticmethod
    def down() -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(seconds=DOWN_AFTER_FAIL)

    def update(self):
        if bool(self.crane_pin.value):
            self.crane_on_time = datetime.datetime.now()
        else:
            self.crane_off_time = datetime.datetime.now()

        if datetime.datetime.now() - self.crane_off_time > datetime.timedelta(seconds=MAX_SECONDS_BEFORE_CRANE_CHECK):
            self.crane_down_until = self.down()
        if datetime.datetime.now() - self.crane_on_time > datetime.timedelta(seconds=MAX_SECONDS_BEFORE_CRANE_CHECK):
            self.crane_down_until = self.down()

    def get_status(self) -> bool:
        """
        @return: traffic, crane
        """
        now = datetime.datetime.now()
        return self.crane_down_until < now


teams = {
    "1": CraneTeam(header_pin(board.D20)),
    "2": CraneTeam(header_pin(board.D16)),
    "3": CraneTeam(header_pin(board.D12)),
    "4": CraneTeam(header_pin(board.D21)),
    "5": CraneTeam(header_pin(board.D1)),
    "6": CraneTeam(header_pin(board.D7)),
    "7": CraneTeam(header_pin(board.D8)),
    "8": CraneTeam(header_pin(board.D25)),
}


def update_loop():
    last = 0
    cycle = 0.1
    while True:
        time.sleep(max(0, last - time.time() + cycle))
        for name, team in teams.items():
            team.update()
        last = time.time()


@app.route("/scoring")
def scoring():
    return {n: t.get_status() for n, t in teams.items()}


@app.route("/crane://<team_ip>/")
def score_crane(team_ip):
    team_num = team_ip.split(".")[2]
    try:
        return "SCORING" if teams[team_num].get_status() else "DOWN"
    except KeyError:
        return "INVALID TEAM"


if __name__ == "__main__":
    app.send_update_loop_thread = Thread(target=update_loop, daemon=True)
    app.send_update_loop_thread.start()

    app.run(host="0.0.0.0", debug=False, port=PORT)
