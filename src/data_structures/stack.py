"""
Stack implementation for edit history (undo functionality).
Stores recently edited events for undo operations.
"""

class EventStack:
    def __init__(self, max_size: int = 10):
        """
        Initialize the stack with a maximum size.
        :param max_size: Maximum number of items to store in the stack.
        """
        self.items = []
        self.max_size = max_size
    
    def push(self, item):
        """
        Push an item onto the stack.
        If stack is full, remove the oldest item first.
        """
        if len(self.items) >= self.max_size:
            self.items.pop(0)  # Remove oldest item
        self.items.append(item)
    
    def pop(self):
        """
        Pop the most recent item from the stack.
        :return: The most recent item, or None if stack is empty.
        """
        if self.items:
            return self.items.pop()
        return None
    
    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.items) == 0
    
    def size(self):
        """Get the current size of the stack."""
        return len(self.items)
    
    def peek(self):
        """
        Look at the top item without removing it.
        :return: The top item, or None if stack is empty.
        """
        if self.items:
            return self.items[-1]
        return None
