class TaskNode:
    def __init__(self, priority, task_id, description):
        self.priority = priority
        self.task_id = task_id
        self.description = description
        self.left = None
        self.right = None

class TaskBST:
    def __init__(self):
        self.root = None

    def insert(self, priority, task_id, description):
        self.root = self._insert_recursive(self.root, priority, task_id, description)

    def _insert_recursive(self, node, priority, task_id, description):
        if node is None:
            return TaskNode(priority, task_id, description)
        if priority < node.priority:
            node.left = self._insert_recursive(node.left, priority, task_id, description)
        elif priority > node.priority:
            node.right = self._insert_recursive(node.right, priority, task_id, description)
        else:
            # Update existing
            node.task_id = task_id
            node.description = description
        return node

    def search(self, priority):
        return self._search_recursive(self.root, priority)

    def _search_recursive(self, node, priority):
        if node is None or node.priority == priority:
            return node
        if priority < node.priority:
            return self._search_recursive(node.left, priority)
        else:
            return self._search_recursive(node.right, priority)

    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return [(n.priority, n.task_id, n.description) for n in result]

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node)
            self._inorder_recursive(node.right, result)