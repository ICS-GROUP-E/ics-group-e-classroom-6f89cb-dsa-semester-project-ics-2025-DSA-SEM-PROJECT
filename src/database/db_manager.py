import sqlite3
import json
from typing import List, Optional
import logging
from dataclasses import dataclass

# Assuming Event and LLNode classes are available from event_planner_integrated.py
# In a real application, you might put these into a separate 'models.py' file
# and import them from there. For this setup, we'll assume they are accessible
# or you will copy-paste them into this file if running standalone.
# For now, we'll import them directly, assuming event_planner_integrated.py is in the same directory.
try:
    from core.event_planner import Event, logger as app_logger # Import Event and logger
    from data_structures.linked_list import LLNode # Import LLNode
except ImportError:
    # Fallback for standalone testing or if classes are defined elsewhere
    logging.warning("Could not import Event and LLNode from event_planner_integrated.py. "
                    "Ensure the file is in the same directory or define them here for testing.")
    # Define dummy classes for testing this file in isolation if needed
    @dataclass
    class Event:
        event_id: int
        name: str
        date: str
        time: str
        reminder_set: bool
        location: str = ""
        description: str = ""
        attendees: str = ""

    class LLNode:
        def __init__(self, data: str, completed: bool = False):
            self.data = data
            self.completed = completed
            self.next = None
    
    # Use a local logger if app_logger is not available
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    app_logger = logging.getLogger(__name__)


class DBManager:
    def __init__(self, db_name: str = "events.db"):
        """
        Initializes the database manager and connects to the SQLite database.
        Creates the 'events' and 'tasks' tables if they do not exist.
        :param db_name: The name of the SQLite database file.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
        app_logger.info(f"Database manager initialized for {self.db_name}")

    def _connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            app_logger.debug(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            app_logger.error(f"Error connecting to database {self.db_name}: {e}")
            raise

    def _create_tables(self):
        """Creates the 'events' and 'tasks' tables if they don't already exist."""
        try:
            # Events table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    event_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    reminder_set INTEGER NOT NULL, -- SQLite stores booleans as 0 or 1
                    location TEXT,
                    description TEXT,
                    attendees TEXT
                )
            """)
            # Tasks table (associated with events)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER NOT NULL,
                    task_description TEXT NOT NULL,
                    completed INTEGER NOT NULL,
                    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
                )
            """)
            self.conn.commit()
            app_logger.info("Database tables checked/created.")
        except sqlite3.Error as e:
            app_logger.error(f"Error creating tables: {e}")
            raise

    def save_event(self, event: Event):
        """
        Inserts a new event or updates an existing one in the database.
        :param event: The Event object to save.
        """
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO events (event_id, name, date, time, reminder_set, location, description, attendees)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.event_id, event.name, event.date, event.time, 
                1 if event.reminder_set else 0, # Convert boolean to integer
                event.location, event.description, event.attendees
            ))
            self.conn.commit()
            app_logger.info(f"Event ID {event.event_id} saved/updated in DB.")
        except sqlite3.Error as e:
            app_logger.error(f"Error saving event {event.event_id}: {e}")
            self.conn.rollback()
            raise

    def load_events(self) -> List[Event]:
        """
        Loads all events from the database.
        :return: A list of Event objects.
        """
        events = []
        try:
            self.cursor.execute("SELECT event_id, name, date, time, reminder_set, location, description, attendees FROM events")
            rows = self.cursor.fetchall()
            for row in rows:
                event = Event(
                    event_id=row[0],
                    name=row[1],
                    date=row[2],
                    time=row[3],
                    reminder_set=bool(row[4]), # Convert integer back to boolean
                    location=row[5],
                    description=row[6],
                    attendees=row[7]
                )
                events.append(event)
            app_logger.info(f"Loaded {len(events)} events from DB.")
        except sqlite3.Error as e:
            app_logger.error(f"Error loading events: {e}")
            raise
        return events

    def delete_event(self, event_id: int):
        """
        Deletes an event and all its associated tasks from the database.
        :param event_id: The ID of the event to delete.
        """
        try:
            self.cursor.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
            # ON DELETE CASCADE in tasks table definition handles task deletion automatically
            self.conn.commit()
            app_logger.info(f"Event ID {event_id} and its tasks deleted from DB.")
        except sqlite3.Error as e:
            app_logger.error(f"Error deleting event {event_id}: {e}")
            self.conn.rollback()
            raise

    def save_tasks(self, event_id: int, tasks_ll_head: Optional[LLNode]):
        """
        Saves the linked list of tasks for a given event to the database.
        It first deletes all existing tasks for the event, then inserts the new ones.
        :param event_id: The ID of the event to save tasks for.
        :param tasks_ll_head: The head of the LLNode linked list for tasks.
        """
        try:
            # Delete existing tasks for this event
            self.cursor.execute("DELETE FROM tasks WHERE event_id = ?", (event_id,))
            
            current_node = tasks_ll_head
            while current_node:
                self.cursor.execute("""
                    INSERT INTO tasks (event_id, task_description, completed)
                    VALUES (?, ?, ?)
                """, (event_id, current_node.data, 1 if current_node.completed else 0))
                current_node = current_node.next
            self.conn.commit()
            app_logger.info(f"Tasks for Event ID {event_id} saved to DB.")
        except sqlite3.Error as e:
            app_logger.error(f"Error saving tasks for event {event_id}: {e}")
            self.conn.rollback()
            raise

    def load_tasks(self, event_id: int) -> Optional[LLNode]:
        """
        Loads tasks for a given event from the database and reconstructs the linked list.
        :param event_id: The ID of the event to load tasks for.
        :return: The head of the LLNode linked list, or None if no tasks.
        """
        head = None
        tail = None
        try:
            self.cursor.execute("SELECT task_description, completed FROM tasks WHERE event_id = ?", (event_id,))
            rows = self.cursor.fetchall()
            for row in rows:
                new_node = LLNode(data=row[0], completed=bool(row[1]))
                if head is None:
                    head = new_node
                    tail = new_node
                else:
                    tail.next = new_node
                    tail = new_node
            app_logger.info(f"Loaded {len(rows)} tasks for Event ID {event_id}.")
        except sqlite3.Error as e:
            app_logger.error(f"Error loading tasks for event {event_id}: {e}")
            raise
        return head

    def get_max_event_id(self) -> int:
        """
        Retrieves the maximum event_id currently in the database.
        Useful for initializing the event_id_counter in EventPlanner.
        :return: The maximum event ID, or 0 if no events exist.
        """
        try:
            self.cursor.execute("SELECT MAX(event_id) FROM events")
            max_id = self.cursor.fetchone()[0]
            return max_id if max_id is not None else 0
        except sqlite3.Error as e:
            app_logger.error(f"Error getting max event ID: {e}")
            return 0 # Return 0 or raise, depending on desired error handling

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            app_logger.info("Database connection closed.")

