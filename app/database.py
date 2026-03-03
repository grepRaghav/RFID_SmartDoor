"""Database module for storing intruder records."""

import sqlite3
import os
from datetime import datetime


def get_db_path():
    """Get the path to the intruders database."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.join(logs_dir, "intruders.db")


def init_db():
    """Initialize the database with the intruders table if it doesn't exist."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intruders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            emotion TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def add_intruder_record(age, gender, emotion, image_path):
    """Add an intruder record to the database.
    
    Args:
        age: Detected age of the intruder
        gender: Detected gender of the intruder
        emotion: Detected emotion of the intruder
        image_path: Path to the captured image
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO intruders (timestamp, age, gender, emotion, image_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, age, gender, emotion, image_path))

    conn.commit()
    conn.close()


def get_all_intruders():
    """Retrieve all intruder records from the database.
    
    Returns:
        List of tuples containing intruder records
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM intruders ORDER BY timestamp DESC')
    records = cursor.fetchall()

    conn.close()
    return records
