import unittest
from src.Graph import TaskGraph
class TestTaskGraph(unittest.TestCase):
    def test_topological_sort(self):
        graph = TaskGraph()
        graph.add_task("Task A")
        graph.add_task("Task B")
        graph.add_task("Task C")
        graph.add_dependency("Task C", "Task B")
        graph.add_dependency("Task B", "Task A")
        order = graph.topological_sort()
        self.assertTrue(order.index("Task A") < order.index("Task B") < order.index("Task C"))