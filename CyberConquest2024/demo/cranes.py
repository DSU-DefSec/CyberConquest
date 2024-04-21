#!/usr/bin/env python3
# @Name: cranes.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-03-25
import dataclasses
import time

import board
import digitalio


@dataclasses.dataclass
class Crane:
    direction: bool
    button_state: bool
    relay_1_pin: digitalio.DigitalInOut
    relay_2_pin: digitalio.DigitalInOut
    switch_pin: digitalio.DigitalInOut

    def __init__(self, relay_1_pin, relay_2_pin, switch_pin):
        """
        Set up the pins used by the cranes.
        @param relay_1_pin: Pin for the first relay.
        @param relay_2_pin: Pin for the second relay.
        @param switch_pin: Pin for the limit switch.
        """
        self.relay_1_pin = digitalio.DigitalInOut(relay_1_pin)
        self.relay_1_pin.direction = digitalio.Direction.OUTPUT

        self.relay_2_pin = digitalio.DigitalInOut(relay_2_pin)
        self.relay_2_pin.direction = digitalio.Direction.OUTPUT

        self.switch_pin = digitalio.DigitalInOut(switch_pin)
        self.switch_pin.direction = digitalio.Direction.INPUT

        # Beware! I have no idea what the default values for this should be.
        self.direction = False
        self.button_state = False

        self.freeze_time = None
        self.last_run = None

    def crane_dir_1(self) -> None:
        """Direction one"""
        self.relay_1_pin.value = True
        self.relay_2_pin.value = False

    def crane_dir_2(self) -> None:
        """Direction two"""
        self.relay_1_pin.value = False
        self.relay_2_pin.value = True

    def crane_stop(self) -> None:
        """Stop the crane"""
        self.relay_1_pin.value = False
        self.relay_2_pin.value = False
        self.freeze_time = time.time() + 0.2

    def tick(self):
        """Tick the cranes. Must be run at least every 0.1 seconds or cranes may crash"""
        if self.last_run is not None:
            assert time.time() - self.last_run > 0.1
        self.last_run = time.time()

        if self.freeze_time is None:
            if self.direction:
                self.crane_dir_1()
            else:
                self.crane_dir_2()
        else:
            if self.freeze_time < time.time():
                self.freeze_time = None

        # If switch is in a different state than the last run
        if self.switch_pin.value != self.button_state:
            # Toggle the last state remembered to match the current state
            self.button_state = not self.button_state

            # If the current state of the switch is grounded (pressed)
            if self.button_state is False:
                # Stop the crane and toggle the direction
                self.direction = not self.direction
                self.crane_stop()

    def __del__(self):
        self.crane_stop()


if __name__ == "__main__":
    cranes = [
        Crane(board.G1, board.G2, board.G0),  # Crane(board.G1, board.G2, board.G0),
        # Crane(board.G1, board.G2, board.G0),
        # Crane(board.G1, board.G2, board.G0),
    ]
    while True:
        for c in cranes:
            c.tick()
        time.sleep(0.1)
