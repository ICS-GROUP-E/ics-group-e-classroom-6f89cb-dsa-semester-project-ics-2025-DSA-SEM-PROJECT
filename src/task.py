#Defines the Task class, the central data object used to hold all the information about a single to-do-item
import uuid
from datetime import datetime

class Task:
    """
        Represents a single task in the to-do list.
        Each task has a unique ID, description, priority, difficulty,
        creation timestamp, and a status.
    """
    def __init__(self,description,priority,difficulty,task_id=None,created_at=None,status="pending"):
        """
        Initializes a Task object
        - description (str): The text of the task.
        - priority (int): The priority level (e.g., 1-5, lower is higher).
        - difficulty (int): The difficulty level (e.g., 1-10).
        - task_id (str, optional): A unique identifier. Defaults to a new UUID.
        - created_at (datetime, optional): The creation time. Defaults to now.
        - status (str, optional): 'pending' or 'completed'. Defaults to 'pending'.
        """
        self.task_id = task_id if task_id else str(uuid.uuid4())
        self.description=description
        self.priority=int(priority)
        self.difficulty=int(difficulty)
        self.status=status
        #if created_at is a string from the database, convert it to datetime
        if isinstance(created_at, str):
            self.created_at=datetime.fromisoformat(created_at)
        else:
            if created_at:
                self.created_at=created_at
            else:
                self.created_at=datetime.now()

    def to_dict(self):
        """
        Converts a task object to a dictionary for serialization
        """
        return{
            'task_id':self.task_id,
            'description':self.description,
            'priority':self.priority,
            'difficulty':self.difficulty,
            'created_at':self.created_at.isoformat(),
            'status':self.status
        }

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the task
        """
        return (f"Task(id={self.task_id}, desc='{self.description}', "
                f"priority={self.priority}, difficulty={self.difficulty}, status='{self.status}')")
