import os
from datetime import datetime
import cv2
from deepface import DeepFace

from app import gui
from app import database
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
            actions=['age', 'gender', 'emotion'],
            enforce_detection=False
        )

        age = analysis[0]['age']
        gender = analysis[0]['dominant_gender']
        emotion = analysis[0]['dominant_emotion']

        details = f"Age: {age} | Gender: {gender} | Emotion: {emotion}"

        # detect face region with cascade classifier to draw bounding box
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # draw bounding boxes around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(frame, details,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2)

        cv2.imwrite(filename, frame)
        gui.show_image(frame)

        gui.result_label.config(text=details)

        # add the intruder record to the database
        database.add_intruder_record(age, gender, emotion, filename)

    cap.release()

    gui.root.after(5000, gui.set_idle)
