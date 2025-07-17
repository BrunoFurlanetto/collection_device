# This file is executed on every boot (including wake-boot from deepsleep)
import json
import sys
import time
from machine import Pin

# LED onboard para sinalizar erro (ajuste o pino se for outro)
_ERROR_LED_PIN = 14


def blink_error(times=3, interval=0.2):
    led = Pin(_ERROR_LED_PIN, Pin.OUT)

    for _ in range(times):
        led.on()
        time.sleep(interval)
        led.off()
        time.sleep(interval)


def reset_ports():
    try:
        with open('config/ports_config.json', 'r', encoding='utf-8') as f:
            ports = json.load(f).values()
    except Exception as e:
        # Problema ao abrir ou decodificar o JSON
        sys.print_exception(e)
        blink_error()
        return

    for port in ports:
        try:
            # Configura pino como saída e força nível baixo
            Pin(port, Pin.OUT, value=0)
        except Exception as e:
            # Se qualquer pino falhar, reporta e pisca LED
            sys.print_exception(e)
            blink_error()


# Executa no boot
reset_ports()
