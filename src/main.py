import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from get_remote_files import get_test_files
from time import sleep

from src.interface.gui.initial_screen import initial_screen

# Caminho para o interpretador do Python na venv
PYTHON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\\venv\\Scripts\\python')


def connect_esp(port):
    try:
        messagebox.showinfo("Instrução", 'Ao abrir o terminal, pressione "ctrl + B" e execute:\n\nexecfile("protocols/initial/initialization.py")')
        subprocess.call(f'{PYTHON_PATH} -m serial.tools.miniterm {port} 115200')
    except Exception as e:
        messagebox.showerror("Erro de conexão", f"Erro na conexão com o microcontrolador: {e}")


def download_test_files(port, modality_initials):
    if not modality_initials:
        messagebox.showwarning("Aviso", "Digite as iniciais da modalidade.")
        return
    try:
        get_test_files(port, modality_initials.lower().replace(" ", "_"))
        messagebox.showinfo("Sucesso", "Arquivos de teste baixados com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar arquivos: {e}")


if __name__ == "__main__":
    initial_screen()