# Example usage for testing DBManager
if __name__ == "__main__":
    db_manager = DBManager(db_name="test_events.db")

    # Create dummy events for testing
    from dataclasses import dataclass # Ensure Event is defined for standalone test
    @dataclass
    class Event:
        event_id: int
        name: str
        date: str
        time: str
        reminder_set: bool
        location: str = ""
        description: str = ""
        attendees: str = ""

    # Test Save Event
    print("\n--- Testing Save Event ---")
    event_a = Event(1, "Meeting Alpha", "2025-07-15", "09:00", True, "Room 1", "Discuss project A", "John, Jane")
    event_b = Event(2, "Workshop Beta", "2025-07-16", "11:00", False, "Online", "Training session", "Team")
    db_manager.save_event(event_a)
    db_manager.save_event(event_b)

    # Test Load Events
    print("\n--- Testing Load Events ---")
    loaded_events = db_manager.load_events()
    for e in loaded_events:
        print(f"Loaded Event: ID={e.event_id}, Name={e.name}, Date={e.date}, Reminder={e.reminder_set}")

    # Test Update Event
    print("\n--- Testing Update Event ---")
    event_a.name = "Meeting Alpha (Revised)"
    event_a.reminder_set = False
    db_manager.save_event(event_a)
    reloaded_event_a = [e for e in db_manager.load_events() if e.event_id == event_a.event_id][0]
    print(f"Updated Event A: Name={reloaded_event_a.name}, Reminder={reloaded_event_a.reminder_set}")

    # Test Save and Load Tasks
    print("\n--- Testing Tasks ---")
    # Create a linked list for event_a
    task1 = LLNode("Prepare slides", False)
    task2 = LLNode("Send invites", True)
    task1.next = task2
    db_manager.save_tasks(event_a.event_id, task1)

    loaded_tasks = db_manager.load_tasks(event_a.event_id)
    current_task = loaded_tasks
    print(f"Tasks for Event {event_a.event_id}:")
    while current_task:
        print(f"- {current_task.data} (Completed: {current_task.completed})")
        current_task = current_task.next

    # Test Delete Event
    print("\n--- Testing Delete Event ---")
    db_manager.delete_event(event_b.event_id)
    loaded_events_after_delete = db_manager.load_events()
    print(f"Events after deleting Event B: {[e.name for e in loaded_events_after_delete]}")
    
    # Verify tasks are also deleted (due to ON DELETE CASCADE)
    loaded_tasks_after_event_delete = db_manager.load_tasks(event_b.event_id)
    print(f"Tasks for deleted Event B: {loaded_tasks_after_event_delete}") # Should be None

    # Test get_max_event_id
    print("\n--- Testing Max Event ID ---")
    max_id = db_manager.get_max_event_id()
    print(f"Max event ID in DB: {max_id}")

    db_manager.close()
    print("\nDatabase operations completed and connection closed.")

