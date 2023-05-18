import subprocess

from time import sleep

from get_remote_files import get_test_files

port = input('Insura a porta de comunicação com o ESP32: ')

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

get_test_files(port, name)
