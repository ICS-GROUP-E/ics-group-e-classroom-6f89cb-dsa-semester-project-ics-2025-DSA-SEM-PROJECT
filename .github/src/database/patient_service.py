from database.db_connection import get_connection

class PatientService:

    @staticmethod
    def add_patient(name, priority):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patients (name, priority) VALUES (?, ?)",
            (name, priority)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_patients():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, priority, timestamp FROM patients ORDER BY priority ASC, timestamp ASC"
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete_patient_by_id(patient_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def clear_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients")
        conn.commit()
        conn.close()
