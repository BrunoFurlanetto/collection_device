import json

import utime
from random import choice, randint
from time import sleep

from machine import Pin


def tactile_choice_familiarization():
    print('Familiarização iniciada!')

    with open('config/ports_config.json', 'r') as f:
        PORTS_CONFIG = json.load(f)

    port_right = PORTS_CONFIG['RIGHT_VIBRACALL']
    port_left = PORTS_CONFIG['LEFT_VIBRACALL']
    port_right_button = PORTS_CONFIG['RIGHT_PUSH_BUTTON']
    port_left_button = PORTS_CONFIG['LEFT_PUSH_BUTTON']

    left = Pin(port_left, Pin.OUT)
    right = Pin(port_right, Pin.OUT)
    push_button_left = Pin(port_left_button, Pin.IN)
    push_button_right = Pin(port_right_button, Pin.IN)
    left_group = [push_button_left, left]
    right_group = [push_button_right, right]
    possible_choice = [right_group, left_group]

    for _ in range(0, 5):
        choice_side = choice(possible_choice)
        another_side = right_group if choice_side == left_group else left_group
        sleep(randint(3, 7))

        count = utime.ticks_ms()
        choice_side[1].value(True)

        while True:
            success_state = choice_side[0].value()
            error_state = another_side[0].value()

            if success_state:
                choice_side[1].value(False)

                break
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                choice_side[1].value(False)

                break

    print('Familiarização finalizada com sucesso!')


def tactile_simple_familiarization():
    print('Familiarização iniciada!')

    with open('config/ports_config.json', 'r') as f:
        PORTS_CONFIG = json.load(f)

    with open('config/session_config.json', 'r') as f:
        SESSION_CONFIG = json.load(f)

    port_vibracall = PORTS_CONFIG['RIGHT_VIBRACALL'] if SESSION_CONFIG['DOMINANT_HAND'] == 'D' else PORTS_CONFIG['LEFT_VIBRACALL']
    port_push_button = PORTS_CONFIG['RIGHT_PUSH_BUTTON'] if SESSION_CONFIG['DOMINANT_HAND'] == 'D' else PORTS_CONFIG['LEFT_PUSH_BUTTON']

    vibracall = Pin(port_vibracall, Pin.OUT)
    push_button = Pin(port_push_button, Pin.IN)

    for _ in range(0, 3):
        sleep(randint(3, 7))
        count = utime.ticks_ms()
        vibracall.value(True)

        while True:
            success_state = push_button.value()

            if success_state:
                vibracall.value(0)

                break
            elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                vibracall.value(False)

                break

    print('Familiarização finalizada com sucesso!')
