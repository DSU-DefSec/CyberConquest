#!/usr/bin/env python3
# @Name: scoring_server.py
# @Project: CyberConquest/CyberConquest2024/scoring
# @Author: Goofables
# @Created: 2024-03-21
import threading
import time
from threading import Thread

import digitalio
from flask import Flask, request, render_template

import lights

PORT = 80
MIN_SPACE_BETWEEN_CARS = 10
NEW_CAR_RAND_CHANCE = 2

GLOBAL_PIXEL_LOCK = threading.Lock()

app = Flask(__name__)

def header_pin(slot: int) -> digitalio.DigitalInOut:
    p = digitalio.DigitalInOut(slot)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP
    return p

def update_loop():
    last = 0
    cycle = 1
    while True:
        time.sleep(max(0, last - time.time() + cycle))
        last = time.time()

@app.route("/")
def scoring():
    return render_template("index.html")

if __name__ == "__main__":
    app.send_update_loop_thread = Thread(target=update_loop, daemon=True)
    app.send_update_loop_thread.start()

    app.car_driver = lights.Cars(1500)
    app.car_driver.start_loop()

    app.run(host="0.0.0.0", debug=False, port=PORT)