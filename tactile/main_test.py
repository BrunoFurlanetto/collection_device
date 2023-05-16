from machine import Pin
from time import sleep
from random import randint, choice
import utime

from utils.utils import reaction_time, save_data


def tactile_choice_test():
    left = Pin(18, Pin.OUT)
    rigth = Pin(22, Pin.OUT)
    push_button_left = Pin(21, Pin.IN)
    push_button_rigth = Pin(23, Pin.IN)
    left_group = [push_button_left, left]
    right_group = [push_button_rigth, rigth]
    possible_choice = [right_group, left_group]
    results = []

    for i in range(0, 8):
        choice_side = choice(possible_choice)
        another_side = right_group if choice_side == left_group else left_group

        sleep(randint(3, 7))

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
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 1000:
                choice_side[1].value(False)
                results.append(0)

                break

    save_data('tactile_choice_test.dat', results)

    return


def tactile_simple_test():
    rigth = Pin(22, Pin.OUT)
    push_button_rigth = Pin(23, Pin.IN)
    results = []

    for i in range(0, 8):
        sleep(randint(3, 7))
        count = start_time = utime.ticks_ms()
        rigth.value(True)

        while True:
            success_state = push_button_rigth.value()

            if success_state:
                end_time = utime.ticks_ms()
                rigth.value(0)
                results.append(reaction_time(start_time, end_time))

                break
            elif utime.ticks_diff(utime.ticks_ms(), count) > 1000:
                rigth.value(False)
                results.append(0)

                break

    save_data('tactile_simple_test.dat', results)

    return
