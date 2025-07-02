import heapq
class PriorityQueue:
    """
    A Priority Queue implementation using Python's heapq library.
    It stores tasks based on their priority, allowing for efficient retrieval
    of the highest-priority task.
    Note: heapq is a min-heap, so lower priority numbers are considered higher priority.
    """
    def __init__(self):
        """Initializes the priority queue."""
        self._heap=[]

    def push(self, priority, item):
         """
        Pushes an item with a given priority onto the queue.
        - priority (int): The priority of the item.
        - item: The item to be stored (in our case, a task_id).
        """
         heapq.heappush(self._heap,(priority,item))

    def pop(self):
        """
        Pops the item with the highest priority (lowest number).
        Returns a tuple (priority, item).
        """
        if not self.is_empty():
            return heapq.heappop(self._heap)
        else:
            return None

    def is_empty(self):
       #Checks if the priority queue is empty
       if len(self._heap)==0:
           return True
       else:
           return False

    def clear(self):
       #Clears all items from the priority queue
       self._heap=[]

    def repopulate(self,items):
        """
         Clears the heap and repopulates it from a list of (priority, item) tuples.
         This is useful for rebuilding the heap after deletions or updates.
        """
        self.clear()
        for priority,item in items:
            self.push(priority,item)