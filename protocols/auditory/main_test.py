import uasyncio as asyncio
from machine import Pin, PWM
from time import sleep
from random import randint, choice
import utime

from protocols.auditory.familiarization import auditory_choice_familiarization, auditory_simple_familiarization
from protocols.utils.utils import reaction_time, save_data, anticipation_test


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
    low_beeper = PWM(Pin(32, Pin.OUT), freq=500, duty_u16=0)
    high_beeper = PWM(Pin(18, Pin.OUT), freq=500, duty_u16=0)
    push_button_low = Pin(12, Pin.IN)
    push_button_high = Pin(19, Pin.IN)
    low_group = [push_button_low, low_beeper]
    high_group = [push_button_high, high_beeper]
    possible_choices = [low_group, high_group]
    results = []
    auditory_choice_familiarization(low_group, high_group, possible_choices)
    print('Teste iniciado!')

    for _ in range(0, 20):
        sleep(1)
        choice_group = choice(possible_choices)
        another_beeper = low_group if choice_group == high_group else high_group
        wait_time = randint(2, 6) * 1000
        wait_time_start = utime.ticks_ms()
        anticipated = anticipation_test(wait_time_start, wait_time, push_button_high, push_button_low)

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
    low_beeper.deinit()
    high_beeper.deinit()


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
    beeper = PWM(Pin(18, Pin.OUT), freq=500, duty_u16=0)
    push_button_high = Pin(19, Pin.IN)
    results = []
    auditory_simple_familiarization(beeper, push_button_high)
    print('Teste iniciado!')

    for _ in range(0, 20):
        sleep(1)
        wait_time = randint(2, 6) * 1000
        wait_time_start = utime.ticks_ms()
        anticipated = anticipation_test(wait_time_start, wait_time, push_button_high)

        if not anticipated:
            count = start_time = utime.ticks_ms()
            beeper.duty_u16(50)

            while True:
                success_state = push_button_high.value()

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
    beeper.deinit()

    return
