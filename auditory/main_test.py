from machine import Pin, PWM
from time import sleep
from random import randint, choice
import utime

from utils.utils import reaction_time, save_data


def auditory_choice_test():
    """
    8 stimuli are made at random, both in the time between stimuli and in the frequency of the stimuli, and the
    volunteer must press the designated button as quickly as possible.
    -----------------------------------------------------------------------------------------------------------
    Function responsible for the auditory choice reaction time collection protocol. The protocol consists of
    choosing two distinct frequencies, so that the volunteer can distinguish both and make the right choice when
    the stimulus occurs. At the end, the reaction time and errors, both by choice and by omission, are saved in
    a file named 'auditory_choice_test.dat'. Errors are assigned a value of zero.
    :return: The function has no return at the end
    """
    low_beeper = PWM(Pin(32, Pin.OUT), duty=0, freq=330)
    high_beeper = PWM(Pin(19, Pin.OUT), duty=0, freq=1320)
    push_button_low = Pin(12, Pin.IN)
    push_button_high = Pin(21, Pin.IN)
    low_group = [push_button_low, low_beeper]
    high_group = [push_button_high, high_beeper]
    possible_choices = [low_group, high_group]
    results = []

    for i in range(0, 8):
        choice_group = choice(possible_choices)
        another_beeper = low_group if choice_group == high_group else high_group
        sleep(randint(3, 7))

        count = start_time = utime.ticks_ms()
        choice_group[1].duty(512)

        while True:
            success_state = choice_group[0].value()
            error_state = another_beeper[0].value()

            if success_state:
                end_time = utime.ticks_ms()
                choice_group[1].duty(0)
                results.append(reaction_time(start_time, end_time))

                break
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                choice_group[1].duty(0)
                results.append(0)

                break

    save_data('auditory_choice_test.dat', results)
    low_beeper.deinit()
    high_beeper.deinit()

    return


def auditory_simple_test():
    """
    8 stimuli are made with a time interval between them at random, ranging from 3 to 7 seconds. The volunteer must
    then press the button as quickly as possible.
    -------------------------------------------------- ------------------------------------------------------------
    Function responsible for the collection protocol of the auditory simple reaction time. The protocol consists of
    issuing a sound stimulus for the volunteer to respond as quickly as possible by pressing the designated button.
    At the end, the volunteer's reaction time and errors (by omission) are saved in a file named
    'auditory_simples_test.dat'. Errors are assigned a value of zero.
    :return: The function has no return at the end
    """
    beeper = PWM(Pin(19, Pin.OUT), duty=0, freq=1320)
    push_button_high = Pin(21, Pin.IN)
    results = []

    for i in range(0, 8):
        sleep(randint(3, 7))

        count = start_time = utime.ticks_ms()
        beeper.duty(512)

        while True:
            success_state = push_button_high.value()

            if success_state:
                end_time = utime.ticks_ms()
                beeper.duty(0)
                results.append(reaction_time(start_time, end_time))

                break
            elif utime.ticks_diff(utime.ticks_ms(), count) > 1000:
                beeper.duty(0)
                results.append(0)

                break

    save_data('auditory_simple_test.dat', results)
    beeper.deinit()

    return
