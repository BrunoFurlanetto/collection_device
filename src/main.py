from get_remote_files import get_test_files

import os
import subprocess
from time import sleep


def connect_esp(port):
    print('Conectando com o microcontrolador...')
    sleep(1)
    print('Ao entrar, pressione "ctrl + B" e execute execfile("protocols/initial/initialization.py") para dar início ao protocolo de coleta')
    sleep(1)
    python_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\\venv\\Scripts\\python')

    try:
        subprocess.call(f'{python_path} -m serial.tools.miniterm {port} 115200')
    except Exception as e:
        print(f'Erro {e}, na conexão com o microcontrolador')


def main():
    port = input('Insira a porta de comunicação com o ESP32: ')
    connect_esp(port)

    name = input('Digite o nome do voluntário: ').strip().replace(' ', '_')
    get_test_files(port, name.lower().replace(' ', '_'))


if __name__ == "__main__":
    main()
