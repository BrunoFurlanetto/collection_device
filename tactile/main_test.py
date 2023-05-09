from machine import Pin
from time import sleep
from random import randint, choice
import utime

from utils.utils import reaction_time, save_data


def main_tactile_test():
    results = []

    left = Pin(18, Pin.OUT)
    rigth = Pin(22, Pin.OUT)

    push_button_left = Pin(21, Pin.IN)
    push_button_rigth = Pin(23, Pin.IN)

    lef_group = [push_button_left, left]
    right_group = [push_button_rigth, rigth]

    for i in range(0, 8):
        choice_led = choice([lef_group, right_group])
        sleep(randint(3, 7))
        start_time = utime.ticks_ms()
        choice_led[1].value(1)

        while True:
            logic_state = choice_led[0].value()

            if logic_state:
                end_time = utime.ticks_ms()
                choice_led[1].value(0)
                results.append(reaction_time(start_time, end_time))

                break

    save_data('tactile_test.dat', results)

    return
