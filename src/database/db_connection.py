import sqlite3
import os

def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "../../hospital.db")
    return sqlite3.connect(os.path.abspath(db_path))
