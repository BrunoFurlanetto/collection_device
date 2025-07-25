import sys
import uselect
from utils.command_parser import parse_command

from protocols.auditory.familiarization import auditory_choice_familiarization, auditory_simple_familiarization
from protocols.auditory.main_test import auditory_choice_test, auditory_simple_test
from protocols.tactile.familiarization import tactile_choice_familiarization, tactile_simple_familiarization
from protocols.tactile.main_test import tactile_simple_test, tactile_choice_test
from protocols.visual.familiarization import visual_simple_familiarization, visual_choice_familiarization
from protocols.visual.main_test import visual_simple_test, visual_choice_test

serialPoll = uselect.poll()
serialPoll.register(sys.stdin, uselect.POLLIN)


def handle_command(command):
    """
    Handle a command received over serial.

    :param command: (String) the command to handle
    """
    if not command:  # ignora None ou string vazia
        return

    cmd = command.strip()

    # se iniciar com T:
    if cmd.startswith("T"):
        via = cmd[1]
        tipo = cmd[2]

        if via == 'V':
            if tipo == 'S':
                visual_simple_test()
                sys.stdout.write('SUCCESS\n')
            else:
                visual_choice_test()
                sys.stdout.write('SUCCESS\n')

        if via == 'A':
            if tipo == 'S':
                auditory_simple_test()
                sys.stdout.write('SUCCESS\n')
            else:
                auditory_choice_test()
                sys.stdout.write('SUCCESS\n')

        if via == 'T':
            if tipo == 'S':
                tactile_simple_test()
                sys.stdout.write('SUCCESS\n')
            else:
                tactile_choice_test()
                sys.stdout.write('SUCCESS\n')
        else:
            sys.stdout.write("ERROR:INVALID_COMMAND\n")
    elif cmd.startswith("F"):
        via = cmd[1]
        tipo = cmd[2]

        if via == 'V':
            if tipo == 'S':
                visual_simple_familiarization()
                sys.stdout.write('SUCCESS\n')
            else:
                visual_choice_familiarization()
                sys.stdout.write('SUCCESS\n')

        if via == 'A':
            if tipo == 'S':
                auditory_simple_familiarization()
                sys.stdout.write('SUCCESS\n')
            else:
                auditory_choice_familiarization()
                sys.stdout.write('SUCCESS\n')

        if via == 'T':
            if tipo == 'S':
                tactile_simple_familiarization()
                sys.stdout.write('SUCCESS\n')
            else:
                tactile_choice_familiarization()
                sys.stdout.write('SUCCESS\n')
    else:
        sys.stdout.write("ERROR:UNKNOWN_COMMAND\n")


def readSerial():
    """
    reads a single character over serial.

    :return: returns the character which was read, otherwise returns None
    """
    return sys.stdin.read(3) if serialPoll.poll(0) else None


# loop principal
while True:
    c = readSerial()
    if c is not None:
        handle_command(c)
