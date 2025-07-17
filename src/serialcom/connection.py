import subprocess
import os
from tkinter import messagebox
from time import sleep
from src.serialcom.commands import send_command

PYTHON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\\venv\\Scripts\\python')


def connect_esp(port):
    try:
        messagebox.showinfo("Instrução", 'Ao abrir o terminal, pressione "ctrl + B" e execute:\n\nexecfile("protocols/initial/initialization.py")')
        subprocess.call(f'{PYTHON_PATH} -m serial.tools.miniterm {port} 115200}')
        send_command('start_initialization', '')  # Envia comando inicial para o ESP32
        sleep(2)  # Aguarda o ESP32 estar pronto
        messagebox.showinfo("Sucesso", "Conexão estabelecida com o microcontrolador!")
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Erro na conexão com o microcontrolador: {e}")
