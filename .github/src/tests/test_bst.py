# test_bst.py

import pytest
from bst_doctorlookup import Doctor, DoctorBST

def test_insert_and_search():
    bst = DoctorBST()
    bst.insertDoctor(Doctor("Alice", "Cardiology"))
    result = bst.searchDoctor("Alice")
    assert result is not None and result.specialty == "Cardiology"

def test_update_doctor():
    bst = DoctorBST()
    bst.insertDoctor(Doctor("Bob", "Surgery"))
    assert bst.updateDoctor("Bob", "Neurology") is True
    assert bst.searchDoctor("Bob").specialty == "Neurology"

def test_delete_doctor():
    bst = DoctorBST()
    bst.insertDoctor(Doctor("Chris", "Dentist"))
    bst.deleteDoctor("Chris")
    assert bst.searchDoctor("Chris") is None

def test_inorder_traversal():
    bst = DoctorBST()
    bst.insertDoctor(Doctor("Zane", "A"))
    bst.insertDoctor(Doctor("Mike", "B"))
    bst.insertDoctor(Doctor("Aaron", "C"))
    names = [doc.name for doc in bst.inorderTraversal()]
    assert names == sorted(names)
