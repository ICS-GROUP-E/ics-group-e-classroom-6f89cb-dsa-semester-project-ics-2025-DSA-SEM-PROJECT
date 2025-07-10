# tests/test_bst.py
# by Gakenyi
import sys
import os
import pytest

# ✅ Add src/ds to the system path to allow import
current_dir = os.path.dirname(__file__)
ds_path = os.path.abspath(os.path.join(current_dir, '..', 'src', 'ds'))

print(f"Test current directory: {current_dir}")
print(f"DS path: {ds_path}")
print(f"BST file exists: {os.path.exists(os.path.join(ds_path, 'bst_doctorlookup.py'))}")

sys.path.insert(0, ds_path)

try:
    from bst_doctorlookup import Doctor, DoctorBST

    print("Successfully imported Doctor and DoctorBST for testing")
except ImportError as e:
    print(f"Import error in tests: {e}")
    raise


def test_insert_and_search():
    """Test inserting and searching for a doctor"""
    bst = DoctorBST()
    bst.insertDoctor(Doctor("Alice", "Cardiology"))
    result = bst.searchDoctor("Alice")
    assert result is not None
    assert result.name == "Alice"
    assert result.specialty == "Cardiology"


def test_search_nonexistent():
    """Test searching for a doctor that doesn't exist"""
    bst = DoctorBST()
    result = bst.searchDoctor("NonExistent")
    assert result is None


def test_update_doctor():
    """Test updating a doctor's specialty"""
    bst = DoctorBST()
    bst.insertDoctor(Doctor("Bob", "Surgery"))
    assert bst.updateDoctor("Bob", "Neurology") is True
    updated_doctor = bst.searchDoctor("Bob")
    assert updated_doctor.specialty == "Neurology"


def test_update_nonexistent_doctor():
    """Test updating a doctor that doesn't exist"""
    bst = DoctorBST()
    assert bst.updateDoctor("NonExistent", "Cardiology") is False


def test_delete_doctor():
    """Test deleting a doctor"""
    bst = DoctorBST()
    bst.insertDoctor(Doctor("Chris", "Dentistry"))
    # Verify doctor exists before deletion
    assert bst.searchDoctor("Chris") is not None
    # Delete the doctor
    bst.deleteDoctor("Chris")
    # Verify doctor no longer exists
    assert bst.searchDoctor("Chris") is None


def test_delete_nonexistent_doctor():
    """Test deleting a doctor that doesn't exist"""
    bst = DoctorBST()
    # This should not raise an error
    bst.deleteDoctor("NonExistent")
    assert bst.searchDoctor("NonExistent") is None


def test_inorder_traversal_sorted():
    """Test that inorder traversal returns doctors in alphabetical order"""
    bst = DoctorBST()
    bst.insertDoctor(Doctor("Zane", "Oncology"))
    bst.insertDoctor(Doctor("Aaron", "Pediatrics"))
    bst.insertDoctor(Doctor("Mike", "ENT"))

    doctors = bst.inorderTraversal()
    names = [doc.name for doc in doctors]
    assert names == sorted(names)
    assert len(names) == 3


def test_empty_bst():
    """Test operations on empty BST"""
    bst = DoctorBST()
    assert bst.searchDoctor("Anyone") is None
    assert bst.inorderTraversal() == []
    assert bst.updateDoctor("Anyone", "Anything") is False


def test_single_node_operations():
    """Test operations on BST with single node"""
    bst = DoctorBST()
    bst.insertDoctor(Doctor("Single", "Specialty"))

    # Test search
    result = bst.searchDoctor("Single")
    assert result is not None
    assert result.name == "Single"

    # Test traversal
    doctors = bst.inorderTraversal()
    assert len(doctors) == 1
    assert doctors[0].name == "Single"

    # Test update
    assert bst.updateDoctor("Single", "NewSpecialty") is True
    assert bst.searchDoctor("Single").specialty == "NewSpecialty"

    # Test delete
    bst.deleteDoctor("Single")
    assert bst.searchDoctor("Single") is None
    assert bst.inorderTraversal() == []


def test_multiple_operations():
    """Test multiple operations in sequence"""
    bst = DoctorBST()

    # Add multiple doctors
    doctors_to_add = [
        ("Alice", "Cardiology"),
        ("Bob", "Surgery"),
        ("Charlie", "Pediatrics"),
        ("Diana", "Neurology")
    ]

    for name, specialty in doctors_to_add:
        bst.insertDoctor(Doctor(name, specialty))

    # Verify all were added
    assert len(bst.inorderTraversal()) == 4

    # Update one
    assert bst.updateDoctor("Bob", "Orthopedics") is True
    assert bst.searchDoctor("Bob").specialty == "Orthopedics"

    # Delete one
    bst.deleteDoctor("Charlie")
    assert bst.searchDoctor("Charlie") is None
    assert len(bst.inorderTraversal()) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])