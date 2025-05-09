import tkinter as tk
from tkinter import ttk
import os
import json
import random

from src.interface.gui.execution_screen import start_execution_screen

VIAS = ['Visual', 'Auditiva', 'Tátil']
TESTES = ['Simples', 'Escolha']


def sortear_ordem_vias(via_order_vars):
    nova_ordem = random.sample(VIAS, len(VIAS))

    for var, via in zip(via_order_vars, nova_ordem):
        var.set(via)


def sortear_ordem_testes(test_order_vars, via):
    nova_ordem = random.sample(TESTES, len(TESTES))

    for var, teste in zip(test_order_vars[via], nova_ordem):
        var.set(teste)


def criar_interface_ordem(frame):
    # Criar as variáveis aqui, depois que a janela principal existe
    via_order_vars = [tk.StringVar(frame) for _ in VIAS]
    test_order_vars = {
        via: [tk.StringVar(frame) for _ in TESTES]
        for via in VIAS
    }

    ttk.Label(frame, text="Ordem das vias sensoriais:").grid(row=0, column=0, columnspan=4, pady=5, sticky='w')

    for i in range(len(VIAS)):
        via_order_vars[i].set(VIAS[i])
        ttk.OptionMenu(frame, via_order_vars[i], VIAS[i], *VIAS).grid(row=1, column=i)

    ttk.Button(frame, text="Sortear vias", command=lambda: sortear_ordem_vias(via_order_vars)).grid(row=1,
                                                                                                    column=len(VIAS),
                                                                                                    padx=10)

    row_offset = 2
    for idx, via in enumerate(VIAS):
        ttk.Label(frame, text=f"{via} - Ordem dos testes:").grid(row=row_offset, column=0, columnspan=4, pady=5,
                                                                 sticky='w')

        for j in range(len(TESTES)):
            test_order_vars[via][j].set(TESTES[j])
            ttk.OptionMenu(frame, test_order_vars[via][j], TESTES[j], *TESTES).grid(row=row_offset + 1, column=j)

        ttk.Button(frame, text="Sortear testes", command=lambda v=via: sortear_ordem_testes(test_order_vars, v)).grid(
            row=row_offset + 1, column=len(TESTES), padx=10)

        row_offset += 2

    return via_order_vars, test_order_vars


def submit_data(porta, codigo, mao, root, via_order_vars, test_order_vars):
    config = {
        "porta": porta.get(),
        "codigo_participante": codigo.get(),
        "mao_dominante": mao.get(),
        "ordem_vias": [var.get() for var in via_order_vars],
        "ordem_testes": {
            via: [var.get() for var in test_order_vars[via]]
            for via in VIAS
        }
    }

    os.makedirs("src/config", exist_ok=True)
    with open("src/config/config.json", "w") as f:
        json.dump(config, f, indent=4)

    print("Configuração salva:")
    print(json.dumps(config, indent=4))
    root.destroy()
    start_execution_screen()


def initial_screen():
    root = tk.Tk()
    root.title("Configuração da Coleta")
    root.geometry("400x400")
    style = ttk.Style()
    style.configure('TMenubutton', background='white')

    # Frame de dados iniciais
    top_frame = ttk.Frame(root, padding=10)
    top_frame.pack(fill='x')

    ttk.Label(top_frame, text="Porta de Comunicação:").grid(row=0, column=0, sticky='w')
    porta_var = tk.StringVar(root)
    porta_var = tk.StringVar(root, value='COM5')
    porta_entry = ttk.Entry(top_frame, textvariable=porta_var, width=20)
    porta_entry.grid(row=1, column=0, padx=5)

    ttk.Label(top_frame, text="Código do Participante:").grid(row=0, column=1, sticky='w')
    codigo_var = tk.StringVar(root)
    codigo_entry = ttk.Entry(top_frame, textvariable=codigo_var, width=20)
    codigo_entry.grid(row=1, column=1, padx=5)

    ttk.Label(top_frame, text="Mão Dominante:").grid(row=0, column=2, sticky='w')
    mao_var = tk.StringVar(root)
    mao_menu = ttk.OptionMenu(top_frame, mao_var, '', "Direita", "Esquerda")
    mao_menu.grid(row=1, column=2, padx=5)

    # Frame de configuração de testes
    ordem_frame = ttk.Frame(root, padding=10)
    ordem_frame.pack(fill='both', expand=True)
    via_order_vars, test_order_vars = criar_interface_ordem(ordem_frame)

    # Botão de envio
    bottom_frame = ttk.Frame(root, padding=10)
    bottom_frame.pack(fill='x')
    ttk.Button(bottom_frame, text="Iniciar Coleta",
               command=lambda: submit_data(porta_var, codigo_var, mao_var, root, via_order_vars, test_order_vars)).pack(
        pady=10)

    root.mainloop()
