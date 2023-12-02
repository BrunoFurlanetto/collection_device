import subprocess

from time import sleep

stimuli = ['visual', 'auditory', 'tactile']


def get_test_files(port, name):
    """
    Function responsible for taking the files from the microcontroller's memory and saving them in the local repository
    :param port: Communication port with the microcontroller
    :param name: Name of the volunteer to be in the filename
    :return: The function has no return
    """
    print('Processando os resultados obtidos...')
    sleep(1)
    for stimulus in stimuli:
        try:
            command = f'venv\\Scripts\\ampy -p {port} get {stimulus}_simple_test.dat ..\\results\\{stimulus}_simple_test_{name}.dat'
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f'Arquivo {stimulus}_simple_test.dat não encontrado.')
            else:
                subprocess.run(
                    f'venv\\Scripts\\ampy -p {port} rm {stimulus}_simple_test.dat',
                    capture_output=True,
                    text=True,
                    shell=True
                )
        except Exception as e:
            print(f'Erro: {e}')

        try:
            command = f'venv\\Scripts\\ampy -p {port} get {stimulus}_choice_test.dat ..\\results\\{stimulus}_choice_test_{name}.dat'
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode != 0:
                print(f'Aarquivo {stimulus}_choice_test.dat não encontrado.')
            else:
                subprocess.run(
                    f'ampy -p {port} rm {stimulus}_choice_test.dat',
                    capture_output=True,
                    text=True,
                    shell=True
                )
        except Exception as e:
            print(f'Erro: {e}')

    print('Os arquivos resultantes dos testes estão na pasta "results".')
    sleep(10)
