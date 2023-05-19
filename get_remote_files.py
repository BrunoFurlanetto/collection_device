import locale
import subprocess


linguage = locale.getlocale()[0]
stimuli = ['visual', 'auditory', 'tactile']


def get_test_files(port, name):
    """
    Function responsible for taking the files from the microcontroller's memory and saving them in the local repository
    :param port: Communication port with the microcontroller
    :param name: Name of the volunteer to be in the filename
    :return: The function has no return
    """
    for stimulus in stimuli:
        try:
            result = subprocess.run(
                ['ampy', '--port', port, 'get', f'{stimulus}_simple_test.dat', f'{stimulus}_simples_test_{name}.dat',
                 f'ampy --port {port} rm {stimulus}_simple_test.dat'],
                capture_output=True, text=True)

            if result.returncode != 0:
                if linguage == 'pt_BR':
                    print(f'Arquivo {stimulus}_simple_test.dat não encontrado.')
                else:
                    print(f'File {stimulus}_simple_test.dat not found.')
        except Exception as e:
            if linguage == 'pt_BR':
                print(f'Erro: {e}')
            else:
                print(f'Error: {e}')

        try:
            result = subprocess.run(
                ['ampy', '--port', port, 'get', f'{stimulus}_choice_test.dat', f'{stimulus}_choice_test_{name}.dat',
                 f'ampy --port {port} rm {stimulus}_choice_test.dat'],
                capture_output=True, text=True)

            if result.returncode != 0:
                if linguage == 'pt_BR':
                    print(f'Aarquivo {stimulus}_choice_test.dat não encontrado.')
                else:
                    print(f'File {stimulus}_choice_test.dat not find.')
        except Exception as e:
            if linguage == 'pt_BR':
                print(f'Erro: {e}')
            else:
                print(f'Error: {e}')
