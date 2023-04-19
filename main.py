from machine import Pin
from time import sleep
from random import randint, choice

red_led = Pin(4, Pin.OUT)
green_led = Pin(2, Pin.OUT)

push_button_red = Pin(13, Pin.IN)
push_button_green = Pin(12, Pin.IN)

red_group = [push_button_red, red_led]
green_group = [push_button_green, green_led]


while True:
    choice_led = choice([red_group, green_group])
    sleep(randint(3, 7))
    choice_led[1].value(1)

    while True:
        logic_state = choice_led[0].value()

        if logic_state:
            choice_led[1].value(0)
            break
