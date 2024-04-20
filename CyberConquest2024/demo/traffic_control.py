#!/usr/bin/env python3
# @Name: lights.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-03-25

import dataclasses
import datetime
import enum
import random
import threading
import time
from threading import Thread

import board
import digitalio
import neopixel

PORT = 80
MIN_SPACE_BETWEEN_CARS = 10
CAR_SPAWN_CHANCE = 0.5
MIN_CAR_LENGTH = 0
MAX_CAR_LENGTH = 3

GLOBAL_PIXEL_LOCK = threading.Lock()


class TrafficLightColor(enum.Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2


@dataclasses.dataclass
class TrafficLight:
    """
    Traffic light controller.
    This takes a pin to control each bulb of the traffic light and handles setting their color.
    """

    # GPIO pins to control light bulbs
    red_pin: digitalio.DigitalInOut
    yellow_pin: digitalio.DigitalInOut
    green_pin: digitalio.DigitalInOut

    # Pixel id for where cars should stop for the intersection
    intersection: int

    # Current light color
    color: TrafficLightColor = None

    def __post_init__(self):
        self.red_pin = digitalio.DigitalInOut(self.red_pin)
        self.red_pin.direction = digitalio.Direction.OUTPUT
        self.yellow_pin = digitalio.DigitalInOut(self.yellow_pin)
        self.yellow_pin.direction = digitalio.Direction.OUTPUT
        self.green_pin = digitalio.DigitalInOut(self.green_pin)
        self.green_pin.direction = digitalio.Direction.OUTPUT

    def green(self) -> None:
        """Set traffic light to green"""
        self.red_pin.value = False
        self.yellow_pin.value = False
        self.green_pin.value = True
        self.color = TrafficLightColor.GREEN

    def yellow(self) -> None:
        """Set traffic light to yellow"""
        self.red_pin.value = False
        self.yellow_pin.value = True
        self.green_pin.value = False
        self.color = TrafficLightColor.YELLOW

    def red(self) -> None:
        """Set traffic light to red"""
        self.red_pin.value = True
        self.yellow_pin.value = False
        self.green_pin.value = False
        self.color = TrafficLightColor.RED


def light_generator(
    red_pin,
    yellow_pin,
    green_pin,
):
    pass


def light_factory(red_pin, yellow_pin, green_pin, intersections: list[tuple[int, int]]):
    """
    Create list of traffic lights with the same control pins.

    @param red_pin: Pin id of the red pin
    @param yellow_pin: Pin id of the yellow pin
    @param green_pin: Pin id of the green pin
    @param intersections: List of intersection tuples in the form (line, intersection)
    @return:
    """
    red_pin = digitalio.DigitalInOut(red_pin)
    red_pin.direction = digitalio.Direction.OUTPUT
    yellow_pin = digitalio.DigitalInOut(yellow_pin)
    yellow_pin.direction = digitalio.Direction.OUTPUT
    green_pin = digitalio.DigitalInOut(green_pin)
    green_pin.direction = digitalio.Direction.OUTPUT

    return [TrafficLight(red_pin, yellow_pin, green_pin, line=i[0], intersection=i[1]) for i in intersections]


LIGHTS = [
    TrafficLight(board.D26, board.D13, board.D19, 100),
    TrafficLight(board.D5, board.D0, board.D6, 100),
]


class Cars:
    """
    Controls the car system.
    Spawns random sized cars at random intervals to drive on the road.
    Interfaces with traffic lights to properly slow and stop the cars
    """

    @dataclasses.dataclass
    class Car:
        """
        A single car. It starts with a white light, has `length` lights of `color` and ends with a red light.
        """

        color: tuple = (0, 0, 0)
        position: float = 0
        velocity: float = 0
        accel: float = 0
        length: int = 0
        cid: int = 0

        def change_acc(self, next_obstacle: int):
            """
            Change car's acceleration based on where it is from the next obstacle.
            @param next_obstacle: the closest obstacle
            """
            # set car to break if we are close to the next intersection
            if 0 < next_obstacle - self.position < 2:
                self.accel = -0.5 * 3 / (next_obstacle - self.position)
            else:
                # Car is not near next intersection
                if self.velocity < 0.5:
                    # Car is slow, so accelerate quickly
                    self.accel = random.random() * 0.1
                else:
                    # Car is fast so accelerate quickly
                    self.accel = 0.03

                # Slow car acceleration based on length of car
                self.accel *= 0.9**self.length

        def move_car(self, collide: bool):
            """
            Changes the pixels of the body to move the car along the track.
            @param collide: has the car collided
            """
            self.position += self.velocity
            # Update car velocity
            self.velocity = min(max(self.velocity + self.accel, 0), 1)

            pos = int(self.position)
            # Get the pixel colors for the car (white, color * length, red)
            body = [(255, 255, 255)] + [self.color] * self.length + [(255, 0, 0)]
            for pixel in body:
                # Only set car pixel if it is within the pixels. Prevent out of bounds error
                if 0 <= pos < len(self.pixels):
                    self.pixels[pos] = pixel if not collide else (255, 0, 0)
                pos -= 1
            return pos

    def __init__(self, strip_pin, pixel_count: int):
        """
        Setup the car controller
        @param pixel_count: Number of pixels in the neopixel strip
        """
        self.pixels = neopixel.NeoPixel(
            strip_pin,
            n=pixel_count,
            bpp=3,  # Bits per pixel. Always 3 with neopixel strip
            pixel_order=neopixel.GRB,  # GRB color scheme
            auto_write=False,  # Do not auto sync writes. Use .show()
            brightness=0.1,
        )
        self.cars: list[Cars.Car] = []
        self.total_spawned = 0

        # Should the loop thread still run
        self.active = True
        self.loop_thread = None

    def new_car(self, pos: int = 0) -> None:
        """
        Spawn a new random colored car at the given position
        @param pos: Position to start the car. Normally 0
        """
        self.cars.append(
            Cars.Car(
                color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                velocity=0.1,
                accel=0.01,
                length=random.randint(MIN_CAR_LENGTH, MAX_CAR_LENGTH),
                position=pos,
                cid=self.total_spawned,
            )
        )
        self.total_spawned += 1
        if self.total_spawned % 10 == 0:
            print(f"[{datetime.datetime.now()}] Cars spawned: {self.total_spawned}")

    def car_driving_loop(self) -> None:
        """Main loop to spawn and control cars"""
        while self.active:
            if (
                len(self.cars) == 0
                or self.cars[-1].position > MIN_SPACE_BETWEEN_CARS
                and random.random() < CAR_SPAWN_CHANCE
            ):
                self.new_car()
            with GLOBAL_PIXEL_LOCK:
                self.pixels.fill(0)
            # Next border that a car could run into
            next_obstacle = -1
            to_del = []
            for car in self.cars:
                collide = False
                for light in LIGHTS:
                    # Ignore the light if it is green
                    if light.is_green:
                        continue
                    # If the car is in the intersection run collision code
                    # if light.intersection + car.length >= car.position >= light.intersection:
                    #     for car2 in self.cars:
                    #         if (
                    #             car.cid != car2.cid
                    #             and light.intersection + car2.length + 2 > car2.position >= light.intersection
                    #         ):
                    #             collide = True
                    #             to_del.append(car)
                    #             print(
                    #                 f"{car.cid} <> {car2.cid}"
                    #             )  # with GLOBAL_PIXEL_LOCK:  #    for p in range(int(car.position - car.length * 2), int(car.position + car.length)):  #         self.pixels[p] = (255,0,0)  # self.pixels.show()  # # time.sleep(0.2)  # with GLOBAL_PIXEL_LOCK:  #    for p in range(int(car.position - car.length * 2), int(car.position + car.length)):  #         self.pixels[p] = (0,255,0)  # self.pixels.show()  # # time.sleep(0.2)

                    # If the car is after the intersection then ignore it
                    if car.position >= light.intersection:
                        continue

                    # Set the light as the next border if it is closer than the previous one
                    if car.position < light.intersection < next_obstacle:
                        next_obstacle = light.intersection

                # change car's acceleration based on the next obstacle
                car.change_acc(next_obstacle)

                # Move the car
                # Update next border to be this car so the next car knows that is farthest forward point it can be
                pos = car.move_car(collide)
                next_obstacle = pos

                # Set car to be deleted if the end of it is off the strip of pixels
                if pos > len(self.pixels):
                    to_del.append(car)

            # Delete all cars pending deletion
            for c in to_del:
                self.cars.remove(c)

            # Write the changes to the matrix
            with GLOBAL_PIXEL_LOCK:
                try:
                    self.pixels.show()
                except Exception as e:
                    print(f"Error writing to cars: {e}")  # time.sleep(0.05)

    def __del__(self):
        """Properly cleanup and stop control loop when destroyed"""
        self.active = False
        if self.loop_thread is not None:
            self.loop_thread.join()
            self.loop_thread = None

    def start_loop(self):
        """Start the control loop thread"""
        self.loop_thread = Thread(target=self.car_driving_loop, daemon=True)
        self.loop_thread.start()

    def set_brightness(self, brightness: int):
        """Set brightness of the whole strip"""
        self.pixels.brightness = brightness / 100


if __name__ == "__main__":
    tc = Cars(board.D4, 300)
    while True:
        for l in LIGHTS:
            l.green_pin.value = True
            l.yellow_pin.value = True
            l.red_pin.value = True
        time.sleep(5)
        for l in LIGHTS:
            l.green_pin.value = False
            l.yellow_pin.value = False
            l.red_pin.value = False
        time.sleep(1)
