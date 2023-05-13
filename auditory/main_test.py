from machine import Pin, PWM
from time import sleep
from random import randint, choice
import utime

from utils.utils import reaction_time, save_data


def auditory_choice_test():
    low_frequency = 330
    high_frequency = 1320
    beeper = PWM(Pin(19, Pin.OUT), duty=0)
    push_button_low = Pin(21, Pin.IN)
    push_button_high = Pin(23, Pin.IN)
    low_group = [push_button_low, low_frequency]
    high_group = [push_button_high, high_frequency]
    possible_choices = [low_group, high_group]
    results = []

    for i in range(0, 8):
        choice_group = choice(possible_choices)
        another_led = low_group if choice_group == high_group else high_group
        beeper.freq(choice_group[1])
        sleep(randint(3, 7))

        count = start_time = utime.ticks_ms()
        beeper.duty(512)

        while True:
            success_state = choice_group[0].value()
            error_state = another_led[0].value()

            if success_state:
                end_time = utime.ticks_ms()
                beeper.duty(0)
                results.append(reaction_time(start_time, end_time))

                break
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 1000:
                beeper.duty(0)
                results.append(0)

                break

    save_data('auditory_choice_test.dat', results)

    return


def auditory_simple_test():
    high_frequency = 1320
    beeper = PWM(Pin(19, Pin.OUT), duty=0)
    push_button_high = Pin(23, Pin.IN)
    results = []

    for i in range(0, 8):
        beeper.freq(high_frequency)
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

    return
