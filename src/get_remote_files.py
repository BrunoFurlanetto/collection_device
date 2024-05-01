import subprocess
from datetime import datetime

from time import sleep

stimuli = ['visual', 'auditory', 'tactile']
# from src.get_remote_files import get_test_files
# get_test_files('com5', 'jota', 'jota')


def get_test_files(port, modality_initials):
    """
    Function responsible for taking the files from the microcontroller's memory and saving them in the local repository
    :param port: Communication port with the microcontroller
    :param modality_initials: Initials of the volunteer modality
    :return: The function has no return
    """
    print('Processando os resultados obtidos...')
    sleep(1)
    date = datetime.now().strftime('%Y-%m-%d_%H-%M')

    for stimulus in stimuli:
        try:
            command = f'venv\\Scripts\\ampy -p {port} get {stimulus}_simple_test.dat results\\trs_{stimulus[0:1]}_{modality_initials}_{date}.dat'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f'Arquivo {stimulus}_simple_test.dat não encontrado.')

            subprocess.run(
                f'venv\\Scripts\\ampy -p {port} rm {stimulus}_simple_test.dat',
                capture_output=True,
                text=True,
                shell=True
            )
        except Exception as e:
            print(f'Erro: {e}')

        try:
            command = f'venv\\Scripts\\ampy -p {port} get {stimulus}_choice_test.dat results\\tre_{stimulus[0:1]}_{modality_initials}_{date}.dat'
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode != 0:
                print(f'Aarquivo {stimulus}_choice_test.dat não encontrado.')

            subprocess.run(
                rf'venv\\Scripts\\ampy -p {port} rm {stimulus}_choice_test.dat',
                capture_output=True,
                text=True,
                shell=True
            )
        except Exception as e:
            print(f'Erro: {e}')

    print('Os arquivos resultantes dos testes estão na pasta "results".')
    sleep(10)
