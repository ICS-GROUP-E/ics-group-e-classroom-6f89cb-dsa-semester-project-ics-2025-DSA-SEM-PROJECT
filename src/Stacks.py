from datetime import datetime

class ActivityNode:
    def __init__(self, action, details):
        self.action = action      # e.g., "ADD", "DELETE"
        self.details = details    # e.g., "ISBN: 123"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.next = None          # Pointer to next node

class ActivityStack:
    def __init__(self, max_size=10):
        self.top = None           # Top of stack
        self.size = 0             # Current size set to zero
        self.max_size = max_size  # limit of stack size

    def push(self, action, details):
        """Adds an action to the stack (O(1) time)."""
        new_node = ActivityNode(action, details)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

        
        if self.size > self.max_size:
            self._remove_last()
        return f"Logged: {action}"

    def pop(self):
        """Removes and returns the top action (O(1) time)."""
        if not self.top:
            return None
        popped = self.top
        self.top = self.top.next
        self.size -= 1
        return (popped.action, popped.details, popped.timestamp)

    def peek(self):
        """Returns the top action without removal (O(1) time)."""
        return (self.top.action, self.top.details) if self.top else None

    def _remove_last(self):
        """Maintains stack size by pruning oldest node (O(n) time)."""
        current = self.top
        while current.next and current.next.next:  # to Stop at second last
            current = current.next
        current.next = None
        self.size -= 1

    def get_all_actions(self):
        """Returns all actions as a list (O(n) time)."""
        actions = []
        current = self.top
        while current:
            actions.append({
                "action": current.action,
                "details": current.details,
                "timestamp": current.timestamp
            })
            current = current.next
        return actions  # Newest will be output first