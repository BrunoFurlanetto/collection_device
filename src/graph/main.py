import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD


class ReactionTimeAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador de Tempo de Reação")
        self.root.geometry("400x400")
        self.sensory_path = ''

        # Valores de referência
        self.reference_values = {
            # 'trs_v': ('Fernando Alonso', 0.120),  # (Descrição, valor)
            # 'trs_a': ('Usain Bolt', 0.155),
            # 'tre_v': ('Visual', None),
            # 'tre_a': ('Auditivo', None),
            # 'tre_t': ('Tátil', None),
            # 'trs_t': ('Tátil', None)
        }

        self.sensory_map = {
            'v': 'Visual',
            'a': 'Auditiva',
            't': 'Tátil',
        }

        # Interface
        self.create_widgets()

    def adjust_window_width(self, event):
        if event.widget == self.canvas:
            canvas_width = event.width
            window_width = canvas_width + 40
            self.root.geometry(f"{window_width}x{self.root.winfo_height()}")

    def create_widgets(self):
        # Frame principal com scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # === LOGO ESQUERDO ===
        logo_left_frame = ttk.Frame(main_frame)
        logo_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        logo_left = self.load_logo_image("src\\graph\\logos\\leplo.png", size=(100, 100))
        if logo_left:
            left_label = ttk.Label(logo_left_frame, image=logo_left)
            left_label.image = logo_left
            left_label.pack()

        # Canvas e scrollbar
        self.canvas = tk.Canvas(main_frame)
        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame real que contém os gráficos (centralizável)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame_wrapper = ttk.Frame(self.scrollable_frame)
        self.scrollable_frame_wrapper.pack()
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Centraliza o wrapper no scrollable_frame
        self.scrollable_frame_wrapper.pack(anchor="center", pady=10)

        # Adiciona a frame ao canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Ajusta scrollregion dinamicamente
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Opcional: atualiza largura do frame sempre que o canvas for redimensionado
        self.canvas.bind("<Configure>", self._resize_scrollable_frame)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # === LOGO DIREITO ===
        logo_right_frame = ttk.Frame(main_frame)
        logo_right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        logo_right = self.load_logo_image("src\\graph\\logos\\proparki.png", size=(100, 100))
        if logo_right:
            right_label = ttk.Label(logo_right_frame, image=logo_right)
            right_label.image = logo_right
            right_label.pack()

        # Controles
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        load_btn = ttk.Button(control_frame, text="Carregar Arquivos", command=self.browse_files)
        load_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = ttk.Button(control_frame, text="Limpar Gráficos", command=self.clear_graphs)
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Configurar arrastar e soltar (opcional)
        try:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.handle_drop)
        except Exception:
            # Se tkdnd não estiver disponível, não faz nada
            pass

    def load_logo_image(self, path, size=(100, 100)):
        try:
            img = Image.open(path)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("Erro ao carregar imagem", str(e))
            return None

    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.process_files([f for f in files if f.endswith('.dat')])

    def browse_files(self):
        files = filedialog.askopenfilenames(filetypes=[("DAT files", "*.dat")])
        if files:
            self.process_files(files)

    def clear_graphs(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def parse_filename(self, filename):
        basename = os.path.basename(filename)
        parts = basename.split('_')

        if len(parts) < 3:
            return None, None, None

        test_type = parts[0]
        sensory_path = parts[1]
        self.sensory_path = self.sensory_map[sensory_path]
        participant = parts[2]

        ref_key = f"{test_type}_{sensory_path}"
        test_name = {
            'trs': 'Tempo de Reação Simples',
            'tre': 'Tempo de Reação de Escolha'
        }.get(test_type, test_type)

        return ref_key, test_name, participant

    def read_data_file(self, filename):
        trials = []
        times = []

        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        try:
                            # Primeiro converte o tempo
                            time = float(parts[1])
                            # Se conversão do tempo for bem-sucedida, adiciona ambos
                            trials.append(int(parts[0]))
                            times.append(time)
                        except ValueError:
                            # Ignora a linha inteira se houver erro em qualquer valor
                            continue
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler arquivo {filename}: {str(e)}")
            return None, None

        return trials, times

    def process_files(self, files):
        if not files:
            return

        self.clear_graphs()

        for file in files:
            ref_key, test_name, participant = self.parse_filename(file)
            trials, times = self.read_data_file(file)

            if not trials or not times or len(trials) != len(times):
                continue

            self.create_individual_graph(
                file_path=file,
                test_name=test_name,
                participant=participant,
                trials=trials,
                times=times,
                ref_key=ref_key
            )

        # Rolagem para o topo
        self.canvas.yview_moveto(0)

    def _resize_scrollable_frame(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def create_individual_graph(self, file_path, test_name, participant, trials, times, ref_key):
        # Criar wrapper que ocupa toda a largura disponível
        wrapper = ttk.Frame(self.scrollable_frame)
        wrapper.pack(fill=tk.X, padx=5, pady=5)

        # Container centralizado dentro do wrapper
        graph_container = ttk.Frame(wrapper, borderwidth=2, relief="groove", padding=5)
        graph_container.pack(anchor="center")

        # Configurar figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), dpi=100)
        fig.suptitle(f"{test_name} - {self.sensory_path}")

        # Gráfico 1: Linhas (tentativas vs tempo)
        ax1.plot(trials, times, 'o-', color='blue', label='Tempo por tentativa')
        ax1.axhline(y=np.mean(times), color='green', linestyle='--', label=f'Média: {np.mean(times):.3f}s')

        # Adicionar referência se existir
        ref_info = self.reference_values.get(ref_key, (None, None))
        if ref_info[1] is not None:
            ax1.axhline(y=ref_info[1], color='red', linestyle='-',
                        label=f'{ref_info[0]}: {ref_info[1]}s')

        ax1.set_xlabel('Tentativa')
        ax1.set_ylabel('Tempo (s)')
        ax1.set_title('Tempos por Tentativa')
        ax1.legend()
        ax1.grid(True)

        # Gráfico 2: Barra única com a média
        mean_value = np.mean(times)
        bar = ax2.bar(['Média'], [mean_value], color='blue', width=0.3)
        ax2.set_title('Média do Tempo de Reação')
        ax2.set_ylabel('Tempo (s)')
        # ax2.grid(True, axis='y')

        # Adicionar valor na barra
        ax2.text(0, mean_value, f'{mean_value:.3f}s',
                 ha='center', va='bottom')

        # Ajustar limites para melhor visualização
        ax2.set_ylim(0, max(mean_value * 1.5, 0.5))  # Limite mínimo de 0.5s se a média for muito baixa
        ax2.set_xlim(-0.5, 0.5)

        # Adicionar linha de referência se existir
        if ref_info[1] is not None:
            ax2.axhline(y=ref_info[1], color='red', linestyle='-',
                        label=f'{ref_info[0]}: {ref_info[1]}s')
            ax2.legend()

        plt.tight_layout()

        # Adicionar ao tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ReactionTimeAnalyzer(root)
    root.mainloop()
