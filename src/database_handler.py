# /database_handler.py

import sqlite3
import mysql.connector
from mysql.connector import errorcode

class SQLiteHandler:
    """Handles all database operations for a SQLite database."""
    
    def __init__(self, db_path):
        """
        Initializes the handler and creates the tasks table if it doesn't exist.
        - db_path (str): The file path for the SQLite database. e.g., 'tasks.db'
        """
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        """Establishes and returns a connection to the database."""
        conn = sqlite3.connect(self.db_path)
        # This allows us to access columns by name
        conn.row_factory = sqlite3.Row
        return conn

    def _create_table(self):
        """Creates the 'tasks' table if it does not already exist."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    description TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    difficulty INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            ''')
            conn.commit()
        finally:
            conn.close()

    def save_task(self, task):
        """Saves a single task to the database."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            task_data = task.to_dict()
            cursor.execute('''
                INSERT INTO tasks (task_id, description, priority, difficulty, created_at, status)
                VALUES (:task_id, :description, :priority, :difficulty, :created_at, :status)
            ''', task_data)
            conn.commit()
        finally:
            conn.close()

    def load_all_tasks(self):
        """Loads all tasks from the database and returns them as a list of dicts."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            # Convert row objects to standard dictionaries
            tasks = [dict(row) for row in cursor.fetchall()]
            return tasks
        finally:
            conn.close()

    def update_task(self, task):
        """Updates an existing task in the database."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            task_data = task.to_dict()
            cursor.execute('''
                UPDATE tasks SET
                    description = :description,
                    priority = :priority,
                    difficulty = :difficulty,
                    status = :status
                WHERE task_id = :task_id
            ''', task_data)
            conn.commit()
        finally:
            conn.close()

    def delete_task(self, task_id):
        """Deletes a task from the database by its ID."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            conn.commit()
        finally:
            conn.close()


class MySQLHandler:
    """Handles all database operations for a MySQL database."""

    def __init__(self, db_config):
        """
        Initializes the handler and connects to the MySQL database.
        - db_config (dict): A dictionary with 'host', 'user', 'password', 'database'.
        """
        self.db_config = db_config
        self.conn = None
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            print("Successfully connected to MySQL database.")
            self._create_table()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist")
            else:
                print(f"Error: {err}")
            self.conn = None

    def _create_table(self):
        """Creates the 'tasks' table if it does not already exist."""
        if not self.conn: return
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id VARCHAR(36) PRIMARY KEY,
                    description TEXT NOT NULL,
                    priority INT NOT NULL,
                    difficulty INT NOT NULL,
                    created_at VARCHAR(50) NOT NULL,
                    status VARCHAR(20) NOT NULL
                )
            ''')
            self.conn.commit()
        finally:
            cursor.close()

    def save_task(self, task):
        """Saves a single task to the database."""
        if not self.conn: return
        cursor = self.conn.cursor()
        try:
            task_data = task.to_dict()
            query = (
                "INSERT INTO tasks "
                "(task_id, description, priority, difficulty, created_at, status) "
                "VALUES (%(task_id)s, %(description)s, %(priority)s, %(difficulty)s, %(created_at)s, %(status)s)"
            )
            cursor.execute(query, task_data)
            self.conn.commit()
        finally:
            cursor.close()

    def load_all_tasks(self):
        """Loads all tasks from the database and returns them as a list of dicts."""
        if not self.conn: return []
        # `dictionary=True` is a convenient way to get results as dicts
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            return tasks
        finally:
            cursor.close()

    def update_task(self, task):
        """Updates an existing task in the database."""
        if not self.conn: return
        cursor = self.conn.cursor()
        try:
            task_data = task.to_dict()
            query = (
                "UPDATE tasks SET "
                "description = %(description)s, priority = %(priority)s, "
                "difficulty = %(difficulty)s, status = %(status)s "
                "WHERE task_id = %(task_id)s"
            )
            cursor.execute(query, task_data)
            self.conn.commit()
        finally:
            cursor.close()

    def delete_task(self, task_id):
        """Deletes a task from the database by its ID."""
        if not self.conn: return
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
            self.conn.commit()
        finally:
            cursor.close()

    def close(self):
        """Closes the database connection."""
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("MySQL connection closed.")