import json
from time import sleep
from random import randint, choice
import utime
from machine import Pin


def visual_choice_familiarization():
    print('Familiarizção Iniciada.')

    with open('config/ports_config.json', 'r') as f:
        PORTS_CONFIG = json.load(f)

    port_right_led = PORTS_CONFIG['RIGHT_LED']
    port_left_led = PORTS_CONFIG['LEFT_LED']
    port_right_button = PORTS_CONFIG['RIGHT_PUSH_BUTTON']
    port_left_button = PORTS_CONFIG['LEFT_PUSH_BUTTON']

    right_led = Pin(port_right_led, Pin.OUT)
    left_led = Pin(port_left_led, Pin.OUT)
    push_button_right = Pin(port_right_button, Pin.IN)
    push_button_left = Pin(port_left_button, Pin.IN)
    right_group = [push_button_right, right_led]
    left_group = [push_button_left, left_led]
    possible_choice = [right_group, left_group]

    for i in range(0, 5):
        choice_led = choice(possible_choice)
        another_led = left_group if choice_led == right_group else right_group

        sleep(randint(3, 7))

        count = utime.ticks_ms()
        choice_led[1].value(True)

        while True:
            success_state = choice_led[0].value()
            error_state = another_led[0].value()

            if success_state:
                choice_led[1].value(False)

                break
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                choice_led[1].value(False)

                break

    print('Familiarização finalizada com sucesso!')


def visual_simple_familiarization():
    print('Familiarização iniciada!')

    with open('config/ports_config.json', 'r') as f:
        PORTS_CONFIG = json.load(f)

    with open('config/session_config.json', 'r') as f:
        SESSION_CONFIG = json.load(f)

    port_led = PORTS_CONFIG['LEFT_LED']
    port_push_button = PORTS_CONFIG['RIGHT_PUSH_BUTTON'] if SESSION_CONFIG['DOMINANT_HAND'] == 'D' else PORTS_CONFIG['LEFT_PUSH_BUTTON']
    led = Pin(port_led, Pin.OUT)
    push_button = Pin(port_push_button, Pin.IN)

    for _ in range(0, 3):
        sleep(randint(3, 7))
        count = utime.ticks_ms()
        led.value(True)

        while True:
            success_state = push_button.value()

            if success_state:
                led.value(False)

                break
            elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                led.value(False)

                break

    print('Familiarização finalizada com sucesso!')
