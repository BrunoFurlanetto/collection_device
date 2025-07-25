import tkinter as tk


class TempAlert:
    """
    Exibe uma janela de aviso padrão, com barra de título e bordas,
    que se fecha automaticamente após um tempo.
    """
    def __init__(self, master, message, duration=3000, width=300, height=100):
        # Cria uma janela Toplevel ligada ao master, sem bloquear o loop principal
        self.win = tk.Toplevel(master)
        self.win.title("Aviso")
        self.win.resizable(False, False)
        self.win.transient(master)
        self.win.attributes('-topmost', True)

        # Frame interno para padding
        frame = tk.Frame(self.win, padx=10, pady=10)
        frame.pack(fill='both', expand=True)

        # Label centralizada com quebra de linha
        lbl = tk.Label(
            frame,
            text=message,
            fg='black',
            font=('Arial', 11),
            wraplength=width - 20,
            justify='center'
        )
        lbl.pack(fill='both', expand=True)

        # Define tamanho e centraliza em relação ao master
        self.win.geometry(f"{width}x{height}")
        self._center_window(master, width, height)

        # Agenda o fechamento automático após duration milissegundos
        self.win.after(duration, self._close)

    def _center_window(self, master, w, h):
        master.update_idletasks()
        mx = master.winfo_rootx()
        my = master.winfo_rooty()
        mw = master.winfo_width()
        mh = master.winfo_height()
        x = mx + (mw - w) // 2
        y = my + (mh - h) // 2
        self.win.geometry(f"+{x}+{y}")

    def _close(self):
        try:
            self.win.destroy()
        except Exception:
            pass
