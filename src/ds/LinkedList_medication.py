from src.database.db_connection import get_connection

class MedicationNode:
    def __init__(self, med_name, dosage, date):
        self.med_name = med_name
        self.dosage = dosage
        self.date = date
        self.next = None

class MedicationHistory:
    def __init__(self):
        self.head = None

    def addMedication(self, patient_id, med_name, dosage, date):
        new_node = MedicationNode(med_name, dosage, date)
        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medication_history(patient_id, med_name, dosage, date) VALUES (?, ?, ?, ?)",
                       (patient_id, med_name, dosage, date))
        conn.commit()
        conn.close()
        print(f"[LOG] Medication added for {patient_id}: {med_name}")

    def deleteMedication(self, patient_id, med_name):
        previous_node = None
        current_node = self.head
        while current_node:
            if current_node.med_name == med_name:
                if previous_node:
                    previous_node.next = current_node.next
                else:
                    self.head = current_node.next
                break
            previous_node = current_node
            current_node = current_node.next

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medication_history WHERE patient_id = ? AND med_name=?",
                       (patient_id, med_name))
        conn.commit()
        conn.close()
        print(f"[LOG] Medication '{med_name}' deleted for {patient_id}")

    def showMedicationHistory(self, patient_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        if patient_id:
            cursor.execute("SELECT patient_id, med_name, dosage, date FROM medication_history WHERE patient_id = ?",
                           (patient_id,))
        else:
            cursor.execute("SELECT patient_id, med_name, dosage, date FROM medication_history")

        rows = cursor.fetchall()
        conn.close()

        if patient_id:
            print(f"[LOG] Medication History for {patient_id}:")
        else:
            print(f"[LOG] Full Medication History:")

        for row in rows:
            print(f" - Patient: {row[0]}, {row[1]} ({row[2]}) on {row[3]}")
        return rows

