"""
Binary Search Tree implementation for event management.
Events are ordered by their date and time.
"""

class BSTNode:
    def __init__(self, event):
        """
        Initializes a node for the Binary Search Tree.
        :param event: The Event object to store in this node.
        """
        self.event = event
        self.left = None
        self.right = None
