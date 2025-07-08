import datetime
import logging
from dataclasses import dataclass
from typing import Optional, List

# Import data structures (assuming these paths are correct in your project structure)
# If LLNode is defined in core/event_planner.py, the import below might be redundant or cause issues
# For this code, I'm assuming LLNode is defined directly in this file as it was in previous versions.
# If you have data_structures/linked_list.py with LLNode, you might need to adjust this.
# from data_structures.binary_search_tree import BSTNode # Assuming BSTNode is in data_structures/binary_search_tree.py
# from data_structures.linked_list import LLNode # Assuming LLNode is in data_structures/linked_list.py
# from data_structures.stack import EventStack # Assuming EventStack is in data_structures/stack.py
# from data_structures.queue import EventQueue # Assuming EventQueue is in data_structures/queue.py

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Event class
@dataclass
class Event:
    event_id: int
    name: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    reminder_set: bool
    location: str = ""
    description: str = ""
    attendees: str = ""  # Comma-separated names

    def __copy__(self):
        """Returns a shallow copy of the Event object."""
        return Event(
            self.event_id,
            self.name,
            self.date,
            self.time,
            self.reminder_set,
            self.location,
            self.description,
            self.attendees
        )

# Node for Linked List (tasks) - Keeping it here as per your provided code structure
class LLNode:
    def __init__(self, data: str, completed: bool = False):
        """
        Initializes a node for a linked list.
        :param data: The data to store in the node (e.g., task description).
        :param completed: Boolean indicating if the task is completed (default False).
        """
        self.data = data
        self.completed = completed
        self.next = None

# Node for Binary Search Tree - Keeping it here as per your provided code structure
class BSTNode:
    def __init__(self, event: Event):
        """
        Initializes a node for the Binary Search Tree.
        :param event: The Event object to store in this node.
        """
        self.event = event
        self.left = None
        self.right = None

