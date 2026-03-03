import serial
import cv2
from deepface import DeepFace
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
import threading

# ----------------------------
# CONFIG
# ----------------------------
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# ----------------------------
# GUI SETUP
# ----------------------------
root = tk.Tk()
root.title("AI Smart Door Security")
root.geometry("900x650")
root.configure(bg="#1e1e1e")

# Title
title_label = tk.Label(
    root,
    text="AI RFID Smart Door System",
    font=("Helvetica", 24, "bold"),
    fg="white",
    bg="#1e1e1e"
)
title_label.pack(pady=20)

# Status Frame
status_frame = tk.Frame(root, bg="#2d2d2d", width=700, height=100)
status_frame.pack(pady=20)

status_label = tk.Label(
    status_frame,
    text="System Ready for Scan",
    font=("Helvetica", 20, "bold"),
    fg="white",
    bg="#2d2d2d"
)
status_label.pack(expand=True)

# Image Display
image_label = tk.Label(root, bg="#1e1e1e")
image_label.pack(pady=20)

# AI Result Label
result_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 14),
    fg="white",
    bg="#1e1e1e"
)
result_label.pack(pady=10)


# ----------------------------
# GUI STATE FUNCTIONS
# ----------------------------
def set_idle():
    status_frame.config(bg="#2d2d2d")
    status_label.config(text="System Ready for Scan", bg="#2d2d2d")


def set_valid():
    status_frame.config(bg="#1f7a1f")
    status_label.config(text="Access Granted - Opening Door...", bg="#1f7a1f")


def set_invalid():
    status_frame.config(bg="#8b0000")
    status_label.config(text="Access Denied - Intruder Detected!", bg="#8b0000")


# ----------------------------
# IMAGE DISPLAY FUNCTION
# ----------------------------
def show_image(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    img = img.resize((650, 400))
    imgtk = ImageTk.PhotoImage(img)

    image_label.imgtk = imgtk
    image_label.configure(image=imgtk)


# ----------------------------
# AI + CAPTURE
# ----------------------------
def handle_intruder():
    set_invalid()

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"intruder_{timestamp}.jpg"

        analysis = DeepFace.analyze(
            img_path=frame,
            actions=['age', 'gender', 'race'],
            enforce_detection=False
        )

        age = analysis[0]['age']
        gender = analysis[0]['dominant_gender']
        race = analysis[0]['dominant_race']

        details = f"Age: {age} | Gender: {gender} | Race: {race}"

        cv2.putText(frame, details,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2)

        cv2.imwrite(filename, frame)
        show_image(frame)

        result_label.config(text=details)

    cap.release()

    root.after(5000, set_idle)


# ----------------------------
# SERIAL LISTENER
# ----------------------------
def serial_listener():
    while True:
        if ser.in_waiting > 0:
            message = ser.readline().decode().strip()
            print("Arduino:", message)

            if message == "VALID":
                set_valid()
                root.after(3000, set_idle)

            elif message == "INVALID":
                handle_intruder()


threading.Thread(target=serial_listener, daemon=True).start()

root.mainloop()
