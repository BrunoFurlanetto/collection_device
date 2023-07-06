import locale
import subprocess
from time import sleep

from get_remote_files import get_test_files

linguage = locale.getlocale()[0]

if linguage == 'pt_BR':
    port = input('Insira a porta de comunicação com o ESP32: ')

    while True:
        print('Conectando com o microcontrolador...')
        sleep(2)
        print('Ao entrar, pressione ctrl + B e execute execfile("/initial/initialization.py") para dar inicio ao protocolo de coleta')
        sleep(2)

        try:
            subprocess.call(f'python -m serial.tools.miniterm {port} 115200')

            break
        except Exception as e:
            print(f'Erro {e}, na conexão com o microcontrolador')

    name = input('Digite o nome do voluntário: ').strip().replace(' ', '_')
else:
    port = input('Enter the communication port with ESP32:')

    while True:
        print('Connecting with the microcontroller...')
        sleep(2)
        print(
            'Upon entering, press ctrl + B and execute execfile("/initial/initialization.py") to start the collection protocol')
        sleep(2)

        try:
            subprocess.call(f'python -m serial.tools.miniterm {port} 115200')

            break
        except Exception as e:
            if linguage == 'pt_BR':
                print(f'Erro {e}, na conexão com o microcontrolador')
            else:
                print(f'Error {e}, when connecting to the microcontroller')

    name = input('Enter the name of the volunteer:').strip().replace(' ', '_')

get_test_files(port, name.lower().replace(' ', '_'))
