from time import sleep


def initial_familiarization(low_group, high_group):
    print('Familiarização do teste auditivo iniciado.')
    while True:
        r = input('Pressione R para mostrar o estimulo sonoro da via direita e L para a esquerda ou Q para finalizar:').strip().lower()

        if r == 'r':
            high_group[1].duty(512)

            while True:
                if high_group[0].value():
                    high_group[1].duty(0)

                    break

        elif r == 'l':
            low_group[1].duty(512)

            while True:
                if low_group[0].value():
                    low_group[1].duty(0)

                    break

        elif r == 'q':
            print('Familiarização inicial finalizada, iniciando o teste em')
            for s in range(5, 0, -1):
                print(s)
                sleep(1)

            return
