import json

import uasyncio as asyncio
from machine import Pin, PWM
from time import sleep
from random import randint, choice
import utime

from protocols.auditory.familiarization import auditory_choice_familiarization, auditory_simple_familiarization
from protocols.utils.utils import reaction_time, save_data, anticipation_test


def safe_buzzer_init(port):
    pin = Pin(port, Pin.OUT)
    pin.value(0)
    sleep(0.01)
    pwm = PWM(pin, freq=500, duty_u16=0)
    sleep(0.01)

    return pwm


def safe_buzzer_cleanup(buzzer, port):
    """
    Limpeza segura do buzzer
    """
    buzzer.duty_u16(0)
    sleep(0.01)
    buzzer.deinit()
    Pin(port, Pin.OUT).value(0)


def auditory_choice_test():
    """
    20 stimuli are made with a time interval between them at random, ranging from 3 to 7 seconds. The volunteer must
    then press the button as quickly as possible.
    --------------------------------------------------------------------------------------------------------------------
    Function responsible for the auditory choice reaction time collection protocol. The protocol consists of providing a
    sound stimulus that is directed into the participant's right or left ear through two buzzers inside a headphone. In
    addition to choosing the side, the time between stimuli is also random, to avoid volunteer learning within the
    protocol. At the end, the reaction time and errors, both by choice and omission and by anticipation, are saved in
    a file called 'visual_choice_test.dat'.
    :return: The function has no return at the end
    --------------------------------------------------------------------------------------------------------------------
    The acronyms that are added to the results in case of volunteer error are as follows:
        • DP - Didn't press
        • WS - Wrong side and
        • AT - Anticipated
    """
    with open('config/ports_config.json', 'r') as f:
        PORTS_CONFIG = json.load(f)

    port_right_beeper = PORTS_CONFIG['RIGHT_BUZZER']
    port_left_beeper = PORTS_CONFIG['LEFT_BUZZER']
    port_right_button = PORTS_CONFIG['RIGHT_PUSH_BUTTON']
    port_left_button = PORTS_CONFIG['LEFT_PUSH_BUTTON']
    left_beeper = safe_buzzer_init(port_left_beeper)
    right_beeper = safe_buzzer_init(port_right_beeper)
    push_button_left = Pin(port_left_button, Pin.IN)
    push_button_right = Pin(port_right_button, Pin.IN)
    left_group = [push_button_left, left_beeper]
    right_group = [push_button_right, right_beeper]
    possible_choices = [left_group, right_group]
    results = []
    print('Teste iniciado!')

    for _ in range(0, 20):
        sleep(1)
        choice_group = choice(possible_choices)
        another_beeper = left_group if choice_group == right_group else right_group
        wait_time = randint(2, 6) * 1000
        wait_time_start = utime.ticks_ms()
        anticipated = anticipation_test(wait_time_start, wait_time, push_button_right, push_button_left)

        if not anticipated:
            count = start_time = utime.ticks_ms()
            choice_group[1].duty_u16(50)

            while True:
                success_state = choice_group[0].value()
                error_state = another_beeper[0].value()

                if success_state:
                    end_time = utime.ticks_ms()
                    choice_group[1].duty_u16(0)
                    results.append(reaction_time(start_time, end_time))

                    break
                elif error_state:
                    choice_group[1].duty_u16(0)
                    results.append('WS')

                    break
                elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                    choice_group[1].duty_u16(0)
                    results.append('DP')

                    break
        else:
            results.append('AT')

    save_data('auditory_choice_test.dat', results)
    print('Teste finalizado com sucesso!')
    safe_buzzer_cleanup(left_beeper, port_left_beeper)
    safe_buzzer_cleanup(right_beeper, port_right_beeper)

    return


def auditory_simple_test():
    """
    20 stimuli are made with a time interval between them at random, ranging from 3 to 7 seconds. The volunteer must
    then press the button as quickly as possible.
    -------------------------------------------------- ------------------------------------------------------------
    Function responsible for the collection protocol of the auditory simple reaction time. The protocol consists of
    issuing a sound stimulus for the volunteer to respond as quickly as possible by pressing the designated button.
    At the end, the volunteer's reaction time and errors (by omission) are saved in a file named
    'auditory_simples_test.dat'. Errors are assigned a value of zero.
    :return: The function has no return at the end
    ---------------------------------------------------------------------------------------------------------------
    The acronyms that are added to the results in case of volunteer error are as follows:
        • DP - Didn't press
        • AT - Anticipated
    """
    with open('config/ports_config.json', 'r') as f:
        PORTS_CONFIG = json.load(f)

    with open('config/session_config.json', 'r') as f:
        SESSION_CONFIG = json.load(f)

    port_beeper = PORTS_CONFIG['RIGHT_BUZZER'] if SESSION_CONFIG['DOMINANT_HAND'] == 'D' else PORTS_CONFIG['LEFT_BUZZER']
    port_push_button = PORTS_CONFIG['RIGHT_PUSH_BUTTON'] if SESSION_CONFIG['DOMINANT_HAND'] == 'D' else PORTS_CONFIG['LEFT_PUSH_BUTTON']
    beeper = safe_buzzer_init(port_beeper)
    push_button = Pin(port_push_button, Pin.IN)
    results = []
    print('Teste iniciado!')

    for _ in range(0, 20):
        sleep(1)
        wait_time = randint(2, 6) * 1000
        wait_time_start = utime.ticks_ms()
        anticipated = anticipation_test(wait_time_start, wait_time, push_button)

        if not anticipated:
            count = start_time = utime.ticks_ms()
            beeper.duty_u16(50)

            while True:
                success_state = push_button.value()

                if success_state:
                    end_time = utime.ticks_ms()
                    beeper.duty_u16(0)
                    results.append(reaction_time(start_time, end_time))

                    break
                elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                    beeper.duty_u16(0)
                    results.append('DP')

                    break
        else:
            results.append('AT')

    save_data('auditory_simple_test.dat', results)
    safe_buzzer_cleanup(beeper, port_beeper)
    print('Teste finalizado com sucesso!')

    return
