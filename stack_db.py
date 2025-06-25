import sqlite3

# Stack to track deleted students (for undo)
undo_stack = []

# --- SQLite: Save Student ---
def save_to_db(student):
    """
    Save a student record to the database (no year).
    """
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT,
            course TEXT,
            gpa REAL
        )
    ''')

    cursor.execute('INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?)', (
        student['id'], student['name'], student['course'], student['gpa']
    ))

    conn.commit()
    conn.close()
    print(f"[Saved] {student['id']} - {student['name']}")


# --- SQLite: Delete Student ---
def delete_from_db(student_id):
    """
    Delete a student from the database and push to undo stack.
    """
    student = fetch_student(student_id)
    if student:
        push_undo(student)
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        print(f"[Deleted] {student_id}")
        return True
    else:
        print("[Error] Student not found.")
        return False


# --- SQLite: Fetch Student ---
def fetch_student(student_id):
    """
    Return a tuple (id, name, course, gpa)
    """
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student


# --- Stack: Push Undo ---
def push_undo(student):
    """
    Add a deleted student to the undo stack.
    'student' is a tuple (id, name, course, gpa)
    """
    undo_stack.append(student)
    print(f"[Undo Log] Saved: {student[0]}")


# --- Stack: Pop Undo ---
def pop_undo():
    """
    Restore the most recently deleted student.
    """
    if not undo_stack:
        print("[Undo] Nothing to undo.")
        return

    student = undo_stack.pop()
    student_dict = {
        'id': student[0],
        'name': student[1],
        'course': student[2],
        'gpa': student[3]
    }
    save_to_db(student_dict)
    print(f"[Undo] Restored student: {student[0]}")
    return student_dict  # optionally return the restored student
