import subprocess

from ampy.pyboard import PyboardError

stimuli = ['visual', 'auditory', 'tactile']


def get_test_files(port, name):
    for stimulus in stimuli:
        try:
            result = subprocess.run(
                ['ampy', '--port', port, 'get', f'{stimulus}_simple_test.dat', f'{stimulus}_choice_test_{name}.dat',
                 f'ampy --port {port} rm {stimulus}_simple_test.dat'],
                capture_output=True, text=True)

            if result.returncode != 0:
                print(f'Arquivo {stimulus}_simple_test.dat não encontrado.')
        except Exception as e:
            print(f'Erro: {e}')

        try:
            result = subprocess.run(
                ['ampy', '--port', port, 'get', f'{stimulus}_choice_test.dat', f'{stimulus}_choice_test_{name}.dat',
                 f'ampy --port {port} rm {stimulus}_choice_test.dat'],
                capture_output=True, text=True)

            if result.returncode != 0:
                print(f'Aarquivo {stimulus}_choice_test.dat não encontrado.')
        except Exception as e:
            print(f'Erro: {e}')
