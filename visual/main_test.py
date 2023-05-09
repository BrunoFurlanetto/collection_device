from machine import Pin
from time import sleep
from random import randint, choice
import utime

from utils.utils import reaction_time, save_data


def main_visual_test():
    results = []

    red_led = Pin(2, Pin.OUT)
    green_led = Pin(4, Pin.OUT)

    push_button_red = Pin(21, Pin.IN)
    push_button_green = Pin(23, Pin.IN)

    red_group = [push_button_red, red_led]
    green_group = [push_button_green, green_led]

    for i in range(0, 8):
        choice_led = choice([red_group, green_group])
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

    save_data('visual_test.dat', results)

    return
