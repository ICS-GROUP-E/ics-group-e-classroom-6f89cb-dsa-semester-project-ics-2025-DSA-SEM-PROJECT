import sys
import os

# ✅ Add 'src' to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# ✅ Now import from ui directly (no "src.")
from ui.emergency_ui import EmergencyTriageGUI

from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    app = EmergencyTriageGUI(root)
    root.mainloop()
