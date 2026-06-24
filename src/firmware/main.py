import sys
import uselect
import json

from machine import Pin, PWM
from time import sleep

from protocols.auditory.familiarization import auditory_choice_familiarization, auditory_simple_familiarization
from protocols.auditory.main_test import auditory_choice_test, auditory_simple_test
from protocols.tactile.familiarization import tactile_choice_familiarization, tactile_simple_familiarization
from protocols.tactile.main_test import tactile_simple_test, tactile_choice_test
from protocols.visual.familiarization import visual_simple_familiarization, visual_choice_familiarization
from protocols.visual.main_test import visual_simple_test, visual_choice_test

serialPoll = uselect.poll()
serialPoll.register(sys.stdin, uselect.POLLIN)

# Default GPIO pin numbers (overridden by ports_config.json when available)
_DEFAULT_PINS = {
    "RIGHT_LED": 2,
    "LEFT_LED": 14,
    "RIGHT_BUZZER": 18,
    "LEFT_BUZZER": 32,
    "RIGHT_VIBRACALL": 5,
    "LEFT_VIBRACALL": 33,
    "RIGHT_PUSH_BUTTON": 19,
    "LEFT_PUSH_BUTTON": 12,
}

# Runtime state for debug mode
_debug_state = {
    "led_r": False,
    "led_l": False,
    "buz_r": False,
    "buz_l": False,
    "vib_r": False,
    "vib_l": False,
    "btn_listen": False,
}

# Active hardware objects (kept alive while toggled ON)
_debug_hw = {
    "led_r": None,
    "led_l": None,
    "buz_r": None,
    "buz_l": None,
    "vib_r": None,
    "vib_l": None,
    "btn_r": None,
    "btn_l": None,
}


def _load_pins():
    """Load pin configuration from JSON file, falling back to defaults."""
    try:
        with open('config/ports_config.json', 'r') as f:
            cfg = json.load(f)
        return cfg
    except Exception:
        return _DEFAULT_PINS


def _get_pin(key):
    """Return the GPIO number for a given config key."""
    pins = _load_pins()
    return pins.get(key, _DEFAULT_PINS.get(key))


# ── Debug handlers ──────────────────────────────────────────────────────────

def _handle_ping():
    sys.stdout.write('PONG\n')


def _handle_led(side, state):
    """Toggle an LED on or off."""
    key = 'RIGHT_LED' if side == 'R' else 'LEFT_LED'
    hw_key = 'led_r' if side == 'R' else 'led_l'
    pin_num = _get_pin(key)

    if state == 'ON':
        led = Pin(pin_num, Pin.OUT)
        led.value(1)
        _debug_hw[hw_key] = led
        _debug_state[hw_key] = True
    else:
        if _debug_hw[hw_key] is not None:
            _debug_hw[hw_key].value(0)
        else:
            Pin(pin_num, Pin.OUT).value(0)
        _debug_hw[hw_key] = None
        _debug_state[hw_key] = False

    sys.stdout.write('OK\n')


def _handle_buz(side, state):
    """Toggle a buzzer on (500 Hz) or off."""
    key = 'RIGHT_BUZZER' if side == 'R' else 'LEFT_BUZZER'
    hw_key = 'buz_r' if side == 'R' else 'buz_l'
    pin_num = _get_pin(key)

    if state == 'ON':
        pin = Pin(pin_num, Pin.OUT)
        pin.value(0)
        sleep(0.01)
        pwm = PWM(pin, freq=500, duty_u16=32768)  # ~50% duty cycle
        sleep(0.01)
        _debug_hw[hw_key] = (pwm, pin_num)
        _debug_state[hw_key] = True
    else:
        if _debug_hw[hw_key] is not None:
            pwm, pnum = _debug_hw[hw_key]
            pwm.duty_u16(0)
            sleep(0.01)
            pwm.deinit()
            Pin(pnum, Pin.OUT).value(0)
        else:
            Pin(pin_num, Pin.OUT).value(0)
        _debug_hw[hw_key] = None
        _debug_state[hw_key] = False

    sys.stdout.write('OK\n')


