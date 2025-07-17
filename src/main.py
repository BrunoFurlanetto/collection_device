from tkinter import messagebox

from src.interface.gui.initial_screen import initial_screen

if __name__ == "__main__":
    try:
        initial_screen()

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao inicializar o software: {e}")
