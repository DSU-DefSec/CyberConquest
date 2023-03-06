# Cyber Conquest 2023

Code for the scored services at Cyber Conquest 2023 at DakotaCon!

## Traffic Light

A flask based webapp that shows the current state of the traffic light and allows for modification of the lights
operating code.

##### Instruction format

```python
[
    [  # pixel 0
        "<command>:<arguments>",
        "<command>:<arguments>"
    ],
    [  # pixel 1
        "<command>:<arguments>"
    ],
]
```

##### Commands

```
set:R,G,B,W     # Set pixel to value
random:         # Set pixel to random
wait:20         # milliseconds
shell:<command> # Execute system command
```

### Water Tower

???

### Wind Turbine

A power generating wind turbine controlled via an SMB share.

Reads the Air-Velocity-Input from `spinny_speed.avi` then spins at that speed to generate power. Power is outputted
into `buzzzt.exe` in the form of EXact-Electrons