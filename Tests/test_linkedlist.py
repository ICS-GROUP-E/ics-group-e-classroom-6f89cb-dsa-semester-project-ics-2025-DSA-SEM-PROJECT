from src.ds.LinkedList_medication import MedicationHistory

def test_add_medication():
    med = MedicationHistory()
    med.addMedication("P001", "Paracetamol", "500mg", "2025-07-10")
    history = med.showHistory("P001")
    assert any("Paracetamol" in h for h in [x[0] for x in history])
