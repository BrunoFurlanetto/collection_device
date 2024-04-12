from random import randint, choice
from time import sleep

import utime


def auditory_choice_familiarization(low_group, high_group, possible_choices):
    print('Familiarização iniciada!')

    for i in range(0, 3):
        choice_group = choice(possible_choices)
        another_beeper = low_group if choice_group == high_group else high_group
        sleep(randint(3, 7))

        count = start_time = utime.ticks_ms()
        choice_group[1].duty_u16(50)

        while True:
            success_state = choice_group[0].value()
            error_state = another_beeper[0].value()

            if success_state:
                end_time = utime.ticks_ms()
                choice_group[1].duty_u16(0)

                break
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                choice_group[1].duty_u16(0)

                break

    print('Familiarização finalizada, aperte enter para iniciar o teste.')
    input('Pessione ENTER para iniciar o teste!')


def auditory_simple_familiarization(beeper, push_button):
    print('Familiarização iniciada!')

    for _ in range(0, 3):
        sleep(randint(3, 7))

        count = utime.ticks_ms()
        beeper.duty_u16(50)

        while True:
            success_state = push_button.value()

            if success_state:
                beeper.duty_u16(0)

                break
            elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                beeper.duty_u16(0)

                break

    print('Familiarização finalizada.')
    input('Pessione ENTER para iniciar o teste!')
