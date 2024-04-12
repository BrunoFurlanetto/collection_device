from machine import Pin
from time import sleep
from random import randint, choice
import utime

from protocols.utils.utils import reaction_time, save_data, anticipation_test
from protocols.tactile.familiarization import tactile_choice_familiarization, tactile_simple_familiarization


def tactile_choice_test():
    """
    20 stimuli are made at random, both in the time between stimuli and on the side of the stimuli. The volunteer must
    press the designated button as quickly as possible.
    --------------------------------------------------------------------------------------------------------------------
    Function responsible for the tactile choice reaction time collection protocol. The protocol consists of providing a
    tactile stimulus by vibrating the joysctick that will be in the volunteer's right or left hand randomly. In addition
    to the choice of the side that will vibrate, the time between stimuli is also random, this to avoid the volunteer's
    learning within the protocol. At the end the reaction time and the errors, both by choice and by omission are saved
    in a file named 'tactile_choice_test.dat'. Errors are assigned a value of zero in the output file.
    :return: The function has no return at the end
    --------------------------------------------------------------------------------------------------------------------
    The acronyms that are added to the results in case of volunteer error are as follows:
        • DP - Didn't press
        • WS - Wrong side and
        • AT - Anticipated
    """
    left = Pin(33, Pin.OUT)
    right = Pin(5, Pin.OUT)
    push_button_left = Pin(12, Pin.IN)
    push_button_right = Pin(19, Pin.IN)
    left_group = [push_button_left, left]
    right_group = [push_button_right, right]
    possible_choice = [right_group, left_group]
    results = []
    tactile_choice_familiarization(left_group, right_group, possible_choice)
    print('Teste iniciado!')

    for _ in range(0, 20):
        sleep(1)
        choice_side = choice(possible_choice)
        another_side = right_group if choice_side == left_group else left_group
        wait_time = randint(2, 6) * 1000
        wait_time_start = utime.ticks_ms()
        anticipated = anticipation_test(wait_time_start, wait_time, push_button_right, push_button_left)

        if not anticipated:
            count = start_time = utime.ticks_ms()
            choice_side[1].value(True)

            while True:
                success_state = choice_side[0].value()
                error_state = another_side[0].value()

                if success_state:
                    end_time = utime.ticks_ms()
                    choice_side[1].value(False)
                    results.append(reaction_time(start_time, end_time))

                    break
                elif error_state:
                    choice_side[1].value(False)
                    results.append('WS')

                    break
                elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                    results.append('DP')
        else:
            results.append('AT')

    save_data('tactile_choice_test.dat', results)

    return


def tactile_simple_test():
    """
    20 stimuli are made randomly in the time between stimuli. The volunteer is expected to press the designated
    button as quickly as possible.
    -----------------------------------------------------------------------------------------------------------
    Function responsible for the simple tactile reaction time collection protocol. The protocol consists of
    providing a tactile stimulus by vibrating the joysctick that will be in the volunteer's dominant hand. The
    time between stimuli is randomly given from 3 to 7 seconds, this to avoid the volunteer learning within the
    protocol. At the end the reaction time and the error (by omission) are saved in a file named
    'tactile_simple_test.dat'. Errors are assigned a value of zero in the output file.
    :return: The function has no return at the end
    --------------------------------------------------------------------------------------------------------------------
    The acronyms that are added to the results in case of volunteer error are as follows:
        • DP - Didn't press
        • AT - Anticipated
    """
    right = Pin(5, Pin.OUT)
    push_button_right = Pin(19, Pin.IN)
    results = []
    tactile_simple_familiarization(right, push_button_right)
    print('Teste iniciado!')

    for _ in range(0, 20):
        sleep(1)
        wait_time = randint(2, 6) * 1000
        wait_time_start = utime.ticks_ms()
        anticipated = anticipation_test(wait_time_start, wait_time, push_button_right)

        if not anticipated:
            count = start_time = utime.ticks_ms()
            right.value(True)

            while True:
                success_state = push_button_right.value()

                if success_state:
                    end_time = utime.ticks_ms()
                    right.value(0)
                    results.append(reaction_time(start_time, end_time))

                    break
                elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                    right.value(False)
                    results.append('DP')

                    break
        else:
            results.append('AT')

    save_data('tactile_simple_test.dat', results)

    return
