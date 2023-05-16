from utime import ticks_diff


def reaction_time(start_time, end_time):
    return ticks_diff(end_time, start_time) / 1000


def save_data(filename, data):
    with open(filename, 'w+') as f:
        # Escrever cada valor em uma linha separada
        for index, value in enumerate(data, start=1):
            f.write(f'{index}   {value}\n')


# def get_file(filename):
#     def get_file_from_esp32(file_name):
#         command = f'ampy --port COM5 get {file_name} {file_name}'
#         os.system(command)
