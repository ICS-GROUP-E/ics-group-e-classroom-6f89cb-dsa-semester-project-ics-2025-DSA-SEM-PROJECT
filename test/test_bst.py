import unittest
from src.bst import TaskBST

class TestTaskBST(unittest.TestCase):
    def test_insert_search(self):
        bst = TaskBST()
        bst.insert(5, 1, "Medium priority task")
        bst.insert(10, 2, "High priority task")
        bst.insert(1, 3, "Low priority task")
        node = bst.search(10)
        self.assertIsNotNone(node)
        self.assertEqual(node.description, "High priority task")

    def test_inorder(self):
        bst = TaskBST()
        bst.insert(2, 1, "Task A")
        bst.insert(1, 2, "Task B")
        bst.insert(3, 3, "Task C")
        ordered = bst.inorder()
        self.assertEqual([t[0] for t in ordered], [1, 2, 3])