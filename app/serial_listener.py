import threading
import time

from app import config
from app import gui
from app import capture


def serial_listener():
    if config.ser is None:
        print("Warning: serial port not initialized")
        return

    while True:
        try:
            if config.ser.in_waiting > 0:
                message = config.ser.readline().decode(errors="ignore").strip()
                print("Arduino:", message)

                if message == "VALID":
                    gui.set_valid()
                    gui.root.after(3000, gui.set_idle)

                elif message == "INVALID":
                    capture.handle_intruder()

        except Exception as e:
            print("Serial error:", e)
            time.sleep(1)   # prevent CPU spinning


def start_thread():
    thread = threading.Thread(target=serial_listener, daemon=True)
    thread.start()
    return thread