import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import datetime
import threading
import time
import logging

# Configure basic logging for the GUI part
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the EventPlanner logic and DBManager
try:
    from core.event_planner import EventPlanner, Event, LLNode
    from database.db_manager import DBManager
except ImportError as e:
    logger.error(f"Failed to import backend modules: {e}")
    messagebox.showerror("Import Error", "Could not load backend modules. "
                                        "Ensure 'event_planner_integrated.py' and 'event_planner_db.py' "
                                        "are in the same directory.")
    exit() # Exit if core modules cannot be imported

class EventPlannerGUI:
    def __init__(self, master: tk.Tk):
        """
        Initializes the Event Planner GUI application.
        :param master: The root Tkinter window.
        """
        self.master = master
        master.title("Event Planner")
        master.geometry("500x700") # Increased size for better layout
        master.protocol("WM_DELETE_WINDOW", self._on_closing) # Handle window close event

        # Initialize DB Manager and load max event ID
        self.db_manager = DBManager()
        max_id = self.db_manager.get_max_event_id()
        self.planner = EventPlanner(initial_event_id_counter=max_id + 1)
        
        # --- Status Bar (Initialize early as it's used during loading) ---
        self.status_label = ttk.Label(master, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self._load_data_from_db() # Load existing events and tasks from DB (now status_label exists)

        # --- Main Notebook (Tabs) ---
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Events Tab ---
        self.events_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.events_frame, text="Events")
        self._setup_events_tab()

        # --- Tasks Tab ---
        self.tasks_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tasks_frame, text="Tasks")
        self._setup_tasks_tab()

        # --- Reminders Tab ---
        self.reminders_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.reminders_frame, text="Reminders")
        self._setup_reminders_tab()

        # --- Undo History Tab ---
        self.undo_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.undo_frame, text="Undo History")
        self._setup_undo_tab()

        # Start periodic reminder check
        self._check_reminders_periodic()
        self.master.after(1000, self._update_all_displays) # Initial display update (now all widgets exist)
        
        # --- Report Generation Button ---
        self._setup_report_button()

    def _setup_events_tab(self):
        """Sets up the UI elements for the Events tab."""
        # --- Input Frame ---
        input_frame = ttk.LabelFrame(self.events_frame, text="Event Details", padding="10")
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Define labels and their corresponding dictionary keys explicitly
        labels_and_keys = [
            ("Name:", "name"),
            ("Location:", "location"),
            ("Description:", "description"),
            ("Attendees (comma-sep):", "attendees")
        ]
        self.entries = {}
        row = 0
        
        # Regular text entries
        for label_text, key in labels_and_keys:
            ttk.Label(input_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)
            entry = ttk.Entry(input_frame, width=50)
            entry.grid(row=row, column=1, sticky=tk.EW, pady=2, padx=5)
            self.entries[key] = entry
            row += 1
        
        # Date picker with dropdowns
        ttk.Label(input_frame, text="Date:").grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)
        date_frame = ttk.Frame(input_frame)
        date_frame.grid(row=row, column=1, sticky=tk.W, pady=2, padx=5)
        
        # Year dropdown
        current_year = datetime.datetime.now().year
        years = list(range(current_year, current_year + 5))
        self.year_var = tk.StringVar(value=str(current_year))
        year_combo = ttk.Combobox(date_frame, textvariable=self.year_var, values=years, width=8, state="readonly")
        year_combo.pack(side=tk.LEFT, padx=2)
        
        # Month dropdown
        months = [(f"{i:02d}", datetime.datetime(2000, i, 1).strftime("%B")) for i in range(1, 13)]
        month_values = [f"{num} - {name}" for num, name in months]
        self.month_var = tk.StringVar(value=f"{datetime.datetime.now().month:02d} - {datetime.datetime.now().strftime('%B')}")
        month_combo = ttk.Combobox(date_frame, textvariable=self.month_var, values=month_values, width=12, state="readonly")
        month_combo.pack(side=tk.LEFT, padx=2)
        
        # Day dropdown
        days = [f"{i:02d}" for i in range(1, 32)]
        self.day_var = tk.StringVar(value=f"{datetime.datetime.now().day:02d}")
        day_combo = ttk.Combobox(date_frame, textvariable=self.day_var, values=days, width=5, state="readonly")
        day_combo.pack(side=tk.LEFT, padx=2)
        row += 1
        
        # Time picker with dropdowns
        ttk.Label(input_frame, text="Time:").grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)
        time_frame = ttk.Frame(input_frame)
        time_frame.grid(row=row, column=1, sticky=tk.W, pady=2, padx=5)
        
        # Hour dropdown
        hours = [f"{i:02d}" for i in range(24)]
        self.hour_var = tk.StringVar(value="09")
        hour_combo = ttk.Combobox(time_frame, textvariable=self.hour_var, values=hours, width=5, state="readonly")
        hour_combo.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(time_frame, text=":").pack(side=tk.LEFT)
        
        # Minute dropdown (allows custom input)
        minutes = [f"{i:02d}" for i in range(0, 60, 15)]  # 15-minute intervals as suggestions
        self.minute_var = tk.StringVar(value="00")
        minute_combo = ttk.Combobox(time_frame, textvariable=self.minute_var, values=minutes, width=5)
        minute_combo.pack(side=tk.LEFT, padx=2)
        
        # Add validation for minute input (0-59)
        def validate_minute(value):
            if value == "":
                return True  # Allow empty for editing
            try:
                minute_val = int(value)
                return 0 <= minute_val <= 59
            except ValueError:
                return False
        
        minute_combo.configure(validate="key", validatecommand=(self.master.register(validate_minute), "%P"))
        row += 1

        # Reminder Checkbox
        self.reminder_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Set Reminder", variable=self.reminder_var).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5, padx=5)

        # --- Buttons Frame ---
        button_frame = ttk.Frame(self.events_frame, padding="5")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Add Event", command=self._create_event).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Event", command=self._update_event).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Event", command=self._delete_event).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self._clear_event_entry_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh Display", command=lambda: self._display_events(filter_upcoming=True)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save All Data", command=self._save_all_data_to_db).pack(side=tk.LEFT, padx=5) # Added Save button

        # --- Event List Treeview ---
        tree_frame = ttk.Frame(self.events_frame, padding="5")
        tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("ID", "Name", "Date", "Time", "Location", "Reminder", "Description", "Attendees")
        self.event_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.event_tree.heading(col, text=col, anchor=tk.W)
            self.event_tree.column(col, width=100, anchor=tk.W)
        self.event_tree.column("ID", width=50)
        self.event_tree.column("Name", width=150)
        self.event_tree.column("Date", width=90)
        self.event_tree.column("Time", width=70)
        self.event_tree.column("Location", width=120)
        self.event_tree.column("Reminder", width=70)
        self.event_tree.column("Description", width=200) # Wider for description
        self.event_tree.column("Attendees", width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.event_tree.yview)
        self.event_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.event_tree.pack(side="left", fill="both", expand=True)

        self.event_tree.bind("<<TreeviewSelect>>", self._load_selected_event_details)

        # Initial display - show all events by default
        self._display_events(filter_upcoming=False)

    def _setup_report_button(self):
        """Sets up the report generation button."""
        button_frame = ttk.Frame(self.master, padding="5")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="Generate Report", command=self._generate_report).pack(side=tk.LEFT, padx=5)

    def _generate_report(self):
        """Generates a report of data structure executions."""
        from reports import DataStructureReportGenerator
        import datetime
        
        # Ask user where to save the PDF
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"data_structure_report_{timestamp}.pdf"
        
        file_path = filedialog.asksaveasfilename(
            title="Save Report As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if not file_path:  # User cancelled the dialog
            return
        
        # Initialize report generator
        report_generator = DataStructureReportGenerator(self.planner)

        try:
            # Generate report with user-specified filename
            report_path = report_generator.generate_comprehensive_report(file_path)
            messagebox.showinfo("Report Generated", f"Report saved successfully as:\n{report_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def _setup_tasks_tab(self):
        # --- Event Selection for Tasks ---
        event_select_frame = ttk.LabelFrame(self.tasks_frame, text="Select Event for Tasks", padding="10")
        event_select_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(event_select_frame, text="Select an Event from the 'Events' tab to manage its tasks.").pack(pady=5)
        self.selected_event_for_tasks_label = ttk.Label(event_select_frame, text="No Event Selected", font=("Arial", 10, "bold"))
        self.selected_event_for_tasks_label.pack(pady=5)

        # --- Task Input ---
        task_input_frame = ttk.LabelFrame(self.tasks_frame, text="Task Details", padding="10")
        task_input_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(task_input_frame, text="Task Description:").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        self.task_entry = ttk.Entry(task_input_frame, width=50)
        self.task_entry.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=5)

        # --- Task Buttons ---
        task_button_frame = ttk.Frame(self.tasks_frame, padding="5")
        task_button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(task_button_frame, text="Add Task", command=self._add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(task_button_frame, text="Remove Selected Task", command=self._remove_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(task_button_frame, text="Mark Selected Task Complete", command=self._mark_task_complete).pack(side=tk.LEFT, padx=5)

        # --- Task List Treeview ---
        task_list_frame = ttk.Frame(self.tasks_frame, padding="5")
        task_list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.task_tree = ttk.Treeview(task_list_frame, columns=("Task", "Completed"), show="headings")
        self.task_tree.heading("Task", text="Task Description", anchor=tk.W)
        self.task_tree.column("Task", width=400, anchor=tk.W)
        self.task_tree.heading("Completed", text="Completed", anchor=tk.W)
        self.task_tree.column("Completed", width=100, anchor=tk.CENTER)

        task_scrollbar = ttk.Scrollbar(task_list_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=task_scrollbar.set)
        task_scrollbar.pack(side="right", fill="y")
        self.task_tree.pack(side="left", fill="both", expand=True)

        # Variable to hold the ID of the event whose tasks are currently displayed
        self.current_event_tasks_id = None
        
        # Track events that have already been warned about to avoid spam
        self.warned_events = set()

    def _setup_reminders_tab(self):
        """Sets up the UI elements for the Reminders tab."""
        ttk.Label(self.reminders_frame, text="Current Reminder Queue:").pack(pady=5, anchor=tk.W)
        self.reminder_listbox = tk.Listbox(self.reminders_frame, height=15, width=80)
        self.reminder_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        reminder_scrollbar = ttk.Scrollbar(self.reminders_frame, orient="vertical", command=self.reminder_listbox.yview)
        self.reminder_listbox.config(yscrollcommand=reminder_scrollbar.set)
        reminder_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._display_reminder_queue()

    def _setup_undo_tab(self):
        """Sets up the UI elements for the Undo History tab."""
        button_frame = ttk.Frame(self.undo_frame, padding="10")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="Undo Last Action", command=self._undo_last_action).pack(pady=5)

        ttk.Label(self.undo_frame, text="Recent Edit History (Last 10 actions):").pack(pady=5, anchor=tk.W)
        self.undo_listbox = tk.Listbox(self.undo_frame, height=15, width=80)
        self.undo_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        undo_scrollbar = ttk.Scrollbar(self.undo_frame, orient="vertical", command=self.undo_listbox.yview)
        self.undo_listbox.config(yscrollcommand=undo_scrollbar.set)
        undo_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._display_edit_history()

    # --- Event Tab Methods ---
    def _get_event_input(self) -> dict:
        """Collects event details from entry fields."""
        # Extract date from dropdowns
        year = self.year_var.get()
        month = self.month_var.get().split(" - ")[0]  # Extract month number from "MM - MonthName"
        day = self.day_var.get()
        date_str = f"{year}-{month}-{day}"
        
        # Extract time from dropdowns
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        
        # Ensure minute is properly formatted (add leading zero if needed)
        try:
            minute_val = int(minute)
            if 0 <= minute_val <= 59:
                minute = f"{minute_val:02d}"
            else:
                raise ValueError(f"Invalid minute value: {minute}")
        except ValueError:
            # If minute is invalid, default to 00
            minute = "00"
            
        time_str = f"{hour}:{minute}"
        
        return {
            "name": self.entries["name"].get(),
            "date": date_str,
            "time": time_str,
            "location": self.entries["location"].get(),
            "description": self.entries["description"].get(),
            "attendees": self.entries["attendees"].get(),
            "reminder_set": self.reminder_var.get()
        }

    def _clear_event_entry_fields(self):
        """Clears all event input fields."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.reminder_var.set(False)
        
        # Reset date dropdowns to current date
        current_date = datetime.datetime.now()
        self.year_var.set(str(current_date.year))
        self.month_var.set(f"{current_date.month:02d} - {current_date.strftime('%B')}")
        self.day_var.set(f"{current_date.day:02d}")
        
        # Reset time dropdowns to default
        self.hour_var.set("09")
        self.minute_var.set("00")
        # The selection should remain when loading details. Deselection should be explicit.

    def _create_event(self):
        """Handles the 'Add Event' button click."""
        event_data = self._get_event_input()
        try:
            new_event = self.planner.create_event(**event_data)
            self.db_manager.save_event(new_event)
            self._save_tasks_to_db_for_event(new_event.event_id) # Save initial empty task list
            self._show_message("Success", f"Event '{new_event.name}' added successfully with ID: {new_event.event_id}")
            self._clear_event_entry_fields()
            self.event_tree.selection_remove(self.event_tree.selection()) # Explicitly deselect after creation
            self._update_all_displays()
        except ValueError as e:
            self._show_message("Input Error", str(e))
        except Exception as e:
            logger.error(f"Error creating event: {e}", exc_info=True)
            self._show_message("Error", f"Failed to add event: {e}")

    def _update_event(self):
        """Handles the 'Update Event' button click."""
        selected_item = self.event_tree.selection()
        if not selected_item:
            self._show_message("Selection Error", "Please select an event to update.")
            return

        event_id = int(self.event_tree.item(selected_item, "values")[0])
        event_data = self._get_event_input() # Get updated data from fields

        try:
            updated_event = self.planner.update_event(event_id, **event_data)
            if updated_event:
                self.db_manager.save_event(updated_event)
                self._show_message("Success", f"Event ID {event_id} updated successfully.")
                self._clear_event_entry_fields()
                self.event_tree.selection_remove(self.event_tree.selection()) # Explicitly deselect after update
                self._update_all_displays()
            else:
                self._show_message("Error", f"Failed to update event ID {event_id}.")
        except ValueError as e:
            self._show_message("Input Error", str(e))
        except Exception as e:
            logger.error(f"Error updating event {event_id}: {e}", exc_info=True)
            self._show_message("Error", f"Failed to update event: {e}")

    def _delete_event(self):
        """Handles the 'Delete Event' button click."""
        selected_item = self.event_tree.selection()
        if not selected_item:
            self._show_message("Selection Error", "Please select an event to delete.")
            return

        event_id = int(self.event_tree.item(selected_item, "values")[0])
        event_name = self.event_tree.item(selected_item, "values")[1]

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{event_name}' (ID: {event_id})?"):
            try:
                if self.planner.delete_event(event_id):
                    self.db_manager.delete_event(event_id) # Delete from DB
                    self._show_message("Success", f"Event '{event_name}' deleted successfully.")
                    self._clear_event_entry_fields()
                    self.event_tree.selection_remove(self.event_tree.selection()) # Explicitly deselect after deletion
                    self._update_all_displays()
                else:
                    self._show_message("Error", f"Failed to delete event ID {event_id}.")
            except Exception as e:
                logger.error(f"Error deleting event {event_id}: {e}", exc_info=True)
                self._show_message("Error", f"Failed to delete event: {e}")

    def _load_selected_event_details(self, event=None):
        """Loads details of the selected event into the input fields."""
        selected_item = self.event_tree.selection()
        if not selected_item:
            self._clear_event_entry_fields()
            self.current_event_tasks_id = None
            self.selected_event_for_tasks_label.config(text="No Event Selected")
            self._display_tasks_for_selected_event() # Clear tasks display
            return

        values = self.event_tree.item(selected_item, "values")
        event_id = int(values[0])
        
        # Clear fields first (but not selection)
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.reminder_var.set(False)

        # Populate text fields
        self.entries["name"].insert(0, values[1])
        self.entries["location"].insert(0, values[4])
        self.reminder_var.set(values[5] == "True") # Convert string "True"/"False" to boolean
        self.entries["description"].insert(0, values[6])
        self.entries["attendees"].insert(0, values[7])
        
        # Populate date dropdowns
        date_parts = values[2].split("-")  # Split YYYY-MM-DD
        if len(date_parts) == 3:
            year, month, day = date_parts
            self.year_var.set(year)
            month_name = datetime.datetime(int(year), int(month), 1).strftime('%B')
            self.month_var.set(f"{month} - {month_name}")
            self.day_var.set(day)
        
        # Populate time dropdowns
        time_parts = values[3].split(":")  # Split HH:MM
        if len(time_parts) == 2:
            hour, minute = time_parts
            self.hour_var.set(hour)
            self.minute_var.set(minute)

        # Set selected event for tasks tab
        self.current_event_tasks_id = event_id
        self.selected_event_for_tasks_label.config(text=f"Selected Event: {values[1]} (ID: {event_id})")
        self._display_tasks_for_selected_event() # Update tasks display

    def _display_events(self, filter_upcoming: bool = True):
        """
        Populates the event Treeview with events from the planner.
        :param filter_upcoming: True for upcoming events, False for all events.
        """
        # Clear existing items
        for item in self.event_tree.get_children():
            self.event_tree.delete(item)

        events_to_display = self.planner.view_events(upcoming=filter_upcoming)
        for event in events_to_display:
            self.event_tree.insert("", tk.END, values=(
                event.event_id,
                event.name,
                event.date,
                event.time,
                event.location,
                str(event.reminder_set), # Store as string for Treeview
                event.description,
                event.attendees
            ))
        self.status_label.config(text=f"Displayed {len(events_to_display)} events.")

    # --- Task Tab Methods ---
    def _add_task(self):
        """Adds a task to the selected event's linked list."""
        if self.current_event_tasks_id is None:
            self._show_message("Selection Error", "Please select an event in the 'Events' tab first.")
            return
        
        task_desc = self.task_entry.get().strip()
        if not task_desc:
            self._show_message("Input Error", "Task description cannot be empty.")
            return
        
        try:
            if self.planner.add_task(self.current_event_tasks_id, task_desc):
                self._save_tasks_to_db_for_event(self.current_event_tasks_id)
                self._show_message("Success", f"Task '{task_desc}' added.")
                self.task_entry.delete(0, tk.END)
                self._display_tasks_for_selected_event()
            else:
                self._show_message("Error", "Failed to add task.")
        except Exception as e:
            logger.error(f"Error adding task: {e}", exc_info=True)
            self._show_message("Error", f"Failed to add task: {e}")

    def _remove_task(self):
        """Removes the selected task from the event's linked list."""
        if self.current_event_tasks_id is None:
            self._show_message("Selection Error", "Please select an event in the 'Events' tab first.")
            return
        
        selected_item = self.task_tree.selection()
        if not selected_item:
            self._show_message("Selection Error", "Please select a task to remove.")
            return
        
        task_desc = self.task_tree.item(selected_item, "values")[0]
        
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove task '{task_desc}'?"):
            try:
                if self.planner.remove_task(self.current_event_tasks_id, task_desc):
                    self._save_tasks_to_db_for_event(self.current_event_tasks_id)
                    self._show_message("Success", f"Task '{task_desc}' removed.")
                    self._display_tasks_for_selected_event()
                else:
                    self._show_message("Error", "Failed to remove task.")
            except Exception as e:
                logger.error(f"Error removing task: {e}", exc_info=True)
                self._show_message("Error", f"Failed to remove task: {e}")

    def _mark_task_complete(self):
        """Marks the selected task as complete."""
        if self.current_event_tasks_id is None:
            self._show_message("Selection Error", "Please select an event in the 'Events' tab first.")
            return
        
        selected_item = self.task_tree.selection()
        if not selected_item:
            self._show_message("Selection Error", "Please select a task to mark complete.")
            return
        
        task_desc = self.task_tree.item(selected_item, "values")[0]
        
        try:
            if self.planner.mark_task_complete(self.current_event_tasks_id, task_desc):
                self._save_tasks_to_db_for_event(self.current_event_tasks_id)
                self._show_message("Success", f"Task '{task_desc}' marked complete.")
                self._display_tasks_for_selected_event()
            else:
                self._show_message("Error", "Failed to mark task complete.")
        except Exception as e:
            logger.error(f"Error marking task complete: {e}", exc_info=True)
            self._show_message("Error", f"Failed to mark task complete: {e}")

    def _display_tasks_for_selected_event(self):
        """Displays tasks for the currently selected event in the task Treeview."""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        if self.current_event_tasks_id is not None:
            tasks = self.planner.get_tasks(self.current_event_tasks_id)
            for task_data in tasks:
                self.task_tree.insert("", tk.END, values=(task_data["task"], "Yes" if task_data["completed"] else "No"))
        else:
            self.task_tree.insert("", tk.END, values=("No event selected", ""))

    # --- Reminder Tab Methods ---
    def _process_reminders_gui(self):
        """Triggers reminder processing and updates the display."""
        try:
            processed_for_removal, ten_min_reminders = self.planner.process_reminders()
            
            # Show specific 10-minute reminders as pop-ups
            if ten_min_reminders:
                for event in ten_min_reminders:
                    if event.event_id not in self.warned_events:
                        messagebox.showwarning("Event Notification", 
                                             f"Reminder: {event.name} starts in 10 minutes!\nDate: {event.date}\nTime: {event.time}")
                        self.warned_events.add(event.event_id)
                        logger.info(f"10-minute warning shown for event: {event.name}")
            
            # Update status bar for processed reminders
            if processed_for_removal: 
                valid_names = [e.name for e in processed_for_removal if hasattr(e, 'name')]
                if valid_names:
                    names = ", ".join(valid_names)
                    self.status_label.config(text=f"Processed reminders for: {names}")
                else:
                    self.status_label.config(text="Processed some reminders.")
            else:
                self.status_label.config(text="No reminders to process at this time.")

            self._display_reminder_queue() # Always update the listbox
        except Exception as e:
            logger.error(f"Error processing reminders: {e}", exc_info=True)
            self._show_message("Error", f"Failed to process reminders: {e}")

    def _display_reminder_queue(self):
        """Populates the reminder listbox."""
        self.reminder_listbox.delete(0, tk.END)
        reminders = self.planner.view_reminder_queue()
        if not reminders:
            self.reminder_listbox.insert(tk.END, "No reminders in queue.")
        else:
            for event in reminders:
                self.reminder_listbox.insert(tk.END, f"ID: {event.event_id} - {event.name} on {event.date} at {event.time}")

    def _check_reminders_periodic(self):
        """Periodically checks and processes reminders."""
        self._process_reminders_gui() # This handles both reminder processing and 10-minute warnings
        # Schedule the next check in 60 seconds (60000 milliseconds)
        self.master.after(60000, self._check_reminders_periodic)


    # --- Undo Tab Methods ---
    def _undo_last_action(self):
        """Handles the 'Undo Last Action' button click."""
        try:
            undone_event = self.planner.undo_last_edit()
            if undone_event:
                self.db_manager.save_event(undone_event) # Save the restored state
                self._show_message("Undo Success", f"Last action undone. Event ID {undone_event.event_id} restored.")
            else:
                # If undo returns None, it might mean a creation was undone, or no action to undo
                self._show_message("Undo Info", "No more actions to undo or a creation was undone.")
            self._update_all_displays()
        except Exception as e:
            logger.error(f"Error during undo: {e}", exc_info=True)
            self._show_message("Error", f"Failed to undo: {e}")

    def _display_edit_history(self):
        """Populates the undo history listbox."""
        self.undo_listbox.delete(0, tk.END)
        history = self.planner.view_edited_events()
        if not history:
            self.undo_listbox.insert(tk.END, "No edit history.")
        else:
            # Display in reverse chronological order (most recent first)
            for event_state in reversed(history):
                self.undo_listbox.insert(tk.END, f"ID: {event_state.event_id} - {event_state.name} ({event_state.date} {event_state.time})")

    # --- Persistence and General Methods ---
    def _load_data_from_db(self):
        """Loads all events and their tasks from the database into the EventPlanner."""
        logger.info("Loading data from database...")
        try:
            events_from_db = self.db_manager.load_events()
            for event_data in events_from_db:
                # Use the special loading method to avoid side effects
                self.planner._add_event_for_loading(event_data)
                # Load tasks for each event
                tasks_ll_head = self.db_manager.load_tasks(event_data.event_id)
                self.planner.todo_lists[event_data.event_id] = tasks_ll_head
                
            logger.info(f"Loaded {len(events_from_db)} events and their tasks from DB.")
            self.status_label.config(text=f"Loaded {len(events_from_db)} events from database.")
        except Exception as e:
            logger.error(f"Error loading data from DB: {e}", exc_info=True)
            self._show_message("Database Error", f"Failed to load data from database: {e}")

    def _save_all_data_to_db(self):
        """Saves all current events and their tasks from the EventPlanner to the database."""
        logger.info("Saving all data to database...")
        try:
            # Get all events (upcoming and past) to ensure all are saved
            all_events = self.planner.view_events(upcoming=False) + self.planner.view_events(upcoming=True)
            # Filter out duplicates (view_events might return overlapping sets if an event is both upcoming/past based on current time)
            unique_event_ids = set()
            unique_events = []
            for event in all_events:
                if event.event_id not in unique_event_ids:
                    unique_events.append(event)
                    unique_event_ids.add(event.event_id)

            for event in unique_events:
                self.db_manager.save_event(event)
                # Save tasks for each event
                tasks_ll_head = self.planner.todo_lists.get(event.event_id)
                self.db_manager.save_tasks(event.event_id, tasks_ll_head)
            logger.info(f"Saved {len(unique_events)} events and their tasks to DB.")
            self.status_label.config(text=f"Saved {len(unique_events)} events to database.")
            self._show_message("Save Success", "All data saved successfully!") # Confirmation message
        except Exception as e:
            logger.error(f"Error saving data to DB: {e}", exc_info=True)
            self._show_message("Database Error", f"Failed to save data to database: {e}")

    def _save_tasks_to_db_for_event(self, event_id: int):
        """Saves tasks for a specific event to the database."""
        try:
            tasks_ll_head = self.planner.todo_lists.get(event_id)
            self.db_manager.save_tasks(event_id, tasks_ll_head)
            logger.debug(f"Tasks for event {event_id} saved to DB.")
        except Exception as e:
            logger.error(f"Error saving tasks for event {event_id}: {e}", exc_info=True)
            self._show_message("Database Error", f"Failed to save tasks for event {event_id}: {e}")

    def _on_closing(self):
        """Handles the window closing event, saving data and closing DB connection."""
        if messagebox.askyesno("Quit", "Do you want to save changes before quitting?"):
            self._save_all_data_to_db()
        self.db_manager.close()
        self.master.destroy()

    def _show_message(self, title: str, message: str):
        """Displays a message box to the user."""
        messagebox.showinfo(title, message)

    def _update_all_displays(self):
        """Refreshes all relevant display areas in the GUI."""
        # Show all events (both upcoming and past) to ensure deleted events disappear
        self._display_events(filter_upcoming=False) 
        self._display_reminder_queue()
        self._display_edit_history()
        # Only update tasks display if an event is currently selected
        if self.current_event_tasks_id:
            self._display_tasks_for_selected_event()


# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = EventPlannerGUI(root)
    root.mainloop()

