import json
import time
import serial

from src.interface.gui.temp_messages import TempAlert


class ESPSerialClient:
    """
    Client for sending commands to ESP32 over serial and waiting for responses.
    """
    def __init__(self, config_path='src/config/session_config.json', baud=115200):
        """
        :param config_path: Path to the JSON file with 'PORT' key.
        :param baud: Baud rate for the serial connection.
        """
        self.baud = baud
        self.port = self._load_port(config_path)
        self.ser = None

    @staticmethod
    def _load_port(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            return cfg['PORT']
        except Exception as e:
            raise RuntimeError(f"Failed to load port from {config_path}: {e}")

    def open(self):
        """Open the serial connection."""
        if self.ser and self.ser.is_open:

            return
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baud, timeout=1)
            time.sleep(2)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        except serial.SerialException as e:
            raise RuntimeError(f"Unable to open serial port {self.port}: {e}")

    def close(self):
        """Close the serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_command_and_wait(self, master, command, success_resp='SUCCESS', retry_on_unknown=True, max_retries=5, read_interval=0.1):
        """
        Send a command to the ESP and wait for a specific success response.

        :param command: Command string (no newline appended).
        :param success_resp: The response indicating success.
        :param retry_on_unknown: If True, retry command when receiving UNKNOWN_COMMAND.
        :param max_retries: Max number of retries on unknown command.
        :param read_interval: Delay between read attempts.
        :return: (successful, list_of_responses)
        """
        if not self.ser or not self.ser.is_open:
            self.open()

        responses = []
        retries = 0
        cmd = command.strip()

        # send first time
        self.ser.write(cmd.encode('utf-8'))
        self.ser.flush()

        while True:
            line = self.ser.readline().decode('utf-8', errors='ignore').strip()

            if line:
                if retry_on_unknown and line == 'ERROR:UNKNOWN_COMMAND':
                    retries += 1

                    if retries > max_retries:

                        break
                    # retry sending
                    self.ser.write(cmd.encode('utf-8'))
                    self.ser.flush()
                    time.sleep(read_interval)

                    continue
                else:
                    responses.append(line)

                    if line == success_resp:
                        return True, responses

                    TempAlert(master, line)
            else:
                time.sleep(read_interval)

        return False, responses


def soft_reset_esp():
    """
    Envia Ctrl-D para forçar um soft reboot do MicroPython no ESP32.
    Funciona porque no REPL o Ctrl-D faz um soft reset.
    """
    with open('src/config/session_config.json', 'r', encoding='utf-8') as f:
        session = json.load(f)

    port = session.get('PORT')
    ser = serial.Serial(port, baudrate=115200, timeout=1)
    time.sleep(0.1)  # deixa a porta estabilizar
    ser.write(b'\x04')  # Ctrl-D
    ser.flush()
    ser.close()
