import sqlite3

class StudentDatabase:
    def __init__(self,db_name="students.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute()
        self.conn.commit()

    def add(self,student):
        self.cursor.execute((student.student_id,student.name,student.course,student.year,student.gpa))
        self.conn.commit()

    def remove(self,student_id):
        self.cursor.execute((student_id))
        self.conn.commit()

    def get(self,student_id):
        self.cursor.execute()
        return self.cursor.fetchall()