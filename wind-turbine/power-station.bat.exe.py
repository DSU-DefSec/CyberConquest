#!/usr/bin/env python
# @Name: power-station.bat.exe.py
# @Project: CyberConquest/wind-turbine
# @Author: Goofables
# @Created: 2/25/23

from time import sleep

from adafruit_motorkit import MotorKit


class WindMillController:
    def __init__(self):
        self.kit = MotorKit()
        self.motor = self.kit.motor1

    def set_speed(self, speed: float):
        # print(speed)
        # if speed != 0:
        self.motor.throttle = min(max(speed / 100, -1), 1)
        # else:
        #     self.motor.throttle = 0


windmill = WindMillController()

"""
docs:
The speed for the windmill is loaded every second from spinny_speed.msi, a Multidirectional Speed Input file
The speed for the windmill is loaded every second from spinny_speed.avi, a Air Velocity input
The power generated is outputted to zappy_zaps.exe a EXact Electron file
"""
speed = 0

while True:
    try:
        with open("data/buzzzt.exe", "rb") as f:
            data = f.read()
            num = int.from_bytes(data[0x0001152:0x0001156], "little")
    except OSError as e:
        print("Recreating")
        data = bytes.fromhex(
            "7f454c4602010100000000000000000003003e000100000060100000000000004000000000000000e03000000000000000000000400038000c004000190018000600000004000000400000000000000040000000000000004000000000000000a002000000000000a002000000000000080000000000000003000000040000001803000000000000180300000000000018030000000000001c000000000000001c000000000000000100000000000000010000000400000000000000000000000000000000000000000000000000000028060000000000002806000000000000001000000000000001000000050000000010000000000000001000000000000000100000000000008101000000000000810100000000000000100000000000000100000004000000002000000000000000200000000000000020000000000000fc00000000000000fc0000000000000000100000000000000100000006000000b82d000000000000b83d000000000000b83d0000000000005802000000000000600200000000000000100000000000000200000006000000c82d000000000000c83d000000000000c83d000000000000f001000000000000f00100000000000008000000000000000400000004000000000000000000000038030000000000000000000000000000000000000000000000000000000000000800000000000000040000000400000000000000000000006803000000000000000000000000000000000000000000000000000000000000080000000000000053e574640400000000000000000000003803000000000000000000000000000000000000000000000000000000000000080000000000000050e57464040000001c200000000000001c200000000000001c2000000000000034000000000000003400000000000000040000000000000051e574640600000000000000000000000000000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002f6c696236342f6c642d6c696e75782d7838362d36342e736f2e3200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000006000000010000000600000000008100000000000600000000000000d165ce6d000000000000000000000000000000000000000000000000000000001000000012000000000000000000000000000000000000004a0000002000000000000000000000000000000000000000220000001200000000000000000000000000000000000000660000002000000000000000000000000000000000000000750000002000000000000000000000000000000000000000010000002200000000000000000000000000000000000000005f5f6378615f66696e616c697a65005f5f6c6962635f73746172745f6d61696e007072696e7466006c6962632e736f2e3600474c4942435f322e322e3500474c4942435f322e3334005f49544d5f64657265676973746572544d436c6f6e655461626c65005f5f676d6f6e5f73746172745f5f005f49544d5f7265676973746572544d436c6f6e655461626c6500000000020001000300010001000300000001000200290000001000000000000000751a6909000003003300000010000000b4919606000002003f00000000000000b83d00000000000008000000000000004011000000000000c03d00000000000008000000000000000011000000000000084000000000000008000000000000000840000000000000d83f00000000000006000000010000000000000000000000e03f00000000000006000000020000000000000000000000e83f00000000000006000000040000000000000000000000f03f00000000000006000000050000000000000000000000f83f00000000000006000000060000000000000000000000d03f00000000000007000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f30f1efa4883ec08488b05d92f00004885c07402ffd04883c408c30000000000ff359a2f0000f2ff259b2f00000f1f00f30f1efa6800000000f2e9e1ffffff90f30f1efaf2ff25ad2f00000f1f440000f30f1efaf2ff25752f00000f1f440000f30f1efa31ed4989d15e4889e24883e4f050544531c031c9488d3dca000000ff15532f0000f4662e0f1f840000000000488d3d792f0000488d05722f00004839f87415488b05362f00004885c07409ffe00f1f8000000000c30f1f8000000000488d3d492f0000488d35422f00004829fe4889f048c1ee3f48c1f8034801c648d1fe7414488b05052f00004885c07408ffe0660f1f440000c30f1f8000000000f30f1efa803d052f000000752b5548833de22e0000004889e5740c488b3de62e0000e819ffffffe864ffffffc605dd2e0000015dc30f1f00c30f1f8000000000f30f1efae977fffffff30f1efa554889e5be00000000488d05a70e00004889c7b800000000e8e6feffffb8000000005dc3000000f30f1efa4883ec084883c408c300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000200506f7765722067656e6572617465643a2025640a00000000011b033b300000000500000004f0ffff6400000024f0ffff8c00000034f0ffffa400000044f0ffff4c0000002df1ffffbc0000001400000000000000017a5200017810011b0c070890010000140000001c000000f0efffff260000000044071000000000240000003400000098efffff20000000000e10460e184a0f0b770880003f1a3a2a33242200000000140000005c00000090efffff100000000000000000000000140000007400000088efffff1000000000000000000000001c0000008c00000069f0ffff2800000000450e108602430d065f0c070800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040110000000000000011000000000000010000000000000029000000000000000c0000000000000000100000000000000d0000000000000074110000000000001900000000000000b83d0000000000001b0000000000000008000000000000001a00000000000000c03d0000000000001c000000000000000800000000000000f5feff6f00000000b003000000000000050000000000000080040000000000000600000000000000d8030000000000000a000000000000008f000000000000000b000000000000001800000000000000150000000000000000000000000000000300000000000000b83f000000000000020000000000000018000000000000001400000000000000070000000000000017000000000000001006000000000000070000000000000050050000000000000800000000000000c000000000000000090000000000000018000000000000001e000000000000000800000000000000fbffff6f000000000100000800000000feffff6f000000002005000000000000ffffff6f000000000100000000000000f0ffff6f000000001005000000000000f9ffff6f0000000003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c83d0000000000000000000000000000000000000000000030100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000840000000000000002e7368737472746162002e696e74657270002e676e752e68617368002e64796e73796d002e64796e737472002e676e752e76657273696f6e002e676e752e76657273696f6e5f72002e72656c612e64796e002e72656c612e706c74002e696e6974002e706c742e676f74002e706c742e736563002e74657874002e66696e69002e726f64617461002e65685f6672616d655f686472002e65685f6672616d65002e696e69745f6172726179002e66696e695f6172726179002e64796e616d6963002e64617461002e62737300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b000000010000000200000000000000180300000000000018030000000000001c0000000000000000000000000000000100000000000000000000000000000013000000f6ffff6f0200000000000000b003000000000000b00300000000000024000000000000000300000000000000080000000000000000000000000000001d0000000b0000000200000000000000d803000000000000d803000000000000a80000000000000004000000010000000800000000000000180000000000000025000000030000000200000000000000800400000000000080040000000000008f000000000000000000000000000000010000000000000000000000000000002d000000ffffff6f0200000000000000100500000000000010050000000000000e000000000000000300000000000000020000000000000002000000000000003a000000feffff6f02000000000000002005000000000000200500000000000030000000000000000400000001000000080000000000000000000000000000004900000004000000020000000000000050050000000000005005000000000000c000000000000000030000000000000008000000000000001800000000000000530000000400000042000000000000001006000000000000100600000000000018000000000000000300000015000000080000000000000018000000000000005d000000010000000600000000000000001000000000000000100000000000001b0000000000000000000000000000000400000000000000000000000000000058000000010000000600000000000000201000000000000020100000000000002000000000000000000000000000000010000000000000001000000000000000630000000100000006000000000000004010000000000000401000000000000010000000000000000000000000000000100000000000000010000000000000006c000000010000000600000000000000501000000000000050100000000000001000000000000000000000000000000010000000000000001000000000000000750000000100000006000000000000006010000000000000601000000000000011010000000000000000000000000000100000000000000000000000000000007b000000010000000600000000000000741100000000000074110000000000000d0000000000000000000000000000000400000000000000000000000000000081000000010000000200000000000000002000000000000000200000000000001900000000000000000000000000000004000000000000000000000000000000890000000100000002000000000000001c200000000000001c2000000000000034000000000000000000000000000000040000000000000000000000000000009700000001000000020000000000000050200000000000005020000000000000ac00000000000000000000000000000008000000000000000000000000000000a10000000e0000000300000000000000b83d000000000000b82d0000000000000800000000000000000000000000000008000000000000000800000000000000ad0000000f0000000300000000000000c03d000000000000c02d0000000000000800000000000000000000000000000008000000000000000800000000000000b9000000060000000300000000000000c83d000000000000c82d000000000000f00100000000000004000000000000000800000000000000100000000000000067000000010000000300000000000000b83f000000000000b82f0000000000004800000000000000000000000000000008000000000000000800000000000000c2000000010000000300000000000000004000000000000000300000000000001000000000000000000000000000000008000000000000000000000000000000c80000000800000003000000000000001040000000000000103000000000000008000000000000000000000000000000010000000000000000000000000000000100000003000000000000000000000000000000000000001030000000000000cd00000000000000000000000000000001000000000000000000000000000000"
        )
        num = 0

    num += speed
    num &= 0xffffffff

    while True:
        try:
            with open("data/buzzzt.exe", "wb") as f:
                f.write(data[:0x0001152] + num.to_bytes(4, "little") + data[0x0001156:])
                break
        except OSError as e:
            if e.errno == 26:
                print("Waiting for output file to close")
                sleep(0.01)
                continue

    print(f"Power generated: {num}")

    try:
        with open("data/spinny_speed.avi") as f:
            speed = int(f.read().strip())
    except OSError:
        print("Could not read config")

    windmill.set_speed(speed)

    sleep(10)
