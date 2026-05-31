import json

from machine import Pin
from time import sleep
from random import randint, choice
import utime

from protocols.utils.utils import reaction_time, save_data, anticipation_test
from protocols.visual.familiarization import visual_choice_familiarization, visual_simple_familiarization


def visual_choice_test():
    """
    20 stimuli are made at random, both in the time between stimuli and in the color of the stimuli. The volunteer must
    press the designated button as quickly as possible.
    --------------------------------------------------------------------------------------------------------------------
    Function responsible for the visual choice reaction time collection protocol. The protocol consists of providing a
    visual stimulus by randomly lighting a red or green LED. In addition to choosing the color of the LED, the time
    between stimuli is also random, this to avoid the volunteer's learning within the protocol. At the end, the reaction
    time and the errors, both by choice and by omission, are saved in a file named 'visual_choice_test.dat'. Errors are
    assigned a value of zero in the output file.
    :return: The function has no return at the end
    --------------------------------------------------------------------------------------------------------------------
    The acronyms that are added to the results in case of volunteer error are as follows:
        • DP - Didn't press
        • WS - Wrong side and
        • AT - Anticipated
    """
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
    results = []
    print('Teste iniciado!')

    for _ in range(0, 20):
        sleep(1)
        choice_led = choice(possible_choice)
        another_led = right_group if choice_led == left_group else left_group
        wait_time = randint(2, 6) * 1000
        wait_time_start = utime.ticks_ms()
        anticipated = anticipation_test(wait_time_start, wait_time, push_button_right, push_button_left)

        if not anticipated:
            start_time = count = utime.ticks_ms()
            choice_led[1].value(True)

            while True:
                success_state = choice_led[0].value()
                error_state = another_led[0].value()

                if success_state:
                    end_time = utime.ticks_ms()
                    choice_led[1].value(False)
                    results.append(reaction_time(start_time, end_time))

                    break
                elif error_state:
                    choice_led[1].value(False)
                    results.append('WS')

                    break
                elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                    choice_led[1].value(False)
                    results.append('DP')

                    break
        else:
            results.append('AT')

    save_data('visual_choice_test.dat', results)
    print('Teste finalizado com sucesso!')

    return


def visual_simple_test():
    """
    8 stimuli are made randomly in the time between stimuli. The volunteer is expected to press the designated button as
    quickly as possible.
    --------------------------------------------------------------------------------------------------------------------
    Function responsible for the simple visual reaction time collection protocol. The protocol consists of providing a
    visual stimulus by lighting a green LED. The time between stimuli is randomly given from 3 to 7 seconds, this to
    avoid the volunteer learning within the protocol. At the end the reaction time and the error (by omission) are
    saved in a file named 'visual_simple_test.dat'. Errors are assigned a value of zero in the output file.
    :return: The function has no return at the end
    --------------------------------------------------------------------------------------------------------------------
    The acronyms that are added to the results in case of volunteer error are as follows:
        • DP - Didn't press
        • AT - Anticipated
    """
    with open('config/ports_config.json', 'r') as f:
        PORTS_CONFIG = json.load(f)

    with open('config/session_config.json', 'r') as f:
        SESSION_CONFIG = json.load(f)

    port_led = PORTS_CONFIG['LEFT_LED']
    port_push_button = PORTS_CONFIG['RIGHT_PUSH_BUTTON'] if SESSION_CONFIG['DOMINANT_HAND'] == 'D' else PORTS_CONFIG['LEFT_PUSH_BUTTON']
    led = Pin(port_led, Pin.OUT)  # TODO: Change after board replacement to port 14
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
            led.value(True)

            while True:
                success_state = push_button.value()

                if success_state:
                    end_time = utime.ticks_ms()
                    led.value(False)
                    results.append(reaction_time(start_time, end_time))

                    break
                elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                    led.value(False)
                    results.append('DP')

                    break
        else:
            results.append('AT')

    save_data('visual_simple_test.dat', results)
    print('Teste finalizado com sucesso!')

    return
