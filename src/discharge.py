import json
import os

class PatientDatabase:
    def __init__(self, filepath='data/patients.json'):
        self.filepath = filepath
        self.patients = self.load_patients()

    def load_patients(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def save_patients(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.patients, f, indent=4)

    def search_by_id(self, patient_id):
        return next((p for p in self.patients if p['id'] == patient_id), None)

    def search_by_name(self, name):
        return [p for p in self.patients if name.lower() in p['name'].lower()]

class DischargeManager:
    def __init__(self):
        self.stack = []

    def discharge(self, patient):
        self.stack.append(patient)

    def get_recent_discharges(self, n=5):
        return self.stack[-n:]