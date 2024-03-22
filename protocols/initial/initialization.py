from machine import Pin

from protocols.auditory.main_test import auditory_choice_test, auditory_simple_test
from protocols.tactile.main_test import tactile_choice_test, tactile_simple_test
from protocols.visual.main_test import visual_choice_test, visual_simple_test


def reset_ports():
    ports = [15, 2, 4, 5, 18, 19, 21, 13, 12, 14, 27, 26, 25, 32, 23, 22, 34, 35]

    for port in ports:
        try:
            _ = Pin(port, Pin.OUT)
        except Exception:
            ...

    return


while True:
    reset_ports()
    print('=' * 100)
    print('Versão 1.0 do protótipo de dispositivo para captação do tempo de reação simples e de escolha')
    print('=' * 100)

    while True:
        print('Qual tipo de teste deseja iniciar? 1 - TR simples, 2 - TR de escolha, 0 - Sair')
        type_test = input().strip()

        try:
            type_test = int(type_test)
        except ValueError:
            print('O valor digitado não é uma opção válida!')
        else:
            if type_test in [0, 1, 2]:
                break
            else:
                print('Selecione uma opção válida, 1 ou 2!!')

    print('=' * 100)

    if int(type_test) == 0:
        print('Testes finalizados!! Pressione ctrl + Ç para sair')

        break

    while True:
        print('Forneça a opção de teste que deseja iniciar: 1 - Visual, 2 - Auditivo, 3 - Tátil, 0 - Finalizar')
        option_test = input().strip()

        try:
            option_test = int(option_test)
        except ValueError:
            print('O valor digitado não é uma opção válida!')
        else:
            if option_test in [0, 1, 2, 3]:
                break
            else:
                print('Selecione uma opção válida, de 0 a 3 apenas!!')

    print('=' * 100)

    if option_test == 0:
        print('Testes finalizados!! Pressione ctrl + Ç para sair')

        break
    if option_test == 1:
        if type_test == 1:
            print('Teste de tempo de reação simples visual iniciado!!')
            visual_simple_test()
        else:
            print('Teste de tempo de reação de escolha visual iniciado!!')
            visual_choice_test()
    if option_test == 2:
        if type_test == 1:
            print('Teste de tempo de reação simples auditivo de iniciado!!')
            auditory_simple_test()
        else:
            print('Teste de tempo de reação de esolha auditivo iniciado!!')
            auditory_choice_test()
    if int(option_test) == 3:
        if type_test == 1:
            print('Teste de tempo de reação simples tátil iniciado!!')
            tactile_simple_test()
        else:
            print('Teste de tempo de reação de escolha tátil iniciado!!')
            tactile_choice_test()
