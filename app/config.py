import serial

# config constants
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
except Exception:
    ser = None  # caller should handle situations where serial isn't available
