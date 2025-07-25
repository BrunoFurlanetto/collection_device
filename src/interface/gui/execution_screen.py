import tkinter as tk
from tkinter import ttk
import json
import os
from threading import Thread
from time import sleep

from src.get_remote_files import get_test_files
from src.interface.gui.temp_messages import TempAlert
from src.serialcom.serial_command import ESPSerialClient


translate_types = {
    "Simples": "Simple",
    "Escolha": "Choice",
}


class TestExecutionScreen:
    def __init__(self, config_path="src/config/session_config.json"):
        self.config_path = config_path
        self.config = self.load_config()

        if not self.config:
            print("Arquivo de configurações não encontrado.")

            return

        self.root = tk.Tk()
        self.root.title("Execução dos testes")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.sense_order = self.config["ORDER_SENSES"]
        self.test_order = self.config["ORDER_TESTS"]

        self.all_tests = [(sense, test_type) for sense in self.sense_order for test_type in self.test_order[sense]]
        self.total_tests = len(self.all_tests)
        self.current_index = tk.IntVar(value=0)

        self.ser = ESPSerialClient()

        self.setup_ui()

    def load_config(self):
        if not os.path.exists(self.config_path):

            return None
        with open(self.config_path, "r", encoding="utf-8") as f:

            return json.load(f)

    def setup_ui(self):
        sense_order = self.config["ORDER_SENSES"]
        test_order = self.config["ORDER_TESTS"]

        # Create the interface
        self.create_test_order_label(sense_order, test_order)
        self.create_progress_bar()

        self.current_test_label = tk.Label(self.root, text="", font=("Arial", 11, "bold"))
        self.current_test_label.pack(pady=5)

        self.remaining_tests_label = tk.Label(self.root, text="Testes restantes:", font=("Arial", 11))
        self.remaining_tests_label.pack(pady=5)

        self.update_current_test_label()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.familiarization_button = tk.Button(button_frame, text="Familiarização", command=self.run_familiarization, width=20)
        self.familiarization_button.pack(side="left", padx=10)

        self.test_button = tk.Button(button_frame, text="Iniciar teste", command=self.run_test_sequence, width=20)
        self.test_button.pack(side="left", padx=10)

        self.end_button = tk.Button(button_frame, text="Coleta finalizada", command=self.end_test, width=20)
        self.end_button.pack(side="left", padx=10)

    def create_test_order_label(self, sense_order, test_order):
        order_text = "\n".join([f"{i + 1}. {sense.upper()} - {test_type.upper()}" for i, (sense, test_type) in enumerate(self.all_tests)])
        tk.Label(self.root, text=order_text, justify="left").pack()

    def create_progress_bar(self):
        self.progress = ttk.Progressbar(self.root, length=500, mode="determinate")
        self.progress.pack(pady=10)
        self.progress['maximum'] = 100

    def update_current_test_label(self):
        i = self.current_index.get()

        if i < self.total_tests:
            sense, test_type = self.all_tests[i]
            self.current_test_label.config(text=f"Teste atual: {sense.upper()} - {test_type.upper()}")
            self.remaining_tests_label.config(text=f"Testes restantes: {self.total_tests - i}")
            self.progress['value'] = (i / self.total_tests) * 100
        else:
            self.current_test_label.config(text="Todos os testes foram completados.")
            self.remaining_tests_label.config(text="Testes completados!")
            self.progress['value'] = 100

    def _disable_all_buttons(self, finish=False):
        if finish:
            for btn in (self.familiarization_button, self.test_button):
                btn.config(state="disabled")
        else:
            for btn in (self.familiarization_button, self.test_button, self.end_button):
                btn.config(state="disabled")

    def _enable_all_buttons(self):
        for btn in (self.familiarization_button, self.test_button, self.end_button):
            btn.config(state="normal")

    def run_familiarization(self):
        i = self.current_index.get()

        def exec_familiarization():
            self._disable_all_buttons()
            self.ser.send_command_and_wait(self.root, f'F{sense.upper()[0]}{translate_types[test_type].upper()[0]}')
            self._enable_all_buttons()

        if i < self.total_tests:
            sense, test_type = self.all_tests[i]
            # Simulando a chamada da função de familiarização
            Thread(target=exec_familiarization, daemon=True).start()

    def run_test_sequence(self):
        i = self.current_index.get()
        sense, test_type = self.all_tests[i]

        if i >= self.total_tests:
            return

        def exec_and_update():
            self._disable_all_buttons()
            self.ser.send_command_and_wait(self.root, f'T{sense.upper()[0]}{translate_types[test_type].upper()[0]}')
            self._enable_all_buttons()
            self.current_index.set(i + 1)
            self.update_current_test_label()

        Thread(target=exec_and_update, daemon=True).start()

    def end_test(self):
        # 1) desabilita botões
        self._disable_all_buttons()
        self.ser.close()
        self.root.config(cursor="watch")
        self.root.update_idletasks()

        Thread(target=self._retrieve_and_close, daemon=True).start()

    def _retrieve_and_close(self):
        # roda a função de fato (que faz o serial, salva arquivos...)
        TempAlert(self.root, "Processando os resultados obtidos...", duration=3000)
        get_test_files(self.root)

        def on_done():
            self.root.config(cursor="")
            self.root.destroy()
            from src.interface.gui.initial_screen import initial_screen
            initial_screen()

        self.root.after(0, on_done)

    def start(self):
        self.ser.open()
        self.root.mainloop()


def start_execution_screen():
    execution_screen = TestExecutionScreen()
    execution_screen.start()
