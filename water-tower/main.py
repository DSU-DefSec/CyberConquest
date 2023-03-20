import sys
import board
import digitalio
import json

print("MCP2221 Ready", file=sys.stderr, flush=True)

pump_pin = board.G0
sensor_pin = board.G1

pump = digitalio.DigitalInOut(pump_pin)
pump.direction = digitalio.Direction.OUTPUT
pump.value = True

sensor = digitalio.DigitalInOut(sensor_pin)
sensor.direction = digitalio.Direction.INPUT

commands = {}
def register_command(name=None):
    def helper(func):
        command_name = func.__name__ if name is None else name
        if command_name in commands:
            raise ValueError(f"Command name '{command_name}' must be unique")
        commands[command_name] = func
        return func
    return helper


@register_command()
def get_board_id():
    return {"board_id": board.board_id}

@register_command()
def pump_set(value):
    pump.value = value
    return {"status": f"Turning Pump to {value}"}

@register_command()
def get_pump_value():
    return {"pump_value": pump.value}

@register_command()
def get_sensor_value():
    return {"sensor_value": sensor.value}


def send_response(data):
    print(json.dumps(data), flush=True)

send_response({"status": "ready"})

for line in sys.stdin:
    data = json.loads(line.strip())

    command = data["command"]
    parameters = data["parameters"]

    if command in commands:
        send_response(commands[command](**parameters))
    else:
        send_response({"error": f"Unknown command '{command}'"})