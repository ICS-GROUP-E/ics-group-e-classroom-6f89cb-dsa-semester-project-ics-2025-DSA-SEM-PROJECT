from task import Task
from hash_table_module import HashTable
from priority_queue_module import PriorityQueue
from bst_module import BinarySearchTree
from stack_module import Stack


class TaskManager:
    """
    The central controller for the to-do list application.
    It integrates all data structures to manage tasks and provides a
    public API for the user interface to interact with.
    """

    def __init__(self):
        """Initializes the TaskManager and all its data structures."""
        print("Initializing TaskManager...")
        # Primary storage for tasks, allowing O(1) lookup by ID.
        self.tasks_ht = HashTable()

        # Auxiliary structures for sorting and features.
        self.tasks_pq = PriorityQueue()
        self.tasks_bst = BinarySearchTree()
        self.undo_stack = Stack()

        # Placeholder for the database handler.
        self.db_handler = None
        print("TaskManager initialized.")

    def set_db_handler(self, handler):
        """Connects a database handler to the TaskManager."""
        self.db_handler = handler

    def load_tasks_from_db(self):
        """Loads all tasks from the database and populates the data structures."""
        if not self.db_handler:
            print("Error: No database handler set.")
            return

        tasks = self.db_handler.load_all_tasks()
        print(f"Loading {len(tasks)} tasks from the database...")
        for task_data in tasks:
            # Re-create task objects from dictionary data
            task = Task(**task_data)
            self.tasks_ht.insert(task.task_id, task)

        # After loading all tasks, rebuild the auxiliary structures
        self._resync_aux_structures()
        print("Tasks loaded and data structures synchronized.")

    def _resync_aux_structures(self):
        """
        Private helper method to rebuild the PQ and BST from the HashTable.
        This ensures consistency after any modification.
        """
        # Clear existing data
        self.tasks_pq.clear()
        self.tasks_bst.clear()

        # Repopulate from the HashTable (the single source of truth)
        all_tasks = self.tasks_ht.get_all_items()
        for task in all_tasks:
            # Only add pending tasks to the active sorting structures
            if task.status == 'pending':
                self.tasks_pq.push(task.priority, task.task_id)
                self.tasks_bst.insert(task.difficulty, task.task_id)

    def create_task(self, description, priority, difficulty):
        """
        Creates a new task, adds it to all data structures, and logs the action.
        """
        task = Task(description=description, priority=priority, difficulty=difficulty)

        # Push the 'create' action to the undo stack
        undo_data = {'action': 'create', 'task_id': task.task_id}
        self.undo_stack.push(undo_data)

        # 1. Add to primary storage
        self.tasks_ht.insert(task.task_id, task)

        # 2. Add to auxiliary structures
        self.tasks_pq.push(task.priority, task.task_id)
        self.tasks_bst.insert(task.difficulty, task.task_id)

        # 3. Save to database
        if self.db_handler:
            self.db_handler.save_task(task)

        print(f"Task created: {task}")
        return task

    def get_task(self, task_id):
        """Retrieves a single task by its ID."""
        return self.tasks_ht.lookup(task_id)

    def update_task(self, task_id, new_description=None, new_priority=None, new_difficulty=None, new_status=None):
        """
        Updates an existing task's properties and logs the action.
        """
        task = self.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        # Push the original state to the undo stack before making changes
        undo_data = {'action': 'update', 'task_id': task_id, 'old_state': task.to_dict()}
        self.undo_stack.push(undo_data)

        # Update properties if new values are provided
        if new_description is not None: task.description = new_description
        if new_priority is not None: task.priority = int(new_priority)
        if new_difficulty is not None: task.difficulty = int(new_difficulty)
        if new_status is not None: task.status = new_status

        # Resynchronize auxiliary data structures to reflect changes
        self._resync_aux_structures()

        # Save changes to the database
        if self.db_handler:
            self.db_handler.update_task(task)

        print(f"Task updated: {task}")
        return True

    def delete_task(self, task_id):
        """
        Deletes a task from all data structures and logs the action.
        """
        task = self.tasks_ht.lookup(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        # Push the deleted task's data to the undo stack before deleting
        undo_data = {'action': 'delete', 'task_data': task.to_dict()}
        self.undo_stack.push(undo_data)

        # 1. Delete from primary storage
        self.tasks_ht.delete(task_id)

        # 2. Resynchronize auxiliary structures
        self._resync_aux_structures()

        # 3. Delete from database
        if self.db_handler:
            self.db_handler.delete_task(task_id)

        print(f"Task deleted: {task_id}")
        return True

    def undo_last_action(self):
        """Reverts the last action performed (create, update, or delete)."""
        last_action = self.undo_stack.pop()
        if not last_action:
            print("No action to undo.")
            return

        action_type = last_action['action']

        if action_type == 'create':
            task_id = last_action['task_id']
            # Directly remove the task from storage and DB
            if self.tasks_ht.lookup(task_id):
                self.tasks_ht.delete(task_id)
                if self.db_handler:
                    self.db_handler.delete_task(task_id)
                print(f"Undo create: Task {task_id} removed.")

        elif action_type == 'delete':
            # Restore the task from its saved data
            task_data = last_action['task_data']
            task = Task(**task_data)
            self.tasks_ht.insert(task.task_id, task)
            if self.db_handler:
                self.db_handler.save_task(task)
            print(f"Undo delete: Task {task.task_id} restored.")

        elif action_type == 'update':
            # Restore the task to its old state
            old_state = last_action['old_state']
            task = Task(**old_state)
            self.tasks_ht.insert(task.task_id, task)  # Overwrite current state in HT
            if self.db_handler:
                self.db_handler.update_task(task)
            print(f"Undo update: Task {task.task_id} reverted to previous state.")

        # Crucially, resync all auxiliary structures after any undo action
        # to ensure they reflect the new state of the main hash table.
        self._resync_aux_structures()

    # --- Data Retrieval Methods for the GUI ---

    def get_all_tasks(self):
        """Returns a list of all tasks, sorted by creation date."""
        all_tasks = self.tasks_ht.get_all_items()
        return sorted(all_tasks, key=lambda task: task.created_at)

    def get_tasks_by_priority(self):
        """
        Returns a list of PENDING tasks sorted from highest to lowest priority.
        """
        sorted_ids = [item[1] for item in sorted(self.tasks_pq._heap)]

        # Look up the full task object and explicitly filter for pending status
        pending_tasks = []
        for task_id in sorted_ids:
            task = self.tasks_ht.lookup(task_id)
            if task and task.status == 'pending':
                pending_tasks.append(task)
        return pending_tasks

    def get_tasks_by_difficulty(self):
        """
        Returns a list of PENDING tasks sorted from lowest to highest difficulty.
        """
        sorted_nodes = self.tasks_bst.get_all_nodes_sorted()

        # Look up the full task object and explicitly filter for pending status
        pending_tasks = []
        for _, task_id in sorted_nodes:
            task = self.tasks_ht.lookup(task_id)
            if task and task.status == 'pending':
                pending_tasks.append(task)
        return pending_tasks
