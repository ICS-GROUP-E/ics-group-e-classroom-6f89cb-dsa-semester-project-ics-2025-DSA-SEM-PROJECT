from src.discharge import PatientDatabase, DischargeManager

# Initialize components
db = PatientDatabase('data/patients.json')
dm = DischargeManager()

# Test searching by name
results = db.search_by_name("Jane")
print("🔍 Search Results for 'Jane':")
for patient in results:
    print(patient)

# Discharge a patient
patient = db.search_by_id("P002")
if patient:
    dm.discharge(patient)
    print(f"\n✅ Discharged: {patient['name']}")

# Show recent discharges
print("\n🧾 Recent Discharges:")
for p in dm.get_recent_discharges():
    print(p["name"])