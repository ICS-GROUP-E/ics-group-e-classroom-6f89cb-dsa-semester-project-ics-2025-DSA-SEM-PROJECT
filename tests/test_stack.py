import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from datastructure.stack import ActionStack
from model.student import Student



class TestActionStack(unittest.TestCase):
    def setUp(self):
        self.stack = ActionStack()
        self.student = Student("001", "Derrick", "Computer Science", 2, 3.7)

    def test_push(self):
        self.stack.push("delete", self.student)
        self.assertEqual(len(self.stack.stack), 1)
        self.assertEqual(self.stack.stack[-1][1].name, "Derrick")

    def test_pop(self):
        self.stack.push("delete", self.student)
        action_type, student = self.stack.pop()
        self.assertEqual(action_type, "delete")
        self.assertEqual(student.student_id, "001")
        self.assertTrue(self.stack.is_empty())

    def test_pop_empty(self):
        self.assertIsNone(self.stack.pop())

    def test_peek(self):
        self.stack.push("delete", self.student)
        action_type, student = self.stack.peek()
        self.assertEqual(action_type, "delete")
        self.assertEqual(student.name, "Derrick")
        self.assertFalse(self.stack.is_empty())

    def test_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.stack.push("delete", self.student)
        self.assertFalse(self.stack.is_empty())

    def test_clear(self):
        self.stack.push("delete", self.student)
        self.stack.clear()
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(len(self.stack.stack), 0)

if __name__ == '__main__':
    unittest.main()
