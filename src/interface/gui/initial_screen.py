import subprocess
import sys

import tkinter as tk
from tkinter import ttk
import os
import json
import random
from tkinter import messagebox

from src.graph.main import ReactionTimeAnalyzer
from src.interface.gui.ports_config import configure_ports
from src.interface.gui.execution_screen import start_execution_screen
from src.serialcom.serial_command import soft_reset_esp


SENSORY_MODES = ['Visual', 'Auditivo', 'Tátil']
TEST_TYPES = ['Simples', 'Escolha']


def shuffle_sensory_order(via_order_vars):
    new_order = random.sample(SENSORY_MODES, len(SENSORY_MODES))

    for var, via in zip(via_order_vars, new_order):
        var.set(via)


def shuffle_test_order(test_order_vars, via):
    new_order = random.sample(TEST_TYPES, len(TEST_TYPES))

    for var, test in zip(test_order_vars[via], new_order):
        var.set(test)


def create_order_interface(frame):
    # Create the variables after the main window exists
    via_order_vars = [tk.StringVar(frame) for _ in SENSORY_MODES]
    test_order_vars = {
        via: [tk.StringVar(frame) for _ in TEST_TYPES]
        for via in SENSORY_MODES
    }

    ttk.Label(frame, text="Ordem das vias sensoriais:").grid(row=0, column=0, columnspan=4, pady=5, sticky='w')

    for i in range(len(SENSORY_MODES)):
        via_order_vars[i].set(SENSORY_MODES[i])
        ttk.OptionMenu(frame, via_order_vars[i], SENSORY_MODES[i], *SENSORY_MODES).grid(row=1, column=i, pady=5, padx=5)

    ttk.Button(frame, text="Sortear ordem", command=lambda: shuffle_sensory_order(via_order_vars)).grid(
        row=1,
        column=len(SENSORY_MODES),
        padx=10,
        pady=10
    )

    row_offset = 2
    for idx, via in enumerate(SENSORY_MODES):
        ttk.Label(frame, text=f"{via} - Ordem dos testes:").grid(row=row_offset, column=0, columnspan=4, pady=5,
                                                                 sticky='w')

        for j in range(len(TEST_TYPES)):
            test_order_vars[via][j].set(TEST_TYPES[j])
            ttk.OptionMenu(frame, test_order_vars[via][j], TEST_TYPES[j], *TEST_TYPES).grid(
                row=row_offset + 1,
                column=j,
                pady=5,
                padx=5
            )

        ttk.Button(frame, text="Sortear testes", command=lambda v=via: shuffle_test_order(test_order_vars, v)).grid(
            row=row_offset + 1, column=len(TEST_TYPES), padx=10, pady=10)

        row_offset += 2

    return via_order_vars, test_order_vars


# Validation function for inputs
def validate_entries(port, code, hand):
    if not port.get():
        messagebox.showwarning("Atenção", "Forneça a porta de comunicação com o dispositivo.")

        return False

    if not code.get():
        messagebox.showwarning("Atenção", "Forneça o código do participante.")

        return False

    if not hand.get():
        messagebox.showwarning("Atenção", "Informe a mão dominante do participante.")

        return False

    return True


# Function to submit data to the configuration file
def submit_data(port, code, hand, root, via_order_vars, test_order_vars):
    if not validate_entries(port, code, hand):
        return  # Stop execution if validation fails

    config = {
        "PORT": port.get(),
        "PARTICIPANT_CODE": code.get().strip().upper(),
        "DOMINANT_HAND": hand.get()[0],
        "ORDER_SENSES": [var.get() for var in via_order_vars],
        "ORDER_TESTS": {
            via: [var.get() for var in test_order_vars[via]]
            for via in SENSORY_MODES
        }
    }

    try:
        os.makedirs("src/config", exist_ok=True)

        with open("src/config/session_config.json", "w") as f:
            json.dump(config, f, indent=4)

        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso.")
        root.destroy()
        send_config_to_esp()
        start_execution_screen()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o salvamento das configurações: {e}")


