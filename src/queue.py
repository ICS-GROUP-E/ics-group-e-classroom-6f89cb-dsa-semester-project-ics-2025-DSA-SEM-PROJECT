from collections import deque

class NotificationQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, notification):
        self.queue.append(notification)

    def dequeue(self):
        return self.queue.popleft() if not self.is_empty() else None

    def peek(self):
        return self.queue[0] if not self.is_empty() else None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)