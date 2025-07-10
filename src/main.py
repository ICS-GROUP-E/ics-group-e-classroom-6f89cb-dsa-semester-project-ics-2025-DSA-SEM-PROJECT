#!/usr/bin/env python3
"""
Main entry point for the Event Planner Application.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to start the Event Planner application."""
    try:
        from ui.gui import EventPlannerGUI
        import tkinter as tk
        
        # Create and start the GUI application
        root = tk.Tk()
        app = EventPlannerGUI(root)
        
        # Configure window close behavior
        root.protocol("WM_DELETE_WINDOW", app._on_closing)
        
        # Start the application
        root.mainloop()
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Please ensure all required modules are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
