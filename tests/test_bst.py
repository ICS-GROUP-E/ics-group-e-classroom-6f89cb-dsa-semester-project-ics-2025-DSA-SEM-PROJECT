import pytest
from src.data_struct.Bsearch import BinarySearchTree
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def bst_populated():
    bst = BinarySearchTree()
    for key, value in [(8, 'x'), (3, 'y'), (10, 'z')]:
        bst.insert(key, value)
    return bst

def test_search_existing(bst_populated):
    assert bst_populated.search(10) == 'z'
    assert bst_populated.search(3) == 'y'
    assert bst_populated.search(99) is None

def test_delete_leaf(bst_populated):
    bst_populated.delete(3)
    keys = [k for k, _ in bst_populated.inorder()]
    assert keys == [8, 10]

def test_delete_two_children():
    bst = BinarySearchTree()
    for k in [5, 2, 8, 1, 3]:
        bst.insert(k, str(k))
    bst.delete(2)  # 2 has children 1 and 3
    assert bst.search(2) is None
    keys = [k for k, _ in bst.inorder()]
    assert keys == [1, 3, 5, 8]
