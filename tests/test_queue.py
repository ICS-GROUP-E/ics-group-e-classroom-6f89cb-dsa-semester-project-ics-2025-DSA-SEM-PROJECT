import unittest
from src.queue import NotificationQueue

class TestNotificationQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        q = NotificationQueue()
        q.enqueue("Alert 1")
        q.enqueue("Alert 2")
        self.assertEqual(q.dequeue(), "Alert 1")
        self.assertEqual(q.dequeue(), "Alert 2")

