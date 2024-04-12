import utime
from random import choice, randint
from time import sleep


def tactile_choice_familiarization(right_group, left_group, possible_choice):
    print('Familiarização iniciada!')

    for _ in range(0, 3):
        choice_side = choice(possible_choice)
        another_side = right_group if choice_side == left_group else left_group
        sleep(randint(3, 7))

        count = utime.ticks_ms()
        choice_side[1].value(True)

        while True:
            success_state = choice_side[0].value()
            error_state = another_side[0].value()

            if success_state:
                choice_side[1].value(False)

                break
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                choice_side[1].value(False)

                break

    print('Familiarização finalizada, aperte enter para iniciar o teste.')
    input('Pessione ENTER para iniciar o teste!')


def tactile_simple_familiarization(right, push_button):
    print('Familiarização iniciada!')

    for _ in range(0, 3):
        sleep(randint(3, 7))
        count = utime.ticks_ms()
        right.value(True)

        while True:
            success_state = push_button.value()

            if success_state:
                right.value(0)

                break
            elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                right.value(False)

                break

    print('Familiarização finalizada, aperte enter para iniciar o teste.')
    input('Pessione ENTER para iniciar o teste!')
