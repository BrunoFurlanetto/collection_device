from machine import Pin, PWM
from time import sleep
from random import randint, choice
import utime

from utils.utils import reaction_time, save_data


def auditory_choice_test():
    low_frequency = 330
    high_frequency = 990
    beeper = PWM(Pin(19, Pin.OUT), duty=0)
    push_button_low = Pin(21, Pin.IN)
    push_button_high = Pin(23, Pin.IN)
    low_group = [push_button_low, low_frequency]
    high_group = [push_button_high, high_frequency]
    results = []

    for i in range(0, 8):
        choice_group = choice([low_group, high_group])
        beeper.freq(choice_group[1])
        sleep(randint(3, 7))
        start_time = utime.ticks_ms()
        beeper.duty(512)

        while True:
            logic_state = choice_group[0].value()

            if logic_state:
                end_time = utime.ticks_ms()
                beeper.duty(0)
                results.append(reaction_time(start_time, end_time))
                break

    save_data('auditory_choice_test.dat', results)

    return
