import tkinter as tk
from tkinter import ttk
import json
import os
from threading import Thread
from time import sleep


# Substitua estas funções pelos seus scripts reais de coleta e familiarização
def executar_teste(via, tipo):
    print(f"Iniciando teste {tipo} da via {via}...")
    sleep(2)  # Simula tempo de execução do teste


def familiarizacao(via, tipo):
    print(f"Familiarização do teste {tipo} da via {via}...")
    sleep(1)  # Simula tempo de execução da familiarização


def start_execution_screen():
    # Lê as configurações da sessão
    config_path = os.path.join("src", "config", "session_config.json")
    if not os.path.exists(config_path):
        print("Arquivo de configuração não encontrado.")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    root = tk.Tk()
    root.title("Execução dos Testes")
    root.geometry("600x400")
    root.resizable(False, False)

    sense_order = config["ordem_vias"]
    test_order = config["ordem_testes"]

    all_tests = [(sense, tipo) for sense in sense_order for tipo in test_order[sense]]
    total_tests = len(all_tests)
    current_index = tk.IntVar(value=0)

    # Função para atualizar visualmente
    def update_current_test_label():
        i = current_index.get()
        if i < total_tests:
            via, tipo = all_tests[i]
            current_test_label.config(text=f"Teste atual: {via.upper()} - {tipo.upper()}")
            remaining_tests_label.config(text=f"Testes restantes: {total_tests - i - 1}")
            progress['value'] = ((i + 1) / total_tests) * 100
        else:
            current_test_label.config(text="Todos os testes foram concluídos.")
            remaining_tests_label.config(text="Todos os testes concluídos!")
            progress['value'] = 100

            # Desabilitar os botões após a conclusão
            familiarizacao_button.config(state="disabled")
            teste_button.config(state="disabled")

    def run_familiarizacao():
        i = current_index.get()

        if i < total_tests:
            via, tipo = all_tests[i]
            Thread(target=familiarizacao, args=(via, tipo), daemon=True).start()

    def run_teste():
        i = current_index.get()
        if i >= total_tests:
            return

        via, tipo = all_tests[i]

        def exec_and_update():
            executar_teste(via, tipo)
            current_index.set(i + 1)
            update_current_test_label()

        Thread(target=exec_and_update, daemon=True).start()

    # Ordem dos testes
    tk.Label(root, text="Ordem dos testes:", font=("Arial", 12, "bold")).pack(pady=5)
    order_text = "\n".join([f"{i + 1}. {via.upper()} - {tipo.upper()}" for i, (via, tipo) in enumerate(all_tests)])
    tk.Label(root, text=order_text, justify="left").pack()

    # Progresso
    progress = ttk.Progressbar(root, length=500, mode="determinate")
    progress.pack(pady=10)
    progress['maximum'] = 100

    # Teste atual
    current_test_label = tk.Label(root, text="", font=("Arial", 11, "bold"))
    current_test_label.pack(pady=5)

    # Testes restantes
    remaining_tests_label = tk.Label(root, text="Testes restantes:", font=("Arial", 11))
    remaining_tests_label.pack(pady=5)

    # Atualiza o label com o teste atual
    update_current_test_label()

    # Botões
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Botão para Familiarização
    familiarizacao_button = tk.Button(button_frame, text="Familiarização", command=run_familiarizacao, width=20)
    familiarizacao_button.pack(side="left", padx=10)

    # Botão para Iniciar Teste
    teste_button = tk.Button(button_frame, text="Iniciar Teste", command=run_teste, width=20)
    teste_button.pack(side="left", padx=10)

    # Finalizar botão
    tk.Button(button_frame, text="Finalizar Coleta", command=root.quit, width=20).pack(side="left", padx=10)

    root.mainloop()
