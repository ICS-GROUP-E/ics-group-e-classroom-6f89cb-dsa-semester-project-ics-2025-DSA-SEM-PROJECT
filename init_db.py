# init_db.py
from src.database.db_connection import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medication_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            med_name TEXT,
            dosage TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ medication_history table created!")

init_db()
