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
    print('Processando os resultados obtidos...') if linguage == 'pt_BR' else print('Processing the results obtained...')

    for stimulus in stimuli:
        try:
            result = subprocess.run(
                ['ampy', '--port', port, 'get', f'{stimulus}_simple_test.dat',
                 f'results/{stimulus}_simple_test_{name}.dat'],
                capture_output=True, text=True
            )

            if result.returncode != 0:
                if linguage == 'pt_BR':
                    print(f'Arquivo {stimulus}_simple_test.dat não encontrado.')
                else:
                    print(f'File {stimulus}_simple_test.dat not found.')
            else:
                result = subprocess.run(
                    ['ampy', '--port', port, 'rm', f'{stimulus}_simple_test.dat'],
                    capture_output=True, text=True
                )
        except Exception as e:
            if linguage == 'pt_BR':
                print(f'Erro: {e}')
            else:
                print(f'Error: {e}')

        try:
            result = subprocess.run(
                ['ampy', '--port', port, 'get', f'{stimulus}_choice_test.dat',
                 f'results/{stimulus}_choice_test_{name}.dat'],
                capture_output=True, text=True
            )

            if result.returncode != 0:
                if linguage == 'pt_BR':
                    print(f'Aarquivo {stimulus}_choice_test.dat não encontrado.')
                else:
                    print(f'File {stimulus}_choice_test.dat not find.')
            else:
                result = subprocess.run(
                    ['ampy', '--port', port, 'rm', f'{stimulus}_choice_test.dat'],
                    capture_output=True, text=True
                )
        except Exception as e:
            if linguage == 'pt_BR':
                print(f'Erro: {e}')
            else:
                print(f'Error: {e}')

    if linguage == 'pt_BR':
        print('Os arquivos resultantes dos testes estão na pasta "results".')
    else:
        print('The files resulting from the tests are in the "results" folder.')
