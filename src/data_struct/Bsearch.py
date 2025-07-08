class TreeNode:
    """
    Node of the BST.
    Attributes:
        key: sortable identifier
        data: payload (e.g., tuple)
        left, right: child nodes
    """
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    """
    In-memory index for fast CRUD via BST operations.
    """
    def __init__(self, log_fn=None):
        self.root = None
        self.log = log_fn or (lambda msg: None)

    def insert(self, key, data):
        self.log(f"[Insert] key={key}")
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if node is None:
            return TreeNode(key, data)
        if key < node.key:
            self.log(f"[Insert] go left at {node.key}")
            node.left = self._insert(node.left, key, data)
        elif key > node.key:
            self.log(f"[Insert] go right at {node.key}")
            node.right = self._insert(node.right, key, data)
        else:
            self.log(f"[Insert] update data at {key}")
            node.data = data
        return node

    def search(self, key):
        self.log(f"[Search] key={key}")
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.data
        if key < node.key:
            self.log(f"[Search] left at {node.key}")
            return self._search(node.left, key)
        else:
            self.log(f"[Search] right at {node.key}")
            return self._search(node.right, key)

    def delete(self, key):
        self.log(f"[Delete] key={key}")
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            succ = self._min_node(node.right)
            node.key, node.data = succ.key, succ.data
            node.right = self._delete(node.right, succ.key)
        return node

    def _min_node(self, node):
        while node.left:
            node = node.left
        return node

    def inorder(self):
        yield from self._inorder(self.root)

    def _inorder(self, node):
        if not node:
            return
        yield from self._inorder(node.left)
        yield (node.key, node.data)
        yield from self._inorder(node.right)