# Event Planner class integrating BST, Stack, Linked List, and Queue
class EventPlanner:
    def __init__(self, initial_event_id_counter: int = 1):
        """
        Initializes the EventPlanner with various data structures.
        :param initial_event_id_counter: The starting ID for new events, typically max_id + 1 from DB.
        """
        self.bst_root = None  # BST for events (for ordered retrieval by date/time)
        self._events_by_id = {} # Dictionary for O(1) event lookup by ID
        self.edit_stack = []  # Stack for recently edited events, max 10
        self.todo_lists = {}  # {event_id: LLNode} for tasks
        self.reminder_queue = []  # Queue for events with reminders
        self.event_id_counter = initial_event_id_counter # Starts from 1 or max_id + 1 from DB
        
        # Execution tracking for reporting
        self.execution_log = {
            'bst': [],
            'stack': [],
            'queue': [],
            'linked_list': []
        }
        
        logger.info(f"EventPlanner initialized with ID counter starting at {self.event_id_counter}")
    
    def _log_execution(self, data_structure: str, operation: str, details: str = ""):
        """Log an execution for reporting purposes."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        execution_record = {
            'timestamp': timestamp,
            'operation': operation,
            'details': details
        }
        self.execution_log[data_structure].append(execution_record)

    @staticmethod
    def _get_datetime(date: str, time: str) -> datetime.datetime:
        """
        Parses and validates a date and time string into a datetime object.
        :param date: Date string in 'YYYY-MM-DD' format.
        :param time: Time string in 'HH:MM' (24-hour) format.
        :return: A datetime object.
        :raises ValueError: If the date or time format is invalid.
        """
        try:
            dt = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            logger.debug(f"Parsed datetime: {date} {time} -> {dt}")
            return dt
        except ValueError:
            logger.error(f"Invalid date/time format: {date} {time}")
            raise ValueError("Invalid date or time format. Use YYYY-MM-DD and HH:MM.")

    def create_event(self, name: str, date: str, time: str, reminder_set: bool, 
                     location: str = "", description: str = "", attendees: str = "") -> Event:
        """
        Creates a new event, assigns a unique ID, and integrates it into the data structures.
        This method is for *new* events created by the user via the GUI.
        :param name: Name of the event.
        :param date: Date of the event (YYYY-MM-DD).
        :param time: Time of the event (HH:MM).
        :param reminder_set: Boolean indicating if a reminder should be set.
        :param location: Location of the event.
        :param description: Description of the event.
        :param attendees: Comma-separated list of attendees.
        :return: The newly created Event object.
        :raises ValueError: If date/time format is invalid.
        """
        logger.info(f"Creating event: {name}, {date} {time}")
        # Validate date/time format early
        self._get_datetime(date, time) 
        
        event = Event(self.event_id_counter, name, date, time, reminder_set, location, description, attendees)
        
        # Store in dictionary for O(1) ID lookup
        self._events_by_id[event.event_id] = event
        
        # Insert into BST for chronological ordering
        self._insert_bst(event)
        self._log_execution('bst', 'INSERT', f'Event "{name}" (ID: {event.event_id}) inserted into BST')
        
        # Initialize an empty linked list for tasks for this new event
        self.todo_lists[event.event_id] = None
        self._log_execution('linked_list', 'INITIALIZE', f'Task list initialized for Event ID: {event.event_id}')
        
        # Add to reminder queue if reminder is set
        if reminder_set:
            self.reminder_queue.append(event)
            self._log_execution('queue', 'ENQUEUE', f'Event "{name}" (ID: {event.event_id}) added to reminder queue')
        
        # Push the newly created event's state to the edit stack for undo functionality (e.g., undoing creation)
        self.edit_stack.append(event.__copy__()) # Push a copy
        if len(self.edit_stack) > 10:
            self.edit_stack.pop(0) # Maintain stack limit
        self._log_execution('stack', 'PUSH', f'Event "{name}" (ID: {event.event_id}) state pushed to edit stack')
            
        self.event_id_counter += 1
        logger.info(f"Event created: ID={event.event_id}")
        return event

    def _add_event_for_loading(self, event: Event):
        """
        Adds an event loaded from the database into the in-memory data structures.
        This method bypasses side effects like incrementing counter or pushing to stack/queue.
        :param event: The Event object loaded from the database.
        """
        logger.debug(f"Loading event ID {event.event_id} from DB into planner.")
        self._events_by_id[event.event_id] = event
        self._insert_bst(event)
        # Initialize todo_lists entry for this event (tasks will be loaded separately)
        if event.event_id not in self.todo_lists: # Only if not already initialized
            self.todo_lists[event.event_id] = None 
        if event.reminder_set and event not in self.reminder_queue:
            self.reminder_queue.append(event)
        # Do NOT increment event_id_counter or push to edit_stack here

    def _insert_bst(self, event: Event) -> None:
        """
        Inserts an event into the Binary Search Tree based on its date and time.
        If dates/times are equal, it goes to the right subtree.
        :param event: The Event object to insert.
        """
        logger.debug(f"Inserting event {event.name} (ID: {event.event_id}) into BST")
        if not self.bst_root:
            self.bst_root = BSTNode(event)
        else:
            self._insert_bst_recursive(self.bst_root, event)

    def _insert_bst_recursive(self, node: BSTNode, event: Event) -> None:
        """Helper for recursive BST insertion."""
        event_dt = self._get_datetime(event.date, event.time)
        node_dt = self._get_datetime(node.event.date, node.event.time)

        if event_dt < node_dt:
            if node.left is None:
                node.left = BSTNode(event)
                logger.debug(f"Inserted {event.name} as left child of {node.event.name}")
            else:
                self._insert_bst_recursive(node.left, event)
        else: # event_dt >= node_dt (handles equal dates/times by going right)
            if node.right is None:
                node.right = BSTNode(event)
                logger.debug(f"Inserted {event.name} as right child of {node.event.name}")
            else:
                self._insert_bst_recursive(node.right, event)

    def update_event(self, event_id: int, name: Optional[str] = None, date: Optional[str] = None, 
                    time: Optional[str] = None, location: Optional[str] = None, 
                    description: Optional[str] = None, attendees: Optional[str] = None, 
                    reminder_set: Optional[bool] = None) -> Optional[Event]:
        """
        Updates an existing event's details. Handles BST re-insertion if date/time changes
        and manages reminder queue. Pushes the old state to the edit stack for undo.
        :param event_id: The ID of the event to update.
        :param kwargs: Keyword arguments for attributes to update.
        :return: The updated Event object, or None if not found or invalid input.
        """
        logger.info(f"Updating event ID={event_id}")
        
        # Get the event using the ID dictionary for efficient O(1) lookup
        event_to_update = self._events_by_id.get(event_id)
        if not event_to_update:
            logger.warning(f"Event {event_id} not found for update.")
            return None
        
        # Create a deep copy of the event's current state for the undo stack
        old_event_state = event_to_update.__copy__()

        # Determine if date/time attributes (which are BST keys) are changing
        date_time_changed = False
        new_date = date if date is not None else event_to_update.date
        new_time = time if time is not None else event_to_update.time

        if new_date != event_to_update.date or new_time != event_to_update.time:
            date_time_changed = True
            try:
                # Validate the new combined date/time before applying
                self._get_datetime(new_date, new_time)
            except ValueError as e:
                logger.error(f"Update failed: Invalid new date/time for event {event_id}. {e}")
                return None # Indicate failure due to invalid input

        # Apply updates to the event object
        if name is not None:
            event_to_update.name = name
        if date is not None:
            event_to_update.date = new_date # Apply validated new date
        if time is not None:
            event_to_update.time = new_time # Apply validated new time
        if location is not None:
            event_to_update.location = location
        if description is not None:
            event_to_update.description = description
        if attendees is not None:
            event_to_update.attendees = attendees
        
        # Handle reminder_set change and queue management
        # If reminder_set changes, or if date/time changes AND reminder_set is True, re-evaluate queue
        reminder_status_changed = (reminder_set is not None and reminder_set != event_to_update.reminder_set)

        if reminder_status_changed or (date_time_changed and event_to_update.reminder_set):
            # Remove from queue first to handle both status change and re-queuing
            self.reminder_queue = [e for e in self.reminder_queue if e.event_id != event_id]
            self._log_execution('queue', 'DEQUEUE', f'Event "{event_to_update.name}" (ID: {event_id}) removed from reminder queue for re-evaluation')

            if reminder_set is not None: # Apply new reminder_set status
                event_to_update.reminder_set = reminder_set
            
            if event_to_update.reminder_set: # If reminder is now set (or still set), add back to queue
                self.reminder_queue.append(event_to_update)
                self._log_execution('queue', 'ENQUEUE', f'Event "{event_to_update.name}" (ID: {event_id}) re-added to reminder queue')
                logger.debug(f"Event {event_id} re-added to reminder queue.")
            else:
                logger.debug(f"Event {event_id} reminder unset, removed from queue.")
        
        # If date or time changed, the event's position in the BST might change.
        # So, we delete the old node and re-insert the updated event.
        if date_time_changed:
            logger.debug(f"Date/time changed for event {event_id}. Re-inserting into BST.")
            self.bst_root = self._delete_bst_node(self.bst_root, event_id) # Remove old node by ID
            self._insert_bst(event_to_update) # Insert updated event
            self._log_execution('bst', 'UPDATE', f'Event "{event_to_update.name}" (ID: {event_id}) re-inserted into BST due to time change')
        
        # Push the *original* state of the event to the undo stack
        self.edit_stack.append(old_event_state)
        if len(self.edit_stack) > 10:
            self.edit_stack.pop(0) # Maintain stack limit by removing oldest

        logger.info(f"Event {event_id} updated.")
        return event_to_update

    def _find_event_in_bst_recursive(self, node: Optional[BSTNode], event_id: int) -> Optional[Event]:
        """
        Helper method to find an event by ID by traversing the BST.
        This is distinct from the O(1) dictionary lookup for demonstrating BST traversal.
        """
        if not node:
            return None
        if node.event.event_id == event_id:
            return node.event
        
        # Search left subtree
        found_in_left = self._find_event_in_bst_recursive(node.left, event_id)
        if found_in_left:
            return found_in_left
        
        # Search right subtree
        return self._find_event_in_bst_recursive(node.right, event_id)


    def _delete_bst_node(self, node: Optional[BSTNode], event_id: int) -> Optional[BSTNode]:
        """
        Deletes an event from the Binary Search Tree based on its event_id.
        Handles nodes with zero, one, or two children.
        :param node: The current BSTNode being considered.
        :param event_id: The ID of the event to delete.
        :return: The new root of the (sub)tree after deletion.
        """
        if not node:
            return None

        # Traverse the BST to find the node to delete based on event_id
        if event_id < node.event.event_id: 
            node.left = self._delete_bst_node(node.left, event_id)
        elif event_id > node.event.event_id:
            node.right = self._delete_bst_node(node.right, event_id)
        else: # node.event.event_id == event_id, this is the node to delete
            logger.debug(f"Found node to delete: Event ID={event_id}")
            # Case 1: Node has no left child (or no children)
            if not node.left:
                return node.right
            # Case 2: Node has no right child
            elif not node.right:
                return node.left
            
            # Case 3: Node has two children
            # Find the inorder successor (smallest in the right subtree)
            successor = self._find_min(node.right)
            # Copy the successor's event data to this node
            node.event = successor.event 
            # Delete the inorder successor from the right subtree
            node.right = self._delete_bst_node(node.right, successor.event.event_id)
        return node

    def _find_min(self, node: BSTNode) -> BSTNode:
        """
        Finds the node with the minimum event (earliest date/time) in a BST subtree.
        Used internally for BST deletion.
        :param node: The root of the subtree to search.
        :return: The BSTNode containing the minimum event.
        """
        current = node
        while current.left:
            current = current.left
        logger.debug(f"Found minimum node: {current.event.name} (ID: {current.event.event_id})")
        return current

    def delete_event(self, event_id: int) -> bool:
        """
        Deletes an event from all relevant data structures.
        :param event_id: The ID of the event to delete.
        :return: True if the event was deleted, False otherwise.
        """
        logger.info(f"Deleting event ID={event_id}")
        event_to_delete = self._events_by_id.get(event_id)
        if not event_to_delete:
            logger.warning(f"Event {event_id} not found for deletion.")
            return False
        
        # Remove from BST
        self.bst_root = self._delete_bst_node(self.bst_root, event_id)
        self._log_execution('bst', 'DELETE', f'Event "{event_to_delete.name}" (ID: {event_id}) deleted from BST')
        
        # Remove from ID lookup dictionary
        del self._events_by_id[event_id]
        
        # Remove associated linked list tasks
        self.todo_lists.pop(event_id, None)
        self._log_execution('linked_list', 'DELETE_ALL', f'All tasks deleted for Event ID: {event_id}')
        
        # Remove from reminder queue if present
        # Rebuild queue without the event (more robust)
        if event_to_delete.reminder_set:
            self.reminder_queue = [e for e in self.reminder_queue if e.event_id != event_id]
            self._log_execution('queue', 'DEQUEUE', f'Event "{event_to_delete.name}" (ID: {event_id}) removed from reminder queue')

        logger.info(f"Event {event_id} deleted.")
        return True

    def view_events(self, upcoming: bool = True) -> List[Event]:
        """
        Retrieves events from the BST in chronological order, filtered by upcoming or past.
        :param upcoming: If True, return upcoming events; if False, return past events.
        :return: A list of Event objects.
        """
        current_date = datetime.datetime.now()
        events = []
        # Perform in-order traversal to get events in sorted order
        self._inorder_traversal(self.bst_root, events, current_date, upcoming)
        logger.info(f"Viewing {'upcoming' if upcoming else 'past'} events: {len(events)} found.")
        return events

    def _inorder_traversal(self, node: Optional[BSTNode], events: List[Event], 
                            current_date: datetime.datetime, upcoming: bool) -> None:
        """
        Helper for in-order traversal of BST to collect events with date filter.
        :param node: The current BSTNode.
        :param events: List to append filtered events to.
        :param current_date: The current datetime for comparison.
        :param upcoming: Filter for upcoming or past events.
        """
        if node:
            self._inorder_traversal(node.left, events, current_date, upcoming)
            event_dt = self._get_datetime(node.event.date, node.event.time)
            if (upcoming and event_dt >= current_date) or (not upcoming and event_dt < current_date):
                events.append(node.event)
            self._inorder_traversal(node.right, events, current_date, upcoming)

    def add_task(self, event_id: int, task: str) -> bool:
        """
        Adds a task to an event's linked list of tasks.
        :param event_id: The ID of the event to add the task to.
        :param task: The description of the task.
        :return: True if task added, False if event not found.
        """
        logger.info(f"Adding task '{task}' to event {event_id}")
        if event_id not in self._events_by_id: # Efficient check
            logger.warning(f"Event {event_id} not found for adding task.")
            return False
        
        new_node = LLNode(task)
        if self.todo_lists.get(event_id) is None:
            self.todo_lists[event_id] = new_node # First task for this event
        else:
            current = self.todo_lists[event_id]
            while current.next:
                current = current.next
            current.next = new_node # Append to end of linked list
        logger.info(f"Task '{task}' added to event {event_id}.")
        self._log_execution('linked_list', 'ADD', f'Task "{task}" added to Event ID: {event_id}')
        return True

    def remove_task(self, event_id: int, task: str) -> bool:
        """
        Removes a task from an event's linked list of tasks.
        :param event_id: The ID of the event.
        :param task: The description of the task to remove.
        :return: True if task removed, False if event or task not found.
        """
        logger.info(f"Removing task '{task}' from event {event_id}")
        if event_id not in self._events_by_id or self.todo_lists.get(event_id) is None:
            logger.warning(f"Event {event_id} or task list not found.")
            return False
        
        head = self.todo_lists[event_id]
        # If head node is the task to remove
        if head and head.data == task: # Check head is not None
            self.todo_lists[event_id] = head.next
            logger.info(f"Task '{task}' removed from event {event_id}.")
            self._log_execution('linked_list', 'REMOVE', f'Task "{task}" removed from Event ID: {event_id}')
            return True
        
        current = head
        while current and current.next: # Ensure current and current.next are not None
            if current.next.data == task:
                current.next = current.next.next # Skip the node to remove
                logger.info(f"Task '{task}' removed from event {event_id}.")
                return True
            current = current.next
        
        logger.warning(f"Task '{task}' not found in event {event_id}'s task list.")
        return False

    def mark_task_complete(self, event_id: int, task: str) -> bool:
        """
        Marks a task in an event's linked list as complete.
        :param event_id: The ID of the event.
        :param task: The description of the task to mark complete.
        :return: True if task marked, False if event or task not found.
        """
        logger.info(f"Marking task '{task}' complete for event {event_id}")
        if event_id not in self._events_by_id or self.todo_lists.get(event_id) is None:
            logger.warning(f"Event {event_id} or task list not found.")
            return False
        
        current = self.todo_lists[event_id]
        while current:
            if current.data == task:
                current.completed = True
                logger.info(f"Task '{task}' marked complete for event {event_id}.")
                self._log_execution('linked_list', 'MARK_COMPLETE', f'Task "{task}" marked complete for Event ID: {event_id}')
                return True
            current = current.next
        
        logger.warning(f"Task '{task}' not found in event {event_id}'s task list.")
        return False

    def get_tasks(self, event_id: int) -> List[dict]:
        """
        Retrieves all tasks for a given event with their completion status.
        :param event_id: The ID of the event.
        :return: A list of dictionaries, each with 'task' and 'completed' keys.
        """
        logger.info(f"Getting tasks for event {event_id}")
        if event_id not in self._events_by_id:
            logger.warning(f"Event {event_id} not found.")
            return []
        
        # If event exists but has no tasks yet, return empty list (this is normal)
        if self.todo_lists.get(event_id) is None:
            logger.info(f"Event {event_id} has no tasks yet.")
            return []
        
        tasks = []
        current = self.todo_lists[event_id]
        while current:
            tasks.append({"task": current.data, "completed": current.completed})
            current = current.next
        logger.info(f"Retrieved {len(tasks)} tasks for event {event_id}.")
        return tasks

    def undo_last_edit(self) -> Optional[Event]:
        """
        Undoes the last create or update operation by popping from the edit stack.
        Restores the event to its state prior to the last modification.
        :return: The restored Event object, or None if no edits to undo.
        """
        logger.info("Attempting to undo last edit.")
        if not self.edit_stack:
            logger.info("No edits to undo.")
            return None
        
        # Pop the last *original state* of the event from the stack
        # This is the state *before* the last create/update operation
        last_event_original_state = self.edit_stack.pop()
        event_id_to_undo = last_event_original_state.event_id

        # Check if the event currently exists in our system (by its ID)
        current_event_in_system = self._events_by_id.get(event_id_to_undo)

        if current_event_in_system:
            # Scenario 1: The last action was an UPDATE on an existing event.
            logger.debug(f"Event ID {event_id_to_undo} found. Assuming last action was an update.")
            
            # Remove the current (potentially modified) version from BST
            self.bst_root = self._delete_bst_node(self.bst_root, event_id_to_undo)

            # Restore the event to its old state in the _events_by_id dictionary
            self._events_by_id[event_id_to_undo] = last_event_original_state
            
            # Re-insert the original state into the BST
            self._insert_bst(last_event_original_state)

            # Also, ensure reminder queue is updated based on restored state
            # Remove old event if it was in queue and new state says no reminder
            self.reminder_queue = [e for e in self.reminder_queue if e.event_id != event_id_to_undo]
            if last_event_original_state.reminder_set:
                self.reminder_queue.append(last_event_original_state)

            logger.info(f"Successfully restored event ID={event_id_to_undo} to its previous state.")
            return last_event_original_state
        else:
            # Scenario 2: The last action was a CREATE of a new event, and this undo aims to delete it.
            logger.warning(f"Event ID={event_id_to_undo} not found in current events. Assuming last action was a creation to be undone.")
            
            # If the event doesn't exist, and we're undoing, it means we should remove it from the system.
            self.bst_root = self._delete_bst_node(self.bst_root, event_id_to_undo)
            self._events_by_id.pop(event_id_to_undo, None)
            self.todo_lists.pop(event_id_to_undo, None)
            self.reminder_queue = [e for e in self.reminder_queue if e.event_id != event_id_to_undo]

            logger.info(f"Successfully undid creation/removed event ID={event_id_to_undo}.")
            return None # Indicate that the event was removed/un-created

    def view_edited_events(self) -> List[Event]:
        """
        Views the stack of recently edited event states.
        :return: A list of Event objects representing the history.
        """
        logger.info(f"Viewing {len(self.edit_stack)} edited events.")
        return self.edit_stack.copy() # Return a copy to prevent external modification

    def process_reminders(self) -> tuple[List[Event], List[Event]]:
        """
        Processes reminders from the queue based on current time.
        Identifies events needing general processing and those exactly 3 mins away for specific notification.
        :return: A tuple: (list of events processed and removed from queue, list of events for 3-min notification).
        """
        current_time = datetime.datetime.now()
        processed_for_removal = []
        three_min_reminders = [] # Renamed from ten_min_reminders

        # Iterate through a copy to allow modification of original queue during iteration
        for event in list(self.reminder_queue): 
            try:
                event_time = self._get_datetime(event.date, event.time)
                time_until_event = event_time - current_time

                # Define a precise window for "3 minutes to" alert
                three_min_lower_bound = datetime.timedelta(minutes=2, seconds=50) # 3 minutes - 10 seconds buffer
                three_min_upper_bound = datetime.timedelta(minutes=3, seconds=10) # 3 minutes + 10 seconds buffer

                # Check for specific 3-minute reminder
                if three_min_lower_bound <= time_until_event <= three_min_upper_bound:
                    three_min_reminders.append(event)
                    self._log_execution('queue', 'ALERT_TRIGGERED', f'3-min alert for event: {event.name}')

                # Events are removed from queue if they are past their event time (e.g., 1 minute past)
                # This ensures they stay in queue until the event has actually passed.
                if time_until_event < datetime.timedelta(minutes=-1): # Remove if event was more than 1 minute ago
                    processed_for_removal.append(event)
                
            except ValueError:
                logger.error(f"Skipping reminder for event ID {event.event_id} due to invalid date/time.")
        
        # Remove processed events from the queue
        for event in processed_for_removal:
            if event in self.reminder_queue: # Check existence before removing
                self.reminder_queue.remove(event)
                self._log_execution('queue', 'DEQUEUED_PAST', f'Event "{event.name}" (ID: {event.event_id}) dequeued as past.')
        
        logger.info(f"Processed {len(processed_for_removal)} reminders, {len(self.reminder_queue)} remaining in queue.")
        return processed_for_removal, three_min_reminders

    def view_reminder_queue(self) -> List[Event]:
        """
        Views the current events in the reminder queue.
        :return: A copy of the list of Event objects in the reminder queue.
        """
        logger.info(f"Viewing {len(self.reminder_queue)} reminders in queue.")
        return self.reminder_queue.copy()

# Example usage (for testing the backend logic)
if __name__ == "__main__":
    planner = EventPlanner()

    # --- Test Create Event ---
    print("\n--- Testing Create Event ---")
    event1 = planner.create_event("Team Sync", "2025-07-10", "10:00", True, "Zoom", "Discuss Q3 goals", "Alice,Bob")
    event2 = planner.create_event("Client Demo", "2025-07-11", "14:30", False, "Client Office", "Show new features", "Charlie")
    event3 = planner.create_event("Project Review", "2025-07-09", "09:00", True, "Meeting Room 3", "Review sprint progress", "David,Eve")
    event4 = planner.create_event("Lunch Break", "2025-07-10", "12:00", False) # Same date as event1
    
    print(f"All Events (upcoming): {[e.name for e in planner.view_events(upcoming=True)]}")
    # Expected order: Project Review, Team Sync, Lunch Break, Client Demo

    # --- Test Update Event ---
    print("\n--- Testing Update Event ---")
    print(f"Event1 before update: {planner._events_by_id[event1.event_id].name}, {planner._events_by_id[event1.event_id].date} {planner._events_by_id[event1.event_id].time}")
    planner.update_event(event1.event_id, name="Updated Team Sync", time="11:00", reminder_set=False)
    print(f"Event1 after update: {planner._events_by_id[event1.event_id].name}, {planner._events_by_id[event1.event_id].date} {planner._events_by_id[event1.event_id].time}")
    print(f"Reminder Queue after update: {[e.name for e in planner.view_reminder_queue()]}") # Event1 should be gone

    # --- Test Undo Last Edit (Update) ---
    print("\n--- Testing Undo Last Edit (Update) ---")
    print(f"Edit Stack: {[e.name for e in planner.view_edited_events()]}")
    undone_event = planner.undo_last_edit()
    if undone_event:
        print(f"Undo successful. Event1 restored to: {undone_event.name}, {undone_event.time}")
    print(f"Event1 current state: {planner._events_by_id[event1.event_id].name}, {planner._events_by_id[event1.event_id].time}")
    print(f"Reminder Queue after undo: {[e.name for e in planner.view_reminder_queue()]}") # Event1 should be back

    # --- Test Add/Remove/Mark Tasks (Linked List) ---
    print("\n--- Testing Task Management ---")
    planner.add_task(event1.event_id, "Prepare agenda")
    planner.add_task(event1.event_id, "Send pre-read materials")
    planner.mark_task_complete(event1.event_id, "Prepare agenda")
    print(f"Tasks for Event1: {planner.get_tasks(event1.event_id)}")
    planner.remove_task(event1.event_id, "Send pre-read materials")
    print(f"Tasks for Event1 after removal: {planner.get_tasks(event1.event_id)}")

    # --- Test Reminder Queue (Queue) ---
    print("\n--- Testing Reminder Queue ---")
    print(f"Initial Reminder Queue: {[e.name for e in planner.view_reminder_queue()]}")
    # To test process_reminders, we need an event close to current time
    # Let's create one that should trigger a reminder
    current_dt = datetime.datetime.now()
    future_event_time = current_dt + datetime.timedelta(minutes=5)
    event_now = planner.create_event("Quick Check", future_event_time.strftime("%Y-%m-%d"), 
                                     future_event_time.strftime("%H:%M"), True)
    print(f"Reminder Queue after adding 'Quick Check': {[e.name for e in planner.view_reminder_queue()]}")
    planner.process_reminders()
    print(f"Reminder Queue after processing: {[e.name for e in planner.view_reminder_queue()]}") # Quick Check should be processed and removed

    # --- Test Delete Event ---
    print("\n--- Testing Delete Event ---")
    print(f"Events before delete: {[e.name for e in planner.view_events()]}")
    planner.delete_event(event2.event_id)
    print(f"Events after deleting Client Demo: {[e.name for e in planner.view_events()]}")
    print(f"Check if Event2 is in _events_by_id: {event2.event_id in planner._events_by_id}")

    # --- Test Undo Last Edit (Create) ---
    print("\n--- Testing Undo Last Edit (Create) ---")
    # Let's create a new event and immediately undo it
    event_to_undo_create = planner.create_event("Temp Event", "2025-08-01", "09:00", False)
    print(f"Events after Temp Event creation: {[e.name for e in planner.view_events()]}")
    planner.undo_last_edit() # This should undo the creation of "Temp Event"
    print(f"Events after undoing Temp Event creation: {[e.name for e in planner.view_events()]}")
    print(f"Is Temp Event still in _events_by_id? {event_to_undo_create.event_id in planner._events_by_id}")

    # --- Test Invalid Date/Time ---
    print("\n--- Testing Invalid Date/Time ---")
    try:
        planner.create_event("Invalid Time", "2025-07-01", "25:00", False)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    try:
        planner.update_event(event1.event_id, time="30:00")
    except ValueError as e:
        print(f"Caught expected error during update: {e}")

