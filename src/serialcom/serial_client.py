import serial
import threading
import time
import sys

class SerialClient:
    def __init__(self, port, baudrate=115200, timeout=1):
        """
        Initializes the serial client.
        :param port: Serial port (e.g., 'COM5' or '/dev/ttyUSB0')
        :param baudrate: Baud rate for the serial connection
        :param timeout: Read timeout in seconds
        """
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            # Give the connection a moment to initialize
            time.sleep(2)
        except serial.SerialException as e:
            print(f"Error opening serial port {port}: {e}")
            sys.exit(1)

    def send_command(self, command):
        """
        Sends a command string to the ESP32, appending a newline.
        :param command: Command string (without newline)
        """
        if not self.ser.is_open:
            raise serial.SerialException("Serial port is not open")
        cmd = command.strip() + "\n"
        self.ser.write(cmd.encode('utf-8'))

    def read_response(self):
        """
        Reads a line response from the ESP32.
        :return: Decoded response string (without newline)
        """
        if not self.ser.is_open:
            raise serial.SerialException("Serial port is not open")
        try:
            line = self.ser.readline()
            return line.decode('utf-8').strip()
        except Exception as e:
            print(f"Error reading from serial port: {e}")
            return None

    def send_and_receive(self, command, wait_for="\n", timeout=5):
        """
        Sends a command and waits for a response up to a timeout.
        :param command: Command string to send
        :param wait_for: Delimiter to wait for (default newline)
        :param timeout: Max time to wait in seconds
        :return: Response string or None
        """
        self.send_command(command)
        start = time.time()
        buffer = b""
        while time.time() - start < timeout:
            chunk = self.ser.read_until(wait_for.encode('utf-8'))
            buffer += chunk
            if wait_for.encode('utf-8') in chunk:
                break
        try:
            return buffer.decode('utf-8').strip()
        except:
            return None

    def close(self):
        """
        Closes the serial connection.
        """
        if self.ser.is_open:
            self.ser.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Serial client for ESP32 communication')
    parser.add_argument('--port', required=True, help='Serial port (e.g., COM5 or /dev/ttyUSB0)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate (default: 115200)')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Command to send, e.g.: START_TEST:Visual,Simple')
    args = parser.parse_args()

    client = SerialClient(args.port, baudrate=args.baud)
    if args.command:
        cmd = ' '.join(args.command)
        print(f"Sending command: {cmd}")
        client.send_command(cmd)
        resp = client.read_response()
        print(f"Response: {resp}")
    else:
        print("Entering interactive mode. Type commands and press enter. Ctrl+C to exit.")
        try:
            while True:
                cmd = input('> ')
                client.send_command(cmd)
                resp = client.read_response()
                print(f"Received: {resp}")
        except KeyboardInterrupt:
            print("Exiting interactive mode.")
    client.close()
