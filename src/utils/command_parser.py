"""
Simple command parser for ESP32 (MicroPython)
Receives a command string and returns (via, tipo) tuple.
"""


def parse_command(command: str):
    """
    Parse a serial command of format:
        <COMMAND>:<via>,<tipo>
    e.g.:
        START_TEST:Visual,Simple
        START_FAMILIARIZATION:Auditory,Choice
    Returns:
        (via, tipo) on success, or (None, None) if parsing fails.
    """
    try:
        # Strip whitespace and split on first ':'
        _, params = command.strip().split(':', 1)
        # Split the parameters on first ','
        via, tipo = params.split(',', 1)
        return via, tipo
    except Exception:
        return None, None

# Example usage in ESP main loop:
# uart = machine.UART(0, 115200)
# while True:
#     if uart.any():
#         line = uart.readline().decode('utf-8').strip()
#         via, tipo = parse_command(line)
#         if via and tipo:
#             uart.write(f"PARSED:{via},{tipo}\n")
#         else:
#             uart.write("ERROR:INVALID_COMMAND\n")
