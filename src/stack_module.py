class Stack:
    """
        A simple Stack implementation using a Python list.
        It follows the Last-In, First-Out (LIFO) principle.
        Used for managing the 'undo' history of actions.
    """
    def __init__(self):
        #Initializes the stack
        self._items=[]

    def push(self, item):
        #Push an item onto the stack
        self._items.append(item)

    def pop(self):
        #Pops and returns the top item from the stack, returns none if the stack is empty
        if not self.is_empty():
            return self._items.pop()
        else:
            return None

    def peek(self):
        #Returns the top item from the stack without removing it, returns None if the stack is empty
        if not self.is_empty():
            return self._items[-1]
        else:
            return None

    def is_empty(self):
        #Checks if the stack is empty
        if len(self._items)==0:
            return True
        else:
            return False
