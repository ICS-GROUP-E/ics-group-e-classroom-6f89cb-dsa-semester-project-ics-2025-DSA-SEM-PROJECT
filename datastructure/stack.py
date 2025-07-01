class ActionStack:
    def __init__(self):
        self.stack = []

    def push(self,action_type,student):
        self.stack.append((action_type,student))

    def pop(self):
        if self.stack:
            action = self.stack.pop()

            return action
        return None

    def peek(self):
        return self.stack[-1]if self.stack else None

    def is_empty(self):
        return len(self.stack) == 0

    def clear(self):
        self.stack.clear()

        