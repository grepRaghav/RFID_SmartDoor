
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import csv
from app import database

# GUI setup
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

# state functions

def set_idle():
    status_frame.config(bg="#2d2d2d")
    status_label.config(text="System Ready for Scan", bg="#2d2d2d")


def set_valid():
    status_frame.config(bg="#1f7a1f")
    status_label.config(text="Access Granted - Opening Door...", bg="#1f7a1f")


def set_invalid():
    status_frame.config(bg="#8b0000")
    status_label.config(text="Access Denied - Intruder Detected!", bg="#8b0000")


# utility for showing a frame

def show_image(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    img = img.resize((650, 400))
    imgtk = ImageTk.PhotoImage(img)

    image_label.imgtk = imgtk
    image_label.configure(image=imgtk)


# --- Export to CSV functionality ---
def export_db_to_csv():
    records = database.get_all_intruders()
    if not records:
        messagebox.showinfo("Export", "No intruder records to export.")
        return

    # Ask user where to save the CSV
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save intruder records as CSV"
    )
    if not file_path:
        return

    # Write records to CSV
    headers = ["id", "timestamp", "age", "gender", "emotion", "image_path", "created_at"]
    try:
        with open(file_path, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for row in records:
                writer.writerow(row)
        messagebox.showinfo("Export", f"Exported {len(records)} records to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Failed", f"Could not export CSV: {e}")


# Add export button to GUI
export_btn = tk.Button(
    root,
    text="Export Intruder Log to CSV",
    font=("Helvetica", 12, "bold"),
    bg="#444",
    fg="white",
    command=export_db_to_csv
)
export_btn.pack(pady=10)
