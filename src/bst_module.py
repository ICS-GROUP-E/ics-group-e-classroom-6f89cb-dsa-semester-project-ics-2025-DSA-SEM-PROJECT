class Node:
    """A node in the binary search tree"""
    def __init__(self,key,value):
        self.key=key #The difficulty level
        self.values=[value] #List of task_ids with this difficulty
        self.right=None
        self.left=None
class BinarySearchTree:
    """
    A binary search tree to store and sort tasks by difficulty.
    Key: difficulty level
    Value: Task ID
    Supports multiple tasks having the same difficulty level
    """
    def __init__(self):
        #Initializes the BST
        self.root=None
    def insert(self,key,value):
        #Inserts a value into the BST based on its key (difficulty)
        if self.root is None:
            self.root=Node(key,value)
        else:
            self._insert_recursive(self.root,key,value)

    def _insert_recursive(self,current_node, key,value):
        if key==current_node.key:
            current_node.values.append(value)
        elif key<current_node.key:
            if current_node.left is None:
                current_node.left=Node(key,value)
            else:
                self._insert_recursive(current_node.left,key,value)
        else:
            if current_node.right is None:
                current_node.right=Node(key,value)
            else:
                self._insert_recursive(current_node.right,key,value)

    def delete(self,key,value):
        #Deletes a specific value from the node with the given key.
        self.root=self._delete_recursive(self.root,key,value)

    def _delete_recursive(self,current_node,key,value):
        if current_node is None:
            return None
        if key<current_node.key:
            current_node.left=self._delete_recursive(current_node.left,key,value)
        elif key>current_node.key:
            current_node.right=self._delete_recursive(current_node.right,key,value)
        else:#Key found
            if value in current_node.values:
                current_node.values.remove(value)
            #If no values at this key, delete the node itself
            if not current_node.values:
                if current_node.left is None:
                    return current_node.right
                if current_node.right is None:
                    return current_node.left
                else:#Node has two children, find in-order successor (smallest in right subtree)
                    min_larger_node = self._find_min(current_node.right)
                    current_node.key = min_larger_node.key
                    current_node.values = min_larger_node.values
                    current_node.right = self._delete_recursive(current_node.right, min_larger_node.key, min_larger_node.values[0])
                    # We only need to remove one value from the successor to trigger its deletion
        return current_node

    def _find_min(self,current_node):
        while current_node.left:
            current_node=current_node.left
        return current_node

    def get_all_nodes_sorted(self):
        """Performs an in-order traversal to get all tasks sorted by difficulty
           Returns a list of (key,value_list) tuples."""
        result=[]
        self._in_order_traversal(self.root,result)
        return result

    def _in_order_traversal(self,current_node,result):
        if current_node:
            self._in_order_traversal(current_node.left,result)
            #Add all values from current node
            for value in current_node.values:
                result.append((current_node.key,value))
            self._in_order_traversal(current_node.right,result)

    def clear(self):
       #Clears all nodes from the tree.
       self.root=None
