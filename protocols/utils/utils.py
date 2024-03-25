from utime import ticks_diff, ticks_ms


def reaction_time(start_time, end_time):
    """
    Function responsible for calculating the volunteer's reaction time to a given stimulus.
    :param start_time: Stimulus start time in milliseconds
    :param end_time: Volunteer response time in milliseconds
    :return: The function returns the reaction time in seconds
    """
    return ticks_diff(end_time, start_time) / 1000


def save_data(filename, data):
    """
    Function responsible for saving the obtained reaction time results in a file.
    :param filename: Name that the output file should receive, with the extension
    :param data: Data to be saved in the output file
    :return: The function has no return
    """
    with open(filename, 'w+') as f:
        # Escrever cada valor em uma linha separada
        for index, value in enumerate(data, start=1):
            f.write(f'{index}   {value}\n')


def anticipation_test(wait_time_start, wait_time, push_button_1, push_button_2=None):
    while ticks_diff(ticks_ms(), wait_time_start) < wait_time:
        if push_button_1.value() or push_button_2.value() if push_button_2 else True:

            return True

    return False
