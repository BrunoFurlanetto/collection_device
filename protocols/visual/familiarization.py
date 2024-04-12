from time import sleep
from random import randint, choice
import utime


def visual_choice_familiarization(red_group, green_group, possible_choice):
    print('Familiarizção Iniciada.')

    for i in range(0, 5):
        choice_led = choice(possible_choice)
        another_led = red_group if choice_led == green_group else green_group

        sleep(randint(3, 7))

        count = utime.ticks_ms()
        choice_led[1].value(True)

        while True:
            success_state = choice_led[0].value()
            error_state = another_led[0].value()

            if success_state:
                choice_led[1].value(False)

                break
            elif error_state or utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                choice_led[1].value(False)

                break

    print('Familiarização finalizada, aperte enter para iniciar o teste.')
    input('Pessione ENTER para iniciar o teste!')


def visual_simple_familiarization(green_led, push_button):
    print('Familiarização iniciada!')

    for _ in range(0, 3):
        sleep(randint(3, 7))
        count = utime.ticks_ms()
        green_led.value(True)

        while True:
            success_state = push_button.value()

            if success_state:
                green_led.value(False)

                break
            elif utime.ticks_diff(utime.ticks_ms(), count) > 2000:
                green_led.value(False)

                break

    print('Familiarização finalizada, aperte enter para iniciar o teste.')
    input('Pessione ENTER para iniciar o teste!')
