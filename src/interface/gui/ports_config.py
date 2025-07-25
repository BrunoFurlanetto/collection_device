import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

# Default port values
DEFAULT_CONFIG = {
    "RIGHT_BUZZER": 18,
    "LEFT_BUZZER": 32,
    "RIGHT_VIBRACALL": 5,
    "LEFT_VIBRACALL": 33,
    "RIGHT_PUSH_BUTTON": 19,
    "LEFT_PUSH_BUTTON": 12,
    "RIGHT_LED": 2,
    "LEFT_LED": 14
}


# Function to load the configuration
def load_config():
    config_path = os.path.join("src", "config", "ports_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CONFIG


# Function to save the configuration
def save_config(config):
    os.makedirs("src/config", exist_ok=True)
    config_path = os.path.join("src", "config", "ports_config.json")

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")


# Function to reset the configuration to default values
def reset_to_default(entries):
    # Set all entries to the default values
    entries['right_buzzer'].delete(0, tk.END)
    entries['right_buzzer'].insert(0, DEFAULT_CONFIG["RIGHT_BUZZER"])

    entries['left_buzzer'].delete(0, tk.END)
    entries['left_buzzer'].insert(0, DEFAULT_CONFIG["LEFT_BUZZER"])

    entries['right_vibracall'].delete(0, tk.END)
    entries['right_vibracall'].insert(0, DEFAULT_CONFIG["RIGHT_VIBRACALL"])

    entries['left_vibracall'].delete(0, tk.END)
    entries['left_vibracall'].insert(0, DEFAULT_CONFIG["LEFT_VIBRACALL"])

    entries['right_push_button'].delete(0, tk.END)
    entries['right_push_button'].insert(0, DEFAULT_CONFIG["RIGHT_PUSH_BUTTON"])

    entries['left_push_button'].delete(0, tk.END)
    entries['left_push_button'].insert(0, DEFAULT_CONFIG["LEFT_PUSH_BUTTON"])

    entries['right_led'].delete(0, tk.END)
    entries['right_led'].insert(0, DEFAULT_CONFIG["RIGHT_LED"])

    entries['left_led'].delete(0, tk.END)
    entries['left_led'].insert(0, DEFAULT_CONFIG["LEFT_LED"])

    messagebox.showinfo("Reset", "As portas foram resetadas para o padrão.")


# Function for the ports configuration screen
def configure_ports():
    # Load the configuration
    config = load_config()
    entries = {}

    def save():
        # Collect the values entered by the user
        try:
            config["RIGHT_BUZZER"] = int(right_buzzer_entry.get())
            config["LEFT_BUZZER"] = int(left_buzzer_entry.get())
            config["RIGHT_VIBRACALL"] = int(right_vibracall_entry.get())
            config["LEFT_VIBRACALL"] = int(left_vibracall_entry.get())
            config["RIGHT_PUSH_BUTTON"] = int(right_push_button_entry.get())
            config["LEFT_PUSH_BUTTON"] = int(left_push_button_entry.get())
            config["RIGHT_LED"] = int(right_led_entry.get())
            config["LEFT_LED"] = int(left_led_entry.get())

            # Save the configuration to the file
            save_config(config)
            configure_window.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Por favor forneça um valor válido de porta.")

    # Function to close without saving
    def cancel():
        configure_window.destroy()

    # Create the configuration window
    configure_window = tk.Toplevel()
    configure_window.title("Configuração da portas do dispositivo")
    configure_window.geometry("400x400")
    configure_window.resizable(False, False)

    # Create a frame to hold the widgets in a grid layout
    grid_frame = ttk.Frame(configure_window)
    grid_frame.pack(pady=10)

    # Add a justified warning message centered in the window using Text widget
    warning_frame = ttk.Frame(configure_window)
    warning_frame.pack(pady=10)

    warning_text = tk.Text(warning_frame, wrap="word", height=2, width=35, font=("Arial", 12, "bold"), padx=10, pady=10)
    warning_text.insert("1.0",
                        "Atenção: Alterações incorretas nesta tela, podem causar mal funcionamento do dispositivo.")
    warning_text.config(state="disabled", background="yellow", foreground="red", font=("Arial", 12, "bold"))
    warning_text.pack()

    # Labels and entries for each port configuration (arranged in 2 columns)
    ttk.Label(grid_frame, text="Buzzer direito:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    right_buzzer_entry = ttk.Entry(grid_frame)
    right_buzzer_entry.grid(row=0, column=1, padx=5, pady=5)
    right_buzzer_entry.insert(0, config["RIGHT_BUZZER"])
    entries['right_buzzer'] = right_buzzer_entry

    ttk.Label(grid_frame, text="Buzzer esquerdo:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    left_buzzer_entry = ttk.Entry(grid_frame)
    left_buzzer_entry.grid(row=1, column=1, padx=5, pady=5)
    left_buzzer_entry.insert(0, config["LEFT_BUZZER"])
    entries['left_buzzer'] = left_buzzer_entry

    ttk.Label(grid_frame, text="Vibracall direito:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    right_vibracall_entry = ttk.Entry(grid_frame)
    right_vibracall_entry.grid(row=2, column=1, padx=5, pady=5)
    right_vibracall_entry.insert(0, config["RIGHT_VIBRACALL"])
    entries['right_vibracall'] = right_vibracall_entry

    ttk.Label(grid_frame, text="Vibracall esquerdo:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
    left_vibracall_entry = ttk.Entry(grid_frame)
    left_vibracall_entry.grid(row=3, column=1, padx=5, pady=5)
    left_vibracall_entry.insert(0, config["LEFT_VIBRACALL"])
    entries['left_vibracall'] = left_vibracall_entry

    ttk.Label(grid_frame, text="Push Button direito:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
    right_push_button_entry = ttk.Entry(grid_frame)
    right_push_button_entry.grid(row=4, column=1, padx=5, pady=5)
    right_push_button_entry.insert(0, config["RIGHT_PUSH_BUTTON"])
    entries['right_push_button'] = right_push_button_entry

    ttk.Label(grid_frame, text="Push Button esquerdo:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
    left_push_button_entry = ttk.Entry(grid_frame)
    left_push_button_entry.grid(row=5, column=1, padx=5, pady=5)
    left_push_button_entry.insert(0, config["LEFT_PUSH_BUTTON"])
    entries['left_push_button'] = left_push_button_entry

    ttk.Label(grid_frame, text="LED direito:").grid(row=6, column=0, padx=5, pady=5, sticky='w')
    right_led_entry = ttk.Entry(grid_frame)
    right_led_entry.grid(row=6, column=1, padx=5, pady=5)
    right_led_entry.insert(0, config["RIGHT_LED"])
    entries['right_led'] = right_led_entry

    ttk.Label(grid_frame, text="LED esquerdo:").grid(row=7, column=0, padx=5, pady=5, sticky='w')
    left_led_entry = ttk.Entry(grid_frame)
    left_led_entry.grid(row=7, column=1, padx=5, pady=5)
    left_led_entry.insert(0, config["LEFT_LED"])
    entries['left_led'] = left_led_entry

    # Save, Cancel, and Reset buttons
    button_frame = tk.Frame(configure_window)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text="Salvar", command=save).pack(side="left", padx=10)
    ttk.Button(button_frame, text="Cancelar", command=cancel).pack(side="left", padx=10)
    ttk.Button(button_frame, text="Resetar portas", command=lambda: reset_to_default(entries)).pack(side="left", padx=10)

    configure_window.mainloop()
