import tkinter as tk
from task_manager import TaskManager
from gui_app import GuiApp
from database_handler import SQLiteHandler, MySQLHandler


def main():
    """
    The main function to set up and run the application.
    """
    # --- Configuration ---
    # Choose your database by setting this variable to 'sqlite' or 'mysql'.
    DATABASE_CHOICE = 'sqlite'

    db_handler = None

    # --- Initialize Database Handler ---
    if DATABASE_CHOICE == 'sqlite':
        # Using SQLite, which stores data in a local file.
        db_path = "my_tasks.db"
        db_handler = SQLiteHandler(db_path)
        print(f"Using SQLite database: {db_path}")

    elif DATABASE_CHOICE == 'mysql':
        # Using MySQL. Make sure you have a MySQL server running and have
        # created a database for this app.
        # Fill in your MySQL connection details below.
        mysql_config = {
            'host': 'localhost',
            'user': 'your_user',  # <--- CHANGE THIS
            'password': 'your_password',  # <--- CHANGE THIS
            'database': 'your_todo_db'  # <--- CHANGE THIS
        }
        db_handler = MySQLHandler(mysql_config)
        if not db_handler.conn:
            print("Failed to connect to MySQL. Exiting.")
            return  # Exit if connection failed
        print(f"Using MySQL database: {mysql_config['database']}")

    else:
        print(f"Error: Invalid database choice '{DATABASE_CHOICE}'. Please choose 'sqlite' or 'mysql'.")
        return

    # --- Initialize Core Components ---
    # 1. Initialize the TaskManager (the backend logic)
    task_manager = TaskManager()

    # 2. Connect the database handler to the manager
    task_manager.set_db_handler(db_handler)

    # 3. Load existing tasks from the database into the manager
    task_manager.load_tasks_from_db()

    # --- Initialize and Run the GUI ---
    # 1. Create the main Tkinter window
    root = tk.Tk()

    # 2. Create an instance of our GUI application class
    app = GuiApp(root, task_manager)

    # 3. Define a graceful shutdown procedure
    def on_closing():
        """Handles the window closing event."""
        print("Closing application...")
        if isinstance(db_handler, MySQLHandler):
            db_handler.close()  # Explicitly close MySQL connection
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 4. Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    # This ensures the main function is called only when the script is executed directly
    main()