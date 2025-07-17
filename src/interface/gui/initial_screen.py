import tkinter as tk
from tkinter import ttk
import os
import json
import random
from tkinter import messagebox

from src.interface.gui.ports_config import configure_ports
from src.interface.gui.execution_screen import start_execution_screen

VIAS = ['Visual', 'Auditiva', 'Tátil']
TESTES = ['Simples', 'Escolha']


def sortear_ordem_vias(via_order_vars):
    nova_ordem = random.sample(VIAS, len(VIAS))

    for var, via in zip(via_order_vars, nova_ordem):
        var.set(via)


def sortear_ordem_testes(test_order_vars, via):
    new_order = random.sample(TESTES, len(TESTES))

    for var, teste in zip(test_order_vars[via], new_order):
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
        ttk.OptionMenu(frame, via_order_vars[i], VIAS[i], *VIAS).grid(row=1, column=i, pady=5, padx=5)

    ttk.Button(frame, text="Sortear vias", command=lambda: sortear_ordem_vias(via_order_vars)).grid(row=1,
                                                                                                    column=len(VIAS),
                                                                                                    padx=10, pady=10)

    row_offset = 2
    for idx, via in enumerate(VIAS):
        ttk.Label(frame, text=f"{via} - Ordem dos testes:").grid(row=row_offset, column=0, columnspan=4, pady=5,
                                                                 sticky='w')

        for j in range(len(TESTES)):
            test_order_vars[via][j].set(TESTES[j])
            ttk.OptionMenu(frame, test_order_vars[via][j], TESTES[j], *TESTES).grid(row=row_offset + 1, column=j,
                                                                                     pady=5, padx=5)

        ttk.Button(frame, text="Sortear testes", command=lambda v=via: sortear_ordem_testes(test_order_vars, v)).grid(
            row=row_offset + 1, column=len(TESTES), padx=10, pady=10)

        row_offset += 2

    return via_order_vars, test_order_vars


# Função de validação das entradas
def validar_entradas(porta, codigo, mao):
    if not porta.get():
        messagebox.showwarning("Aviso", "Por favor, insira a porta de comunicação.")
        return False
    if not codigo.get():
        messagebox.showwarning("Aviso", "Por favor, insira o código do participante.")
        return False
    if not mao.get():
        messagebox.showwarning("Aviso", "Por favor, selecione a mão dominante.")
        return False
    return True


# Função de envio de dados para o arquivo de configuração
def submit_data(porta, codigo, mao, root, via_order_vars, test_order_vars):
    if not validar_entradas(porta, codigo, mao):
        return  # Interrompe a execução caso a validação falhe

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

    try:
        os.makedirs("src/config", exist_ok=True)
        with open("src/config/session_config.json", "w") as f:
            json.dump(config, f, indent=4)

        messagebox.showinfo("Sucesso", "Configuração salva com sucesso.")
        print("Configuração salva:")
        print(json.dumps(config, indent=4))
        root.destroy()
        start_execution_screen()

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar a configuração: {e}")


# Função de tela inicial
def initial_screen():
    root = tk.Tk()
    root.title("Configuração da Coleta")
    root.geometry("400x500")
    root.resizable(False, False)
    style = ttk.Style()
    style.configure('TMenubutton', background='white')

    # Criando o menu de configurações
    menubar = tk.Menu(root)
    config_menu = tk.Menu(menubar, tearoff=0)
    config_menu.add_command(label="Configurar Portas", command=configure_ports)
    menubar.add_cascade(label="Configurações", menu=config_menu)
    root.config(menu=menubar)

    # Frame de dados iniciais
    top_frame = ttk.Frame(root, padding=10)
    top_frame.pack(fill='x')

    ttk.Label(top_frame, text="Porta de Comunicação:").grid(row=0, column=0, sticky='w')
    porta_var = tk.StringVar(root, value='COM5')
    porta_entry = ttk.Entry(top_frame, textvariable=porta_var, width=20)
    porta_entry.grid(row=1, column=0, padx=5, pady=5, sticky='ew')  # 'ew' para expandir horizontalmente

    ttk.Label(top_frame, text="Código do Participante:").grid(row=0, column=1, sticky='w')
    codigo_var = tk.StringVar(root)
    codigo_entry = ttk.Entry(top_frame, textvariable=codigo_var, width=20)
    codigo_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    ttk.Label(top_frame, text="Mão Dominante:").grid(row=0, column=2, sticky='w')
    mao_var = tk.StringVar(root)
    mao_menu = ttk.OptionMenu(top_frame, mao_var, '', "Direita", "Esquerda")
    mao_menu.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

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
