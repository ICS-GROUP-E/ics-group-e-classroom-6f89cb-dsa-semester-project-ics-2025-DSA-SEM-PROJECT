import unittest
from src.LinkedList import TaskLinkedList
class TestTaskLinkedList(unittest.TestCase):
    def test_insert_search(self):
        ll = TaskLinkedList()
        ll.insert("Task X")
        ll.insert("Task Y")
        self.assertTrue(ll.search("Task X"))
        self.assertFalse(ll.search("Task Z"))