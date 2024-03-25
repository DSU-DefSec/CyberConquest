#!/usr/bin/env python3
# @Name: scoring_server.py
# @Project: CyberConquest/CyberConquest2024/scoring
# @Author: Goofables
# @Created: 2024-03-21
import threading
import time
from threading import Thread

import digitalio
from flask import Flask, render_template

import lights

PORT = 80
MIN_SPACE_BETWEEN_CARS = 10
NEW_CAR_RAND_CHANCE = 2
PIXEL_COUNT = 300

# Initialize semaphore
GLOBAL_PIXEL_LOCK = threading.Lock()

app = Flask(__name__, template_folder="templates", static_folder="static")


def header_pin(slot: int) -> digitalio.DigitalInOut:
    """
    Initialize a pin from the pi's header to be an input pull up
    @param slot: the pin to initialize as input
    @return:
    """
    # Get the pin
    p = digitalio.DigitalInOut(slot)
    # Set it as an input pin
    p.direction = digitalio.Direction.INPUT
    # Set to pull up
    p.pull = digitalio.Pull.UP
    return p


def update_loop() -> None:
    """
    Main update cycle
    """
    last = 0
    cycle = 1
    while True:
        # Sleep until the next cycle, or dont sleep if the last tick took too long
        time.sleep(max(0, last - time.time() + cycle))
        last = time.time()


@app.route("/")
def index():
    # Send the index template
    return render_template("index.html")


if __name__ == "__main__":
    # Setup main control loop to run all systems
    app.send_update_loop_thread = Thread(target=update_loop, daemon=True)
    app.send_update_loop_thread.start()

    # Initialize cars and start the controll loop
    app.car_driver = lights.Cars(PIXEL_COUNT)
    app.car_driver.start_loop()

    # Run webapp forever
    app.run(host="0.0.0.0", debug=False, port=PORT)
