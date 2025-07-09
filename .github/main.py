import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.db_connection import initialize_database
initialize_database()

from ui.emergency_ui import EmergencyTriageGUI
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    app = EmergencyTriageGUI(root)
    root.mainloop()
