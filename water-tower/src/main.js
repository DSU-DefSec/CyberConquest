const express = require('express')
const {spawn} = require('child_process')
const readline = require('readline')
const app = express()
const port = 3000
const EventEmitter = require('events')

const json_decode = s => eval(`(${s})`)

// Must be 15 on the VM
const BLINKA_MCP2221_RESET_DELAY = 15


// Modified code from https://stackoverflow.com/a/49957823
function streamLineByLine(stream) {
  const line_stream = new EventEmitter();
  let buff = '';

  stream
    .on('data', data => {
      // console.log(`got chunk ${data}`)
      buff += data;
      lines = buff.split(/\r\n|\n/);
      buff = lines.pop();
      lines.forEach(line => line_stream.emit('line', line));
    })
    .on('end', () => {
      if (buff.length > 0) line_stream.emit('line', buff);
    });

  return line_stream;
}


let run_control_system = true
let feedback_state_sensor_value = false

const python_program = spawn('python', ['main.py'], {
  env: Object.assign(Object.create(process.env), {
    "BLINKA_MCP2221": "1",
    "BLINKA_MCP2221_RESET_DELAY": JSON.stringify(BLINKA_MCP2221_RESET_DELAY)
  }),
  shell: true,
  windowsHide: true,
  stdio: ['pipe', 'pipe', 'inherit'],
})

const stdin_lines = streamLineByLine(python_program.stdout)

function on_command_response(cb) {
  stdin_lines.once('line', (line) => {
    console.log("Command response:", line)
    const command_response = json_decode(line)
    cb(command_response)
  })
}

function send_command(command, parameters, cb) {
  python_program.stdin.write(
    JSON.stringify({command, parameters}) + "\n",
    () => {
      on_command_response(cb)
    },
  )
}

app.use(express.static('static'))

app.get('/api/get_board_id', (req, res) => {
  send_command('get_board_id', {}, (com_res) => {
    res.send(`Board id: ${com_res.board_id}`)
  })
})

app.get('/api/set_pump/:value', (req, res) => {
  value = json_decode(req.params.value)
  send_command('pump_set', {value}, (com_res) => {
    res.send(`Set to ${value}`)
  })
})

app.get('/api/get_sensor_value', (req, res) => {
  send_command('get_sensor_value', {}, (com_res) => {
    res.send(JSON.stringify({sensor_value: com_res.sensor_value}))
  })
})

app.get('/api/get_pump_value', (req, res) => {
  send_command('get_pump_value', {}, (com_res) => {
    res.send(JSON.stringify({pump_value: com_res.pump_value}))
  })
})


app.get('/api/set_override/:value', (req, res) => {
  value = json_decode(req.params.value)
  run_control_system = !value
})

on_command_response((res) => {
  console.log(`Command is ${res.status}`)

  setInterval(() => {
    send_command('get_sensor_value', {}, com_res => {
      feedback_state_sensor_value = com_res.sensor_value
    })

    if (run_control_system) {
      send_command('pump_set', {value: !feedback_state_sensor_value}, com_res => {
      })
    }
  }, 1000)

  app.listen(port, () => {
    console.log(`Listening on port ${port}`)
  })
})
