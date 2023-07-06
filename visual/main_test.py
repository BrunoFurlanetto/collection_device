from machine import Pin
from time import sleep
from random import randint, choice
import utime

from utils.utils import reaction_time, save_data


def visual_choice_test():
    """
    8 stimuli are made at random, both in the time between stimuli and in the color of the stimuli. The volunteer must
    press the designated button as quickly as possible.
    --------------------------------------------------------------------------------------------------------------------
    Function responsible for the visual choice reaction time collection protocol. The protocol consists of providing a
    visual stimulus by randomly lighting a red or green LED. In addition to choosing the color of the LED, the time
    between stimuli is also random, this to avoid the volunteer's learning within the protocol. At the end, the reaction
    time and the errors, both by choice and by omission, are saved in a file named 'visual_choice_test.dat'. Errors are
    assigned a value of zero in the output file.
    :return: The function has no return at the end
    """
    red_led = Pin(14, Pin.OUT)
    green_led = Pin(4, Pin.OUT)
    push_button_red = Pin(12, Pin.IN)
    push_button_green = Pin(21, Pin.IN)
    red_group = [push_button_red, red_led]
    green_group = [push_button_green, green_led]
    possible_choice = [red_group, green_group]
    results = []

    for i in range(0, 8):
        choice_led = choice(possible_choice)
        another_led = red_group if choice_led == green_group else green_group

        sleep(randint(3, 7))

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
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                choice_led[1].value(False)
                results.append(0)

                break

    save_data('visual_choice_test.dat', results)

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
    """
    green_led = Pin(4, Pin.OUT)
    push_button_green = Pin(21, Pin.IN)
    results = []

    for i in range(0, 8):
        sleep(randint(3, 7))
        count = start_time = utime.ticks_ms()
        green_led.value(True)

        while True:
            success_state = push_button_green.value()

            if success_state:
                end_time = utime.ticks_ms()
                green_led.value(False)
                results.append(reaction_time(start_time, end_time))

                break
            elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                green_led.value(False)
                results.append(0)

                break

    save_data('visual_simple_test.dat', results)

    return
