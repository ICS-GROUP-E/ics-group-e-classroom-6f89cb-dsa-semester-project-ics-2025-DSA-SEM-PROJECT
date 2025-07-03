import unittest
from src.linkedlist import StudentLinkedList

class TestStudentLinkedList(unittest.TestCase):
    def setUp(self):
        """
        Initialize a fresh linked list for each test
        """
        self.ll = StudentLinkedList()

        #Test data
        self.sample_students = [
            ("P001", "Alice", "Computer Science", 3.8),
            ("P002" , "Bob", "Engineering" , 3.2),
            ("P003" , "Charlie" , "Mathematics" , 3.5)
        ]
        for student in self.sample_students:
            self.ll.add_student(*student)

    # ---- CORE FUNCTIONALITY TESTS ----
    def test_initial_state(self):
        """
        Test setup creates correct initial state
        """
        self.assertEqual(self.ll.get_size(), 3)
        self.assertEqual(self.ll.search_student("P001")["name"], "Alice")

    def test_add_student(self):
        """
        Test adding new students
        """
        #Test normal addition
        self.ll.add_student("P004", "Diana", "Physics" , 3.9)
        self.assertEqual(self.ll.get_size(), 4)
        self.assertEqual(self.ll.search_student("P004")["gpa"] , 3.9)

        #Test duplicate ID
        with self.assertRaises(ValueError):
            self.ll.add_student("P001" , "Eve", "Biology", 3.7)

    def test_delete_student(self):
        """
        Test student deletion scenarios
        """
        #Delete head node
        self.assertTrue(self.ll.delete_student("P001"))
        self.assertEqual(self.ll.get_size(), 2)

        #Delete middle node
        self.assertTrue(self.ll.delete_student("P002"))

        #Delete last node
        self.assertTrue(self.ll.delete_student("P003"))
        self.assertEqual(self.ll.get_size(), 0)

        #Delete from empty list
        self.assertFalse(self.ll.delete_student("P001"))

    # ----- OPTIMIZED METHODS TEST -----
    def test_add_student_sorted(self):
        """
        Test GPA-sorted insertion
        """
        test_data = [
            ("P011" , "Eve", "Biology", 3.7),
            ("P012" , "Frank", "Chemistry", 4.0),
            ("P013" , "Grace", "Geology", 3.9),
        ]

        ll = StudentLinkedList()
        for student in test_data:
            ll.add_student_sorted(*student)

        #Verify order and integrity
        self.assertEqual(ll.head.student_id, "P012") #Highest GPA first
        self.assertEqual(ll.head.next.student_id, "P013")
        self.assertEqual(ll.head.next.next.student_id, "P011")
        self.assertEqual(ll.get_size(), 3)

    # ----- EDGE CASES -----
    def test_invalid_inputs(self):
        """
        Test handling of invalid inputs
        """
        with self.assertRaises(TypeError):
            self.ll.add_student(None, "Name", "Course" , 3.0) #None ID
        with self.assertRaises(TypeError):
            self.ll.add_student("P006" , 123, "Course", 3.0) #None-string name

        with self.assertRaises(ValueError):
            self.ll.add_student("P005" , "Name", "Course", -1.0) #Negative GPA
        with self.assertRaises(ValueError):
            self.ll.add_student("P007" , "Name", "Course", 4.1) #GPA > 4.0


    def test_display_all(self):
        """
        Test display output capture
        """
        from io import StringIO
        import sys

        #Creates a StringIO object to capture output
        captured_output = StringIO()

        #Save the original stdout
        original_stdout = sys.stdout

        try:
             # Redirect stdout to our StringIO object
             sys.stdout = captured_output

             #Call the method that prints
             self.ll.display_all()

             #Get the value from StringIO
             output = captured_output.getvalue()

             self.assertIn("Alice", output)
             self.assertIn("P001", output)
             self.assertIn("Computer Science", output)

        finally:
            #Restore the original stdout no matter what
            sys.stdout = original_stdout

if __name__ == "__main__":
    unittest.main(failfast=True) #Stop on first failure



