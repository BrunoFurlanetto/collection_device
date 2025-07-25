import json
import subprocess
from datetime import datetime

from time import sleep

from src.interface.gui.temp_messages import TempAlert

stimuli = ['visual', 'auditory', 'tactile']
# from src.get_remote_files import get_test_files
# get_test_files('com5', 'jota', 'jota')


def get_test_files(master):
    """
    Function responsible for taking the files from the microcontroller's memory and saving them in the local repository
    :return: The function has no return
    """
    with open('src/config/session_config.json', 'r') as f:
        SESSION_CONFIG = json.load(f)

    # TempAlert(master, 'Processando os resultados obtidos...')
    date = datetime.now().strftime('%Y-%m-%d_%H-%M')
    port = SESSION_CONFIG['PORT']
    tests_not_found = []
    participant_code = SESSION_CONFIG['PARTICIPANT_CODE'].lower()

    for stimulus in stimuli:
        print(stimulus)
        try:
            command = f'venv\\Scripts\\ampy -p {port} get {stimulus}_simple_test.dat results\\trs_{stimulus[0:1]}_{participant_code}_{date}.dat'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                tests_not_found.append(f'{stimulus} simples')

            subprocess.run(
                f'venv\\Scripts\\ampy -p {port} rm {stimulus}_simple_test.dat',
                capture_output=True,
                text=True,
                shell=True
            )
        except Exception as e:
            TempAlert(master, f'Erro: {e}')

        try:
            command = f'venv\\Scripts\\ampy -p {port} get {stimulus}_choice_test.dat results\\tre_{stimulus[0:1]}_{participant_code}_{date}.dat'
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode != 0:
                tests_not_found.append(f'{stimulus} escolha.')

            subprocess.run(
                rf'venv\\Scripts\\ampy -p {port} rm {stimulus}_choice_test.dat',
                capture_output=True,
                text=True,
                shell=True
            )
        except Exception as e:
            TempAlert(master, f'Erro: {e}')

    TempAlert(master, 'Os arquivos resultantes dos testes estão na pasta "results".', duration=2000)
    sleep(2)
    TempAlert(master, f'Arquivos dos seguintes testes não foram encontrados: {", ".join(tests_not_found)}.', duration=5000)
    sleep(5)

    return
