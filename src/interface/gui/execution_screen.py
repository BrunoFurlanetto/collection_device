import tkinter as tk
from tkinter import ttk
import json
import os
from threading import Thread
from time import sleep
from src.serialcom.serial_command import send_test, send_familiarization

translate_senses = {
    "Visual": "Visual",
    "Auditory": "Auditivo",
    "Tactile": "Tátil",
}

translate_types = {
    "Simple": "Simples",
    "Choice": "Escolha",
}


# Replace these functions with your actual collection and familiarization scripts
def run_test(sense, test_type):
    return send_test(sense, test_type)


def familiarization(sense, test_type):
    return send_familiarization(sense, test_type)


def start_execution_screen():
    # Read the session configurations
    config_path = os.path.join("src", "config", "session_config.json")

    if not os.path.exists(config_path):
        print("Arquivo de configurações não encontrada.")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    root = tk.Tk()
    root.title("Execução dos testes")
    root.geometry("600x400")
    root.resizable(False, False)

    sense_order = config["order_senses"]
    test_order = config["order_tests"]

    all_tests = [(sense, test_type) for sense in sense_order for test_type in test_order[sense]]
    total_tests = len(all_tests)
    current_index = tk.IntVar(value=0)

    # Function to update the visual display
    def update_current_test_label():
        i = current_index.get()

        if i < total_tests:
            sense, test_type = all_tests[i]
            current_test_label.config(text=f"Teste atual: {translate_senses[sense].upper()} - {translate_types[test_type].upper()}")
            remaining_tests_label.config(text=f"Testes restantes: {total_tests - i}")
            progress['value'] = (i / total_tests) * 100
        else:
            current_test_label.config(text="Todos os testes foram completados.")
            remaining_tests_label.config(text="Testes completados!")
            progress['value'] = 100

            # Disable the buttons after completion
            familiarization_button.config(state="disabled")
            test_button.config(state="disabled")

    def run_familiarization():
        i = current_index.get()

        if i < total_tests:
            sense, test_type = all_tests[i]
            Thread(target=familiarization, args=(sense, test_type), daemon=True).start()

    def run_test_sequence():
        i = current_index.get()
        if i >= total_tests:
            return

        sense, test_type = all_tests[i]

        def exec_and_update():
            run_test(sense, test_type)
            current_index.set(i + 1)
            update_current_test_label()

        Thread(target=exec_and_update, daemon=True).start()

    # Test order
    tk.Label(root, text="Ordem dos testes:", font=("Arial", 12, "bold")).pack(pady=5)
    order_text = "\n".join([f"{i + 1}. {translate_senses[sense].upper()} - {translate_types[test_type].upper()}" for i, (sense, test_type) in enumerate(all_tests)])
    tk.Label(root, text=order_text, justify="left").pack()

    # Progress bar
    progress = ttk.Progressbar(root, length=500, mode="determinate")
    progress.pack(pady=10)
    progress['maximum'] = 100

    # Current test label
    current_test_label = tk.Label(root, text="", font=("Arial", 11, "bold"))
    current_test_label.pack(pady=5)

    # Remaining tests label
    remaining_tests_label = tk.Label(root, text="Testes restantes:", font=("Arial", 11))
    remaining_tests_label.pack(pady=5)

    # Update the label with the current test
    update_current_test_label()

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Familiarization button
    familiarization_button = tk.Button(button_frame, text="Familiarização", command=run_familiarization, width=20)
    familiarization_button.pack(side="left", padx=10)

    # Start test button
    test_button = tk.Button(button_frame, text="Iniciar teste", command=run_test_sequence, width=20)
    test_button.pack(side="left", padx=10)

    # Finish collection button
    tk.Button(button_frame, text="Coleta finalizada", command=root.quit, width=20).pack(side="left", padx=10)

    root.mainloop()
