import threading

from app import config
from app import gui
from app import capture


def serial_listener():
    if config.ser is None:
        print("Warning: serial port not initialized")
        return

    while True:
        if config.ser.in_waiting > 0:
            message = config.ser.readline().decode().strip()
            print("Arduino:", message)

            if message == "VALID":
                gui.set_valid()
                gui.root.after(3000, gui.set_idle)

            elif message == "INVALID":
                capture.handle_intruder()


def start_thread():
    thread = threading.Thread(target=serial_listener, daemon=True)
    thread.start()
    return thread
