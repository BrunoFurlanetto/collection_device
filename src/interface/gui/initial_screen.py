import tkinter as tk
from tkinter import ttk
import os
import json
import random
from tkinter import messagebox

from src.interface.gui.ports_config import configure_ports
from src.interface.gui.execution_screen import start_execution_screen

SENSORY_MODES = ['Visual', 'Auditory', 'Tactile']
TEST_TYPES = ['Simple', 'Choice']


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

    ttk.Button(frame, text="Sortear ordem", command=lambda: shuffle_sensory_order(via_order_vars)).grid(row=1,
                                                                                                                column=len(SENSORY_MODES),
                                                                                                                padx=10, pady=10)

    row_offset = 2
    for idx, via in enumerate(SENSORY_MODES):
        ttk.Label(frame, text=f"{via} - Ordem dos testes:").grid(row=row_offset, column=0, columnspan=4, pady=5,
                                                           sticky='w')

        for j in range(len(TEST_TYPES)):
            test_order_vars[via][j].set(TEST_TYPES[j])
            ttk.OptionMenu(frame, test_order_vars[via][j], TEST_TYPES[j], *TEST_TYPES).grid(row=row_offset + 1, column=j,
                                                                                             pady=5, padx=5)

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
        "port": port.get(),
        "participant_code": code.get(),
        "dominant_hand": hand.get(),
        "order_senses": [var.get() for var in via_order_vars],
        "order_tests": {
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
        start_execution_screen()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o salvamento das configurações: {e}")


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
