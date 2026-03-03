import os
from datetime import datetime
import cv2
from deepface import DeepFace

from app import gui


def handle_intruder():
    """Capture a frame, analyze it with DeepFace, overlay details, and update the GUI."""

    gui.set_invalid()

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # ensure the images directory inside the project exists
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        images_dir = os.path.join(base_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        filename = os.path.join(images_dir, f"intruder_{timestamp}.jpg")

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
        gui.show_image(frame)

        gui.result_label.config(text=details)

    cap.release()

    gui.root.after(5000, gui.set_idle)
