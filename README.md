# RFID Smart Door 🚪🔐

This is an **AI-enabled RFID Smart Door Security System** built using an **Arduino** with an **RFID reader** and a **Python GUI application** for intelligent monitoring and access control.

When an RFID tag is scanned, the Arduino checks if it matches an authorized tag. If valid, it unlocks a servo-controlled door. If invalid, the system captures an intruder image and analyzes it using DeepFace (face age, gender, race estimation).
## 🧠 Features

- 🔑 **RFID Access Control:**  
  Reads RFID tags using an RC522 reader and validates against an authorized UID. 

- 🤖 **AI Intruder Detection:**  
  On invalid scans, the system captures an image and analyzes the face using DeepFace (age, gender, race). 

- 💻 **GUI Dashboard:**  
  Python Tkinter app displays status (“Access Granted” or “Access Denied”) and shows captured images. 

---

## 📁 Project Structure

```
RFID_SmartDoor/
├── arduino/
│ └── sketch_mar3a/
│ └── sketch_mar3a.ino ← Arduino code for RFID & Door Servo
├── app/
│ └── main.py ← Python GUI + AI logic
├── requirements.txt ← Python dependencies
```

---

## 🛠️ Hardware Requirements

- Arduino board (e.g., Uno)
- RFID RC522 module (MFRC522)
- RFID tags/cards
- Servo motor (for door lock)
- USB cable for Arduino-PC connection

---

## 💾 Software Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```
Note: The requirements include DeepFace, OpenCV, and other packages used in the Python app.

## ▶️ How to Use

1. Connect the RFID reader to the Arduino and upload sketch_mar3a.ino using Arduino IDE.

2. Connect the servo to control door opening on a valid tag.

3. Run the Python app:

```python
python app/main.py
```

3. The GUI starts and waits for serial data from Arduino.

4. Scan RFID cards:

    - If the tag matches the authorized UID → Door opens.

    - If invalid → Captures intruder image and performs face analysis.

## 📌 Notes

- Update the authorized UID in sketch_mar3a.ino with your own card’s UID.
- Modify the SERIAL_PORT in app/main.py to match your system’s USB port.
