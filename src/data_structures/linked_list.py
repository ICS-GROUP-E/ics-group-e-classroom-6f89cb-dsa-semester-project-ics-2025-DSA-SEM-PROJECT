"""
Linked List implementation for task management.
Each event can have a linked list of tasks.
"""

class LLNode:
    def __init__(self, data: str, completed: bool = False):
        """
        Initializes a linked list node for task management.
        :param data: The task description.
        :param completed: Boolean indicating if the task is completed.
        """
        self.data = data
        self.completed = completed
        self.next = None
