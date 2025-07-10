# src/database/db_connection.py
#by Michelle
import sqlite3

DB_NAME = "doctors.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            name TEXT PRIMARY KEY,
            specialty TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_doctor_db(name, specialty):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO doctors (name, specialty) VALUES (?, ?)", (name, specialty))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def update_doctor_db(name, specialty):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE doctors SET specialty = ? WHERE name = ?", (specialty, name))
    conn.commit()
    conn.close()

def delete_doctor_db(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def fetch_all_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, specialty FROM doctors")
    data = cursor.fetchall()
    conn.close()
    return data
