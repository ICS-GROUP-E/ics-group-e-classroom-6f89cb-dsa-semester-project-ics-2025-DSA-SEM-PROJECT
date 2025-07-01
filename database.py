import sqlite3
from model.student import Student  # Make sure this import exists

class StudentDatabase:
    def __init__(self, db_name="students.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT,
                course TEXT,
                year INTEGER,
                gpa REAL
            )
        """)
        self.conn.commit()

    def add(self, student):

        self.cursor.execute(
            "INSERT OR REPLACE INTO students (id, name, course, year, gpa) VALUES (?, ?, ?, ?, ?)",
            (student.student_id, student.name, student.course, student.year, student.gpa)
        )
        self.conn.commit()

    def remove(self, student_id):

        self.cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )
        self.conn.commit()

    def get(self, student_id):

        self.cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )
        row = self.cursor.fetchone()
        if row:
            return Student(*row)  # Reconstruct the Student object
        return None

    def list_all(self):

        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()
