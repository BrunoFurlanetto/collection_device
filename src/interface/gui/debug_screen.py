import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

import serial
import serial.tools.list_ports

from src.serialcom.serial_client import SerialClient


class DebugScreen:
    """
    Tela de debug do dispositivo ESP32.

    Permite testar individualmente os componentes do dispositivo (LEDs, buzzers,
    vibracalls e botoes) sem executar um protocolo completo de coleta.

    Usa SerialClient diretamente — nao usa ESPSerialClient.
    """

    def __init__(self, default_port: str):
        """
        Abre a janela Toplevel de debug com a porta pre-preenchida.

        :param default_port: Porta COM padrao vinda da tela inicial (ex: 'COM5').
        """
        self._client: SerialClient | None = None
        self._listen_thread: threading.Thread | None = None
        self._listen_active = threading.Event()

        # Estado interno de cada componente (True = ligado)
        self._component_state: dict[str, bool] = {
            "LED_R": False,
            "LED_L": False,
            "BUZ_R": False,
            "BUZ_L": False,
            "VIB_R": False,
            "VIB_L": False,
        }

        self._build_ui(default_port)

    # ── UI ──────────────────────────────────────────────────────────────────

    def _build_ui(self, default_port: str):
        """Constroi todos os widgets da janela."""
        self.window = tk.Toplevel()
        self.window.title("Debug do dispositivo")
        self.window.geometry("480x560")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.cleanup_and_close)

        # ── Porta e conexao ────────────────────────────────────────────────
        port_frame = ttk.LabelFrame(self.window, text="Conexao", padding=8)
        port_frame.pack(fill="x", padx=10, pady=6)

        ttk.Label(port_frame, text="Porta COM:").grid(row=0, column=0, sticky="w")
        self._port_var = tk.StringVar(value=default_port)
        self._port_entry = ttk.Entry(port_frame, textvariable=self._port_var, width=12)
        self._port_entry.grid(row=0, column=1, padx=6)

        ttk.Button(port_frame, text="Testar conexao", command=self.test_connection).grid(
            row=0, column=2, padx=4
        )
        ttk.Button(port_frame, text="Descobrir porta", command=self.discover_port).grid(
            row=0, column=3, padx=4
        )

        self._status_var = tk.StringVar(value="Nao conectado")
        self._status_label = ttk.Label(port_frame, textvariable=self._status_var, foreground="gray")
        self._status_label.grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 0))

        # ── LEDs ──────────────────────────────────────────────────────────
        led_frame = ttk.LabelFrame(self.window, text="LEDs", padding=8)
        led_frame.pack(fill="x", padx=10, pady=4)

        self._led_r_btn = ttk.Button(
            led_frame, text="LED Direito: OFF",
            command=lambda: self.toggle_component("LED", "R")
        )
        self._led_r_btn.grid(row=0, column=0, padx=8, pady=4)

        self._led_l_btn = ttk.Button(
            led_frame, text="LED Esquerdo: OFF",
            command=lambda: self.toggle_component("LED", "L")
        )
        self._led_l_btn.grid(row=0, column=1, padx=8, pady=4)

        # ── Buzzers ───────────────────────────────────────────────────────
        buz_frame = ttk.LabelFrame(self.window, text="Buzzers (500 Hz)", padding=8)
        buz_frame.pack(fill="x", padx=10, pady=4)

        self._buz_r_btn = ttk.Button(
            buz_frame, text="Buzzer Direito: OFF",
            command=lambda: self.toggle_component("BUZ", "R")
        )
        self._buz_r_btn.grid(row=0, column=0, padx=8, pady=4)

        self._buz_l_btn = ttk.Button(
            buz_frame, text="Buzzer Esquerdo: OFF",
            command=lambda: self.toggle_component("BUZ", "L")
        )
        self._buz_l_btn.grid(row=0, column=1, padx=8, pady=4)

        # ── Vibracalls ────────────────────────────────────────────────────
        vib_frame = ttk.LabelFrame(self.window, text="Vibracalls", padding=8)
        vib_frame.pack(fill="x", padx=10, pady=4)

        self._vib_r_btn = ttk.Button(
            vib_frame, text="Vibracall Direito: OFF",
            command=lambda: self.toggle_component("VIB", "R")
        )
        self._vib_r_btn.grid(row=0, column=0, padx=8, pady=4)

        self._vib_l_btn = ttk.Button(
            vib_frame, text="Vibracall Esquerdo: OFF",
            command=lambda: self.toggle_component("VIB", "L")
        )
        self._vib_l_btn.grid(row=0, column=1, padx=8, pady=4)

        # ── Botoes ────────────────────────────────────────────────────────
        btn_frame = ttk.LabelFrame(self.window, text="Botoes Push", padding=8)
        btn_frame.pack(fill="x", padx=10, pady=4)

        self._listen_start_btn = ttk.Button(
            btn_frame, text="Iniciar escuta", command=self.start_button_listen
        )
        self._listen_start_btn.grid(row=0, column=0, padx=8, pady=4)

        self._listen_stop_btn = ttk.Button(
            btn_frame, text="Parar escuta", command=self.stop_button_listen,
            state="disabled"
        )
        self._listen_stop_btn.grid(row=0, column=1, padx=8, pady=4)

        self._btn_indicator = ttk.Label(btn_frame, text="Aguardando...", foreground="gray")
        self._btn_indicator.grid(row=1, column=0, columnspan=2, pady=(4, 0))

        # ── Fechar ────────────────────────────────────────────────────────
        close_frame = ttk.Frame(self.window, padding=8)
        close_frame.pack(fill="x", padx=10, pady=6)

        ttk.Button(close_frame, text="Fechar", command=self.cleanup_and_close).pack(side="right")

    # ── Mapa de botoes por componente ────────────────────────────────────────

    def _get_toggle_button(self, component: str, side: str) -> ttk.Button | None:
        key = f"{component}_{side}"
        mapping = {
            "LED_R": self._led_r_btn,
            "LED_L": self._led_l_btn,
            "BUZ_R": self._buz_r_btn,
            "BUZ_L": self._buz_l_btn,
            "VIB_R": self._vib_r_btn,
            "VIB_L": self._vib_l_btn,
        }
        return mapping.get(key)

    def _component_label(self, component: str, side: str) -> str:
        names = {
            "LED": "LED",
            "BUZ": "Buzzer",
            "VIB": "Vibracall",
        }
        sides = {"R": "Direito", "L": "Esquerdo"}
        return f"{names.get(component, component)} {sides.get(side, side)}"

    # ── Conexao ──────────────────────────────────────────────────────────────

    def _open_connection(self, port: str, timeout: float = 1.0) -> bool:
        """
        Abre conexao serial na porta indicada.

        :param port: Nome da porta (ex: 'COM5').
        :param timeout: Timeout de leitura em segundos.
        :return: True se abriu com sucesso, False caso contrario.
        """
        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None

        try:
            self._client = SerialClient(port, baudrate=115200, timeout=timeout)
            return True
        except SystemExit:
            # SerialClient chama sys.exit(1) em falha — capturamos aqui
            self._client = None
            return False
        except serial.SerialException as exc:
            err = str(exc).lower()
            if "in use" in err or "access is denied" in err or "permiss" in err:
                self._set_status("Porta em uso por outro programa", "red")
            else:
                self._set_status(f"Falha na conexao: {exc}", "red")
            self._client = None
            return False
        except Exception as exc:
            self._set_status(f"Falha na conexao: {exc}", "red")
            self._client = None
            return False

    def _set_status(self, message: str, color: str = "black"):
        self._status_var.set(message)
        self._status_label.config(foreground=color)

    def _disable_toggles(self):
        """Desabilita todos os botoes de toggle (conexao perdida)."""
        for btn in (
            self._led_r_btn, self._led_l_btn,
            self._buz_r_btn, self._buz_l_btn,
            self._vib_r_btn, self._vib_l_btn,
        ):
            btn.config(state="disabled")

    def _enable_toggles(self):
        """Habilita todos os botoes de toggle."""
        for btn in (
            self._led_r_btn, self._led_l_btn,
            self._buz_r_btn, self._buz_l_btn,
            self._vib_r_btn, self._vib_l_btn,
        ):
            btn.config(state="normal")

    # ── Metodos publicos ─────────────────────────────────────────────────────

    def test_connection(self) -> None:
        """
        Envia PING ao ESP32 e aguarda PONG com timeout de 3 segundos.
        Exibe resultado na label de status.
        """
        port = self._port_var.get().strip()
        if not port:
            self._set_status("Informe a porta antes de testar.", "orange")
            return

        self._set_status("Testando conexao...", "gray")
        self.window.update_idletasks()

        if not self._open_connection(port, timeout=3.0):
            # _open_connection ja atualizou o status em caso de erro serial;
            # tratamos aqui somente o caso de porta nao encontrada
            if self._client is None and "em uso" not in self._status_var.get():
                self._set_status("Falha na conexao: porta nao encontrada", "red")
            return

        try:
            response = self._client.send_and_receive("PING", timeout=3)
            if response == "PONG":
                self._set_status("Conexao OK", "green")
                self._enable_toggles()
            else:
                self._set_status(
                    f"Sem resposta do ESP32 (recebido: '{response}')", "red"
                )
                self._disable_toggles()
        except serial.SerialException as exc:
            self._set_status(f"Conexao perdida: {exc}", "red")
            self._client = None
            self._disable_toggles()
        except Exception as exc:
            self._set_status(f"Erro: {exc}", "red")
            self._disable_toggles()

    def toggle_component(self, component: str, side: str) -> None:
        """
        Alterna o estado de um componente (LED, BUZ ou VIB) no lado indicado.

        :param component: 'LED', 'BUZ' ou 'VIB'.
        :param side: 'R' (direito) ou 'L' (esquerdo).
        """
        if self._client is None:
            messagebox.showwarning(
                "Sem conexao",
                "Teste a conexao com o dispositivo antes de usar os controles.",
                parent=self.window,
            )
            return

        key = f"{component}_{side}"
        current_state = self._component_state.get(key, False)
        new_state = not current_state
        command = f"D:{component}_{side}:{'ON' if new_state else 'OFF'}"
        label = self._component_label(component, side)
        btn = self._get_toggle_button(component, side)

        try:
            response = self._client.send_and_receive(command, timeout=3)
        except serial.SerialException as exc:
            self._set_status(f"Conexao perdida: {exc}", "red")
            self._client = None
            self._disable_toggles()
            return
        except Exception as exc:
            self._set_status(f"Erro ao enviar comando: {exc}", "red")
            return

        if response == "OK":
            self._component_state[key] = new_state
            state_label = "ON" if new_state else "OFF"
            if btn:
                btn.config(text=f"{label}: {state_label}")
        else:
            # Timeout ou resposta inesperada — reverte ao estado anterior
            self._set_status(
                f"Timeout: {label} nao respondeu. Estado revertido.", "red"
            )

    def start_button_listen(self) -> None:
        """
        Envia D:BTN:LISTEN e inicia thread de leitura de eventos BTN:R / BTN:L.
        """
        if self._client is None:
            messagebox.showwarning(
                "Sem conexao",
                "Teste a conexao com o dispositivo antes de iniciar a escuta.",
                parent=self.window,
            )
            return

        if self._listen_active.is_set():
            return  # ja em escuta

        try:
            self._client.send_command("D:BTN:LISTEN")
        except serial.SerialException as exc:
            self._set_status(f"Conexao perdida: {exc}", "red")
            self._client = None
            self._disable_toggles()
            return
        except Exception as exc:
            self._set_status(f"Erro ao iniciar escuta: {exc}", "red")
            return

        self._listen_active.set()
        self._listen_start_btn.config(state="disabled")
        self._listen_stop_btn.config(state="normal")
        self._btn_indicator.config(text="Escutando...", foreground="blue")

        self._listen_thread = threading.Thread(
            target=self._button_listen_loop, daemon=True
        )
        self._listen_thread.start()

    def stop_button_listen(self) -> None:
        """
        Envia D:BTN:STOP e encerra a thread de escuta de botoes.
        """
        if not self._listen_active.is_set():
            return

        self._listen_active.clear()

        if self._client is not None:
            try:
                self._client.send_command("D:BTN:STOP")
            except Exception:
                pass

        self._listen_start_btn.config(state="normal")
        self._listen_stop_btn.config(state="disabled")
        self._btn_indicator.config(text="Escuta parada.", foreground="gray")

    def _button_listen_loop(self):
        """
        Thread de leitura de eventos BTN:R / BTN:L enquanto escuta ativa.
        Atualiza o indicador visual via after() para thread-safety.
        """
        while self._listen_active.is_set():
            try:
                if self._client is None:
                    break
                line = self._client.read_response()
                if line in ("BTN:R", "BTN:L"):
                    side = "Direito" if line == "BTN:R" else "Esquerdo"
                    self.window.after(
                        0,
                        lambda s=side: self._btn_indicator.config(
                            text=f"Botao {s} pressionado!", foreground="green"
                        ),
                    )
                elif line == "LISTEN:STOP":
                    break
            except serial.SerialException:
                self.window.after(
                    0,
                    lambda: self._set_status("Conexao perdida durante escuta.", "red"),
                )
                self.window.after(0, self._disable_toggles)
                self._client = None
                break
            except Exception:
                break

        self._listen_active.clear()
        self.window.after(
            0,
            lambda: self._listen_start_btn.config(state="normal"),
        )
        self.window.after(
            0,
            lambda: self._listen_stop_btn.config(state="disabled"),
        )

    def discover_port(self) -> None:
        """
        Varre todas as portas COM disponiveis, envia PING a cada uma (timeout 1s)
        e exibe o resultado.

        - Nenhum dispositivo: mensagem de erro.
        - Um dispositivo: preenche o campo de porta automaticamente.
        - Varios dispositivos: exibe lista para selecao.
        """
        self._set_status("Varrendo portas COM...", "gray")
        self.window.update_idletasks()

        available = [p.device for p in serial.tools.list_ports.comports()]
        if not available:
            self._set_status(
                "Nenhum dispositivo ESP32 encontrado nas portas disponiveis", "red"
            )
            return

        found = []
        for port in available:
            try:
                client = SerialClient(port, baudrate=115200, timeout=1)
                response = client.send_and_receive("PING", timeout=1)
                client.close()
                if response == "PONG":
                    found.append(port)
            except SystemExit:
                pass
            except Exception:
                pass

        if not found:
            self._set_status(
                "Nenhum dispositivo ESP32 encontrado nas portas disponiveis", "red"
            )
        elif len(found) == 1:
            self._port_var.set(found[0])
            self._set_status(f"ESP32 encontrado em {found[0]}", "green")
        else:
            self._show_port_selection(found)

    def _show_port_selection(self, ports: list[str]):
        """Exibe janela de selecao quando multiplos ESP32 sao encontrados."""
        sel_win = tk.Toplevel(self.window)
        sel_win.title("Selecionar porta")
        sel_win.geometry("280x180")
        sel_win.resizable(False, False)
        sel_win.grab_set()

        ttk.Label(sel_win, text="Multiplos dispositivos encontrados.\nSelecione a porta:").pack(
            pady=10
        )

        port_var = tk.StringVar(value=ports[0])
        for p in ports:
            ttk.Radiobutton(sel_win, text=p, variable=port_var, value=p).pack(anchor="w", padx=20)

        def confirm():
            self._port_var.set(port_var.get())
            self._set_status(f"Porta selecionada: {port_var.get()}", "green")
            sel_win.destroy()

        ttk.Button(sel_win, text="Confirmar", command=confirm).pack(pady=10)

    def cleanup_and_close(self) -> None:
        """
        Para escuta ativa, envia D:RESET, fecha conexao serial e destroi a janela.
        """
        # Para thread de escuta se estiver ativa
        if self._listen_active.is_set():
            self._listen_active.clear()

        # Envia D:RESET ao dispositivo
        if self._client is not None:
            try:
                self._client.send_and_receive("D:RESET", timeout=3)
            except Exception:
                pass
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None

        self.window.destroy()
