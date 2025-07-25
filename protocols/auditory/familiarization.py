import json
from random import randint, choice
from time import sleep

import utime
from machine import PWM, Pin


def auditory_choice_familiarization():
    print('Familiarização iniciada!')

    with open('config/ports_config.json', 'r') as f:
        PORTS_CONFIG = json.load(f)

    port_right_beeper = PORTS_CONFIG['RIGHT_BUZZER']
    port_left_beeper = PORTS_CONFIG['LEFT_BUZZER']
    port_right_button = PORTS_CONFIG['RIGHT_PUSH_BUTTON']
    port_left_button = PORTS_CONFIG['LEFT_PUSH_BUTTON']
    left_beeper = PWM(Pin(port_left_beeper, Pin.OUT), freq=500, duty_u16=0)
    right_beeper = PWM(Pin(port_right_beeper, Pin.OUT), freq=500, duty_u16=0)
    push_button_left = Pin(port_left_button, Pin.IN)
    push_button_right = Pin(port_right_button, Pin.IN)
    left_group = [push_button_left, left_beeper]
    right_group = [push_button_right, right_beeper]
    possible_choices = [left_group, right_group]

    for i in range(0, 5):
        choice_group = choice(possible_choices)
        another_beeper = left_group if choice_group == right_group else right_group
        sleep(randint(3, 7))

        count = start_time = utime.ticks_ms()
        choice_group[1].duty_u16(50)

        while True:
            success_state = choice_group[0].value()
            error_state = another_beeper[0].value()

            if success_state:
                end_time = utime.ticks_ms()
                choice_group[1].duty_u16(0)

                break
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                choice_group[1].duty_u16(0)

                break

    left_beeper.deinit()
    right_beeper.deinit()
    print('Familiarização finalizada com sucesso!')


def auditory_simple_familiarization():
    print('Familiarização iniciada!')

    with open('config/ports_config.json', 'r') as f:
        PORTS_CONFIG = json.load(f)

    with open('config/session_config.json', 'r') as f:
        SESSION_CONFIG = json.load(f)

    port_beeper = PORTS_CONFIG['RIGHT_BUZZER'] if SESSION_CONFIG['DOMINANT_HAND'] == 'D' else PORTS_CONFIG['LEFT_BUZZER']
    port_push_button = PORTS_CONFIG['RIGHT_PUSH_BUTTON'] if SESSION_CONFIG['DOMINANT_HAND'] == 'D' else PORTS_CONFIG['LEFT_PUSH_BUTTON']
    beeper = PWM(Pin(port_beeper, Pin.OUT), freq=500, duty_u16=0)
    push_button = Pin(port_push_button, Pin.IN)

    for _ in range(0, 3):
        sleep(randint(3, 7))

        count = utime.ticks_ms()
        beeper.duty_u16(50)

        while True:
            success_state = push_button.value()

            if success_state:
                beeper.duty_u16(0)

                break
            elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                beeper.duty_u16(0)

                break

    beeper.deinit()
    print('Familiarização finalizada com sucesso!')
