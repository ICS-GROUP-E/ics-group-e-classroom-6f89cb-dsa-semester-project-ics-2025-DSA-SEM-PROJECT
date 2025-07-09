import unittest
import sys
import os

# Add 'src' to the system path so we can import modules correctly
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ds.priorityqueue import PriorityQueue


class TestPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.queue = PriorityQueue()

    def test_insert_single_patient(self):
        self.queue.insert("Alice", 3)
        patients = self.queue.list_patients()
        self.assertEqual(patients, ["Alice (Priority 3)"])

    def test_insert_multiple_patients_sorted(self):
        self.queue.insert("Alice", 3)
        self.queue.insert("Bob", 1)
        self.queue.insert("Claire", 2)
        self.assertEqual(
            self.queue.list_patients(),
            ["Bob (Priority 1)", "Alice (Priority 3)", "Claire (Priority 2)"]
        )

    def test_remove_highest_priority(self):
        self.queue.insert("Alice", 3)
        self.queue.insert("Bob", 1)
        self.queue.insert("Claire", 2)

        top_patient = self.queue.remove_highest_priority()
        self.assertEqual(top_patient.name, "Bob")  # ✅ Check the name of the returned patient

        remaining = self.queue.list_patients()
        self.assertEqual(remaining, ["Claire (Priority 2)", "Alice (Priority 3)"])

    def test_stability_for_equal_priority(self):
        self.queue.insert("Alice", 1)
        self.queue.insert("Bob", 1)
        self.queue.insert("Claire", 1)

        # Remove all patients in order and check insertion order is preserved
        names = [self.queue.remove_highest_priority().name for _ in range(3)]
        self.assertEqual(names, ["Alice", "Bob", "Claire"])

    def test_remove_from_empty_queue(self):
        result = self.queue.remove_highest_priority()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