def _handle_vib(side, state):
    """Toggle a vibracall on or off."""
    key = 'RIGHT_VIBRACALL' if side == 'R' else 'LEFT_VIBRACALL'
    hw_key = 'vib_r' if side == 'R' else 'vib_l'
    pin_num = _get_pin(key)

    if state == 'ON':
        vib = Pin(pin_num, Pin.OUT)
        vib.value(1)
        _debug_hw[hw_key] = vib
        _debug_state[hw_key] = True
    else:
        if _debug_hw[hw_key] is not None:
            _debug_hw[hw_key].value(0)
        else:
            Pin(pin_num, Pin.OUT).value(0)
        _debug_hw[hw_key] = None
        _debug_state[hw_key] = False

    sys.stdout.write('OK\n')


def _handle_btn_listen():
    """Start listening for button presses and report them."""
    _debug_state['btn_listen'] = True
    sys.stdout.write('LISTEN:START\n')

    pin_r = _get_pin('RIGHT_PUSH_BUTTON')
    pin_l = _get_pin('LEFT_PUSH_BUTTON')
    btn_r = Pin(pin_r, Pin.IN)
    btn_l = Pin(pin_l, Pin.IN)
    _debug_hw['btn_r'] = btn_r
    _debug_hw['btn_l'] = btn_l

    # Poll buttons until STOP command arrives
    prev_r = 0
    prev_l = 0

    while _debug_state['btn_listen']:
        # Non-blocking check for incoming STOP command
        if serialPoll.poll(0):
            incoming = sys.stdin.read(1)
            # Buffer the character — if we see 'D' start accumulating
            # For simplicity: read rest of STOP command
            buf = incoming
            while len(buf) < 11:  # 'D:BTN:STOP\n' = 11 chars
                if serialPoll.poll(10):
                    buf += sys.stdin.read(1)
                    if buf.endswith('\n'):
                        break
                else:
                    break
            if buf.strip() == 'D:BTN:STOP':
                _debug_state['btn_listen'] = False
                break

        # Detect rising edge on right button
        cur_r = btn_r.value()
        if cur_r and not prev_r:
            sys.stdout.write('BTN:R\n')
        prev_r = cur_r

        # Detect rising edge on left button
        cur_l = btn_l.value()
        if cur_l and not prev_l:
            sys.stdout.write('BTN:L\n')
        prev_l = cur_l

        sleep(0.01)

    _debug_hw['btn_r'] = None
    _debug_hw['btn_l'] = None
    sys.stdout.write('LISTEN:STOP\n')


def _handle_btn_stop():
    """Stop button listening (called when already exited the listen loop)."""
    _debug_state['btn_listen'] = False
    sys.stdout.write('LISTEN:STOP\n')


def _handle_reset():
    """Turn off all debug components and report OK."""
    pins = _load_pins()

    # LEDs off
    for key in ('RIGHT_LED', 'LEFT_LED'):
        try:
            Pin(pins.get(key, _DEFAULT_PINS[key]), Pin.OUT).value(0)
        except Exception:
            pass

    # Buzzers off
    for hw_key, pin_key in (('buz_r', 'RIGHT_BUZZER'), ('buz_l', 'LEFT_BUZZER')):
        if _debug_hw[hw_key] is not None:
            try:
                pwm, pnum = _debug_hw[hw_key]
                pwm.duty_u16(0)
                sleep(0.01)
                pwm.deinit()
                Pin(pnum, Pin.OUT).value(0)
            except Exception:
                pass
            _debug_hw[hw_key] = None
        else:
            try:
                Pin(pins.get(pin_key, _DEFAULT_PINS[pin_key]), Pin.OUT).value(0)
            except Exception:
                pass

    # Vibracalls off
    for key in ('RIGHT_VIBRACALL', 'LEFT_VIBRACALL'):
        try:
            Pin(pins.get(key, _DEFAULT_PINS[key]), Pin.OUT).value(0)
        except Exception:
            pass

    # Reset state tracking
    for k in _debug_state:
        _debug_state[k] = False
    for k in _debug_hw:
        _debug_hw[k] = None

    sys.stdout.write('RESET:OK\n')


