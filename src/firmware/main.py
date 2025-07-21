import uos
import machine
import time

# Desanexa o REPL da UART0
uos.dupterm(None, 0)

# Inicializa UART0 nos pinos padrão
uart = machine.UART(0, baudrate=115200)
time.sleep(2)
print("ECHO TEST: pronto para ecoar tudo que chegar pela serial.")

while True:
    line = uart.readline()      # lê até '\n' ou timeout
    if line:                     # só entra se realmente chegou algo
        # opcional, ecoa um prefixo pra ficar óbvio
        uart.write(b"ECHO: ")
        uart.write(line)        # escreve de volta o que leu
