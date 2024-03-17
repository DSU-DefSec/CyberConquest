#!/usr/bin/env python
# @Name: test-neo.py
# @Project: CyberConquest/examples
# @Author: Goofables
# @Created: 2/21/23

import board
import neopixel_spi as neopixel

NUM_PIXELS = 30 * 5
AMT = 15
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
DELAY = 0.5

pixels = neopixel.NeoPixel_SPI(
    board.SPI(),
    NUM_PIXELS,
    bpp=4,
    pixel_order=neopixel.GRBW,
    auto_write=False,
    brightness=1
)
colors = [(255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 255, 255)]

# for p in range(NUM_PIXELS):
#     pixels[p] = (255,255,255,255)
# pixels.show()
# sleep(1)
pixels.fill(0)

for i in range(AMT):
    a = int(NUM_PIXELS / AMT * i)
    pixels[i] = (int((i / AMT) * 255), 0, 255 - int((i / AMT) * 255))
    # pixels[i] = colors[random.randint(0, len(colors) - 1)]
    # pixels[i] = (255,255,255,255)
pixels.show()
# pixels.fill((255, 255, 255, 255))

while True:
    tmp = pixels[-1]
    for p in range(NUM_PIXELS - 1, 0, -1):
        pixels[p] = pixels[p - 1]
    pixels[0] = tmp
    # if pixels[0][0] == 0:
    # print("Random")
    # pixels[random.randint(0, NUM_PIXELS - 1)] = colors[random.randint(0, len(colors) - 1)]
    # for a in range(AMT):
    #     for i in range(int(NUM_PIXELS/AMT)):
    # pixels[i*AMT+a] = colors[random.randint(0, len(colors) - 1)]
    # pixels[p] = colors[random.randint(0, len(colors) - 1)]
    pixels.show()
    # sleep(0.002)
    #     for i in range(int(NUM_PIXELS/AMT)):
    #         pixels[i*AMT+a] = 0
    # for a in range(AMT):
    #     for i in range(int(NUM_PIXELS/AMT)):
    #         pixels[i*AMT+a] = 0
    # sleep(0.2)
    # pixels.fill(0)
    # sleep(0.2)