def _handle_debug_command(cmd):
    """Dispatch a D:* debug command."""
    # D:RESET
    if cmd == 'D:RESET':
        _handle_reset()
        return

    # D:BTN:LISTEN / D:BTN:STOP
    if cmd == 'D:BTN:LISTEN':
        _handle_btn_listen()
        return
    if cmd == 'D:BTN:STOP':
        _handle_btn_stop()
        return

    # D:<COMPONENT>_<SIDE>:<STATE>  e.g. D:LED_R:ON
    parts = cmd.split(':')  # ['D', 'LED_R', 'ON']
    if len(parts) != 3:
        sys.stdout.write('ERROR:INVALID_DEBUG_COMMAND\n')
        return

    component_side = parts[1]  # e.g. 'LED_R'
    state = parts[2]           # 'ON' or 'OFF'

    if state not in ('ON', 'OFF'):
        sys.stdout.write('ERROR:INVALID_STATE\n')
        return

    if '_' not in component_side:
        sys.stdout.write('ERROR:INVALID_COMPONENT\n')
        return

    component, side = component_side.rsplit('_', 1)  # 'LED', 'R'

    if side not in ('R', 'L'):
        sys.stdout.write('ERROR:INVALID_SIDE\n')
        return

    if component == 'LED':
        _handle_led(side, state)
    elif component == 'BUZ':
        _handle_buz(side, state)
    elif component == 'VIB':
        _handle_vib(side, state)
    else:
        sys.stdout.write('ERROR:UNKNOWN_COMPONENT\n')


def handle_command(command):
    """
    Handle a command received over serial.

    :param command: (String) the command to handle
    """
    if not command:  # ignora None ou string vazia
        return

    cmd = command.strip()

    # PING — debug connection test
    if cmd == 'PING':
        _handle_ping()
        return

    # D:* — debug component commands
    if cmd.startswith('D:'):
        _handle_debug_command(cmd)
        return

    # se iniciar com T:
    if cmd.startswith("T"):
        via = cmd[1]
        tipo = cmd[2]

        if via == 'V':
            if tipo == 'S':
                visual_simple_test()
                sys.stdout.write('SUCCESS\n')
            else:
                visual_choice_test()
                sys.stdout.write('SUCCESS\n')

        if via == 'A':
            if tipo == 'S':
                auditory_simple_test()
                sys.stdout.write('SUCCESS\n')
            else:
                auditory_choice_test()
                sys.stdout.write('SUCCESS\n')

        if via == 'T':
            if tipo == 'S':
                tactile_simple_test()
                sys.stdout.write('SUCCESS\n')
            else:
                tactile_choice_test()
                sys.stdout.write('SUCCESS\n')
        else:
            sys.stdout.write("ERROR:INVALID_COMMAND\n")
    elif cmd.startswith("F"):
        via = cmd[1]
        tipo = cmd[2]

        if via == 'V':
            if tipo == 'S':
                visual_simple_familiarization()
                sys.stdout.write('SUCCESS\n')
            else:
                visual_choice_familiarization()
                sys.stdout.write('SUCCESS\n')

        if via == 'A':
            if tipo == 'S':
                auditory_simple_familiarization()
                sys.stdout.write('SUCCESS\n')
            else:
                auditory_choice_familiarization()
                sys.stdout.write('SUCCESS\n')

        if via == 'T':
            if tipo == 'S':
                tactile_simple_familiarization()
                sys.stdout.write('SUCCESS\n')
            else:
                tactile_choice_familiarization()
                sys.stdout.write('SUCCESS\n')
    else:
        sys.stdout.write("ERROR:UNKNOWN_COMMAND\n")


# Serial read buffer for hybrid protocol
_serial_buffer = ""


def readSerial():
    """
    Reads from serial using a hybrid strategy:
    - Reads character by character
    - If a newline is received: processes the full buffered line
    - If buffer reaches exactly 3 chars AND matches a legacy command (starts with T or F):
      processes immediately (supports ESPSerialClient which sends no newline)
    - Returns the command string to process, or None if nothing ready

    :return: command string or None
    """
    global _serial_buffer

    if not serialPoll.poll(0):
        return None

    ch = sys.stdin.read(1)
    if not ch:
        return None

    _serial_buffer += ch

    # Full line received
    if ch == '\n':
        cmd = _serial_buffer.strip()
        _serial_buffer = ""
        return cmd if cmd else None

    # Legacy 3-char command without newline (ESPSerialClient protocol)
    if len(_serial_buffer) == 3 and (_serial_buffer[0] in ('T', 'F')):
        cmd = _serial_buffer.strip()
        _serial_buffer = ""
        return cmd if cmd else None

    return None


# loop principal
while True:
    c = readSerial()
    if c is not None:
        handle_command(c)
