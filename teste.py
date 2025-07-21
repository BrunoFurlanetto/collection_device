import serial, time

# ajuste a porta para a sua, ex: 'COM5'
ser = serial.Serial('COM5', 115200, timeout=1)
time.sleep(0.1)
# envia Ctrl+B (0x02) para sair do raw REPL
ser.write(b'\x02')
ser.close()