def send_config_to_esp():
    # 1) lê o JSON salvo
    base = os.path.dirname(__file__)  # .../src/interface/gui
    cfg = os.path.abspath(os.path.join(base, '..', '..', 'config', 'session_config.json'))
    ports_cfg = os.path.abspath(os.path.join(base, '..', '..', 'config', 'ports_config.json'))

    try:
        with open(cfg, 'r', encoding='utf-8') as f:
            session = json.load(f)
    except Exception as e:
        messagebox.showerror("Erro", f"Não consegui ler {cfg}: {e}")
        return

    port = session.get('PORT')

    if not port:
        messagebox.showerror("Erro", "Não achei a chave 'port' no JSON")
        return

    # 2) localiza o ampy.exe no venv
    #    sys.executable é .../venv/Scripts/python.exe
    scripts_dir = os.path.dirname(sys.executable)

    if sys.platform.startswith('win'):
        ampy_exe = os.path.join(scripts_dir, 'ampy.exe')
    else:
        ampy_exe = os.path.join(scripts_dir, 'ampy')  # num *nix seria venv/bin/ampy

    if not os.path.isfile(ampy_exe):
        messagebox.showerror("Erro", f"Não achei o ampy em {ampy_exe}\nInstale com pip install adafruit-ampy")

        return

    # 4) envia o arquivo
    put_session_config_cmd = [
        ampy_exe, '--port', port,
        'put', cfg, 'config/session_config.json'
    ]

    put_ports_config_cmd = [
        ampy_exe, '--port', port,
        'put', cfg, 'config/session_config.json'
    ]

    try:
        subprocess.run(put_session_config_cmd, check=True)
        messagebox.showinfo("Sucesso", "Configurações da seção enviado ao ESP!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro de envio", f"Falhou ao executar:\n{e.cmd}\n{e}")

    try:
        subprocess.run(put_ports_config_cmd, check=True)
        messagebox.showinfo("Sucesso", "Configurações das portas enviado ao ESP!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro de envio", f"Falhou ao executar:\n{e.cmd}\n{e}")

    reset_esp = [
        ampy_exe, '--port', port,
        'reset'
    ]

    soft_reset_esp()


# Initial screen function
def initial_screen():
    root = tk.Tk()
    root.title("Configurações da coleta")
    root.geometry("400x500")
    root.resizable(False, False)
    style = ttk.Style()
    style.configure('TMenubutton', background='white')

    # Creating the configuration menu
    menubar = tk.Menu(root)
    config_menu = tk.Menu(menubar, tearoff=0)
    config_menu.add_command(label="Configuração das portas", command=configure_ports)
    menubar.add_cascade(label="Configurações", menu=config_menu)

    # Results menu
    results_menu = tk.Menu(menubar, tearoff=0)
    results_menu.add_command(label="Graficar resultados", command=lambda: _open_analyzer(root))
    menubar.add_cascade(label="Resultados", menu=results_menu)

    root.config(menu=menubar)

    # Initial data frame
    top_frame = ttk.Frame(root, padding=10)
    top_frame.pack(fill='x')

    ttk.Label(top_frame, text="Porta de comunicação:").grid(row=0, column=0, sticky='w')
    port_var = tk.StringVar(root, value='COM5')
    port_entry = ttk.Entry(top_frame, textvariable=port_var, width=20)
    port_entry.grid(row=1, column=0, padx=5, pady=5, sticky='ew')  # 'ew' to expand horizontally

    ttk.Label(top_frame, text="Código do participante:").grid(row=0, column=1, sticky='w')
    code_var = tk.StringVar(root)
    code_entry = ttk.Entry(top_frame, textvariable=code_var, width=20)
    code_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    ttk.Label(top_frame, text="Mão dominante:").grid(row=0, column=2, sticky='w')
    hand_var = tk.StringVar(root)
    hand_menu = ttk.OptionMenu(top_frame, hand_var, '', "Direita", "Esquerda")
    hand_menu.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

    # Test configuration frame
    order_frame = ttk.Frame(root, padding=10)
    order_frame.pack(fill='both', expand=True)
    via_order_vars, test_order_vars = create_order_interface(order_frame)

    # Submit button
    bottom_frame = ttk.Frame(root, padding=10)
    bottom_frame.pack(fill='x')
    ttk.Button(bottom_frame, text="Iniciar coleta",
               command=lambda: submit_data(port_var, code_var, hand_var, root, via_order_vars, test_order_vars)).pack(
        pady=10)

    root.mainloop()


def _open_analyzer(master):
    # Open the Reaction Time Analyzer in a Toplevel window
    win = tk.Toplevel(master)
    ReactionTimeAnalyzer(win)
