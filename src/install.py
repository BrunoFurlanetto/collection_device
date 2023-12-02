import subprocess
from datetime import datetime

import os
from time import sleep


def init_install(port):
    def run_command(command):
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            errors.append(e)

    errors = []
    create_venv_cmd = "python -m venv venv"
    activate_venv_cmd = f'venv\\Scripts\\activate'
    install_requirements_cmd = f'venv\\Scripts\\pip install -r ..\\requirements.txt'
    erase_flash_cmd = f'venv\\Scripts\\esptool.py --chip esp32 --port {port} erase_flash'
    write_flash_cmd = f'venv\\Scripts\\esptool.py --chip esp32 --port {port} --baud 115200 write_flash -z 0x1000 config\\esp32.bin'
    commands = [create_venv_cmd, activate_venv_cmd, install_requirements_cmd, erase_flash_cmd, write_flash_cmd]

    for command in commands:
        run_command(command)
        sleep(1)

    if len(errors) > 0:
        with open('log.txt', 'w') as file:
            for error in errors:
                file.write(f'{error}: {datetime.now()} \n')

        return f'Erro: instalação não concluída, consultar log.txt', errors
    else:
        try:
            os.remove('log.txt')
        except FileNotFoundError:
            ...
        finally:
            return 'Instalação concluída com sucesso', errors


def send_protocols_to_esp(port):
    list_directories = os.listdir('..\\protocols')
    print('Reiniciando o dispositivo...')
    subprocess.run(f'venv\\Scripts\\ampy -p {port} reset', shell=True)
    errors = []
    print('Reinicialização completada com sucesso.')
    print('Enviando protocolos para o dispositivo...')

    for directory in list_directories:
        try:
            subprocess.run(f'venv\\Scripts\\ampy -p {port} put ..\\protocols\\{directory}', shell=True)
        except subprocess.SubprocessError as e:
            with open('log.txt', 'w+') as file:
                file.write(f'{e}: {datetime.now()}\n')

            print(f'{directory} não enviado para o dispositivo, verificar log.txt')
            errors.append(e)

            break

    return errors


def main():
    port = input('Qual a porta de comunicação com o dispositivo? ').strip().upper()
    msg, list_errors = init_install(port)
    send_list_errors = []
    sleep(10) if len(list_errors) > 0 else print(msg)

    if len(list_errors) == 0:
        send_list_errors = send_protocols_to_esp(port)

    if len(send_list_errors) == 0:
        print('Instalação completada sem erros')
    else:
        print('Instalação completada parcialmente, verificar o dispositivo e o arquivo log.txt')

    sleep(10)


if __name__ == '__main__':
    main()
