"""
Queue implementation for reminder management.
Stores events that have reminders set for processing.
"""

class EventQueue:
    def __init__(self):
        """Initialize an empty queue."""
        self.items = []
    
    def enqueue(self, item):
        """
        Add an item to the end of the queue.
        :param item: Item to add to the queue.
        """
        self.items.append(item)
    
    def dequeue(self):
        """
        Remove and return the first item from the queue.
        :return: The first item, or None if queue is empty.
        """
        if self.items:
            return self.items.pop(0)
        return None
    
    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0
    
    def size(self):
        """Get the current size of the queue."""
        return len(self.items)
    
    def peek(self):
        """
        Look at the first item without removing it.
        :return: The first item, or None if queue is empty.
        """
        if self.items:
            return self.items[0]
        return None
    
    def clear(self):
        """Remove all items from the queue."""
        self.items.clear()
    
    def contains(self, item):
        """
        Check if an item is in the queue.
        :param item: Item to search for.
        :return: True if item is found, False otherwise.
        """
        return item in self.items
    
    def remove(self, item):
        """
        Remove a specific item from the queue.
        :param item: Item to remove.
        :return: True if item was removed, False if not found.
        """
        try:
            self.items.remove(item)
            return True
        except ValueError:
            return False
