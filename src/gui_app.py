import tkinter as tk
from tkinter import ttk , messagebox

class GuiApp:

    """
    This is the main GUI for the TO-DO list application
    Here, users can render the window, widgets,  user interactions and communicates with the Task Manager to perform actions

    """
    def __init__(self , master , task_manager):
        """
        Initializes the GUI
        -master:The root of the Tkinter window
        -task_manager: An instance of the TaskManager class to handle task operations
        """
        self.master = master
        self.task_manager = task_manager

        self.master.title("TO-DO List Application")
        self.master.geometry("1000x600")

        #Configuring the main Frame
        self.main_frame = ttk.Frame(self.master , padding="10")
        self.main_frame.pack(fill=tk.BOTH , expand=True)

        self._create_widgets()
        self.refresh_task_list() #this is the initial population of the task list

    def _create_widgets(self):
        """
        Creates the widgets for the GUI
        """

       #Creates the Frames
        input_frame = ttk.LabelFrame(self.main_frame , text="Add New Task" , padding="10")
        input_frame.pack(fill=tk.X , pady=5)

        display_frame =ttk.LabelFrame(self.main_frame , text="Tasks" , padding="10")
        display_frame.pack(fill=tk.BOTH , expand=True , pady=5)

        action_frame = ttk.Frame(self.main_frame,padding="5")
        action_frame.pack(fill=tk.X)

        self.status_bar = ttk.Label(self.master , text ="Ready", relief=tk.SUNKEN ,anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM , fill=tk.X)

        #Input Frame Widgets
        ttk.Label(input_frame , text="Description:").grid(row=0 , column=0 , padx=5 , pady=5 , sticky=tk.W)
        self.desc_entry= ttk.Entry(input_frame , width=40)
        self.desc_entry.grid(row=0 , column=1 , padx=5 , pady=5 , sticky=tk.EW)

        ttk.Label(input_frame, text="Priority (1-5):").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.priority_spinbox = ttk.Spinbox(input_frame, from_=1, to=5, width=5)
        self.priority_spinbox.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Difficulty (1-10):").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.difficulty_spinbox = ttk.Spinbox(input_frame, from_=1, to=10, width=5)
        self.difficulty_spinbox.grid(row=0, column=5, padx=5, pady=5)

        add_button = ttk.Button(input_frame, text="Add Task", command=self._add_task)
        add_button.grid(row=0, column=6, padx=10, pady=5)
        input_frame.columnconfigure(1, weight=1)  # Make the description entry expand

        #Display Frame Widgets // Treeview for displaying tasks
        columns = ("id", "description", "priority", "difficulty", "status", "created_at")
        self.tree = ttk.Treeview(display_frame, columns=columns, show="headings")

        #define headings
        self.tree.heading("id" , text="ID")
        self.tree.heading("description", text="Description")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("difficulty", text="Difficulty")
        self.tree.heading("status", text="Status")
        self.tree.heading("created_at", text="Created At")

        # Configure column widths
        self.tree.column("id", width=250, anchor=tk.W)
        self.tree.column("description", width=300, anchor=tk.W)
        self.tree.column("priority", width=60, anchor=tk.CENTER)
        self.tree.column("difficulty", width=70, anchor=tk.CENTER)
        self.tree.column("status", width=80, anchor=tk.CENTER)
        self.tree.column("created_at", width=150, anchor=tk.W)

        #Adding  scrollbar
        scrollbar = ttk.Scrollbar(display_frame , orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT ,fill=tk.BOTH , expand=True)
        scrollbar.pack(side=tk.RIGHT ,fill=tk.Y)

        #Action Frame Widgets
        #Filter buttons
        ttk.Button(action_frame, text="Show All", command=self.refresh_task_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Sort by Priority", command=self._apply_sort_priority).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Sort by Difficulty", command=self._apply_sort_difficulty).pack(side=tk.LEFT, padx=5)

        # Action buttons
        ttk.Button(action_frame, text="Undo Last Action", command=self._undo_action).pack(side=tk.RIGHT, padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self._delete_selected_task).pack(side=tk.RIGHT, padx=5)
        ttk.Button(action_frame, text="Mark as Complete", command=self._mark_task_complete).pack(side=tk.RIGHT, padx=5)

    def refresh_task_list(self, tasks=None):
         """Clears and repopulates the task list in the Treeview."""
         # Clear existing items in the tree
         for item in self.tree.get_children():
             self.tree.delete(item)

         # If no specific list of tasks is provided, get all tasks
         if tasks is None:
             tasks = self.task_manager.get_all_tasks()

         # Populate the tree with tasks
         for task in tasks:
             values = (
                 task.task_id,
                 task.description,
                 task.priority,
                 task.difficulty,
                 task.status,
                 task.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Format datetime for display
             )
             self.tree.insert(" ", tk.END, values=values)
         self.update_status(f"Displaying {len(tasks)} tasks.")

    def update_status(self, message):
        """Updates the text in the status bar."""
        self.status_bar.config(text=message)

        # --- Event Handler Methods ---

    def _add_task(self):
        """Handles the 'Add Task' button click."""
        description = self.desc_entry.get()
        priority = self.priority_spinbox.get()
        difficulty = self.difficulty_spinbox.get()

        if not description:
            messagebox.showerror("Error", "Description cannot be empty.")
            return

        try:
            self.task_manager.create_task(description, priority, difficulty)
            self.refresh_task_list()
            self.update_status(f"Task '{description}' added successfully.")
            # Clear input fields
            self.desc_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add task: {e}")
            self.update_status("Error: Could not add task.")

    def _get_selected_task_id(self):
        """Helper to get the task_id of the selected item in the Treeview."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a task first.")
            return None
        selected_item = selected_items[0]
        task_id = self.tree.item(selected_item, "values")[0]
        return task_id

    def _delete_selected_task(self):
        """Handles the 'Delete Selected' button click."""
        task_id = self._get_selected_task_id()
        if not task_id:
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?"):
            if self.task_manager.delete_task(task_id):
                self.refresh_task_list()
                self.update_status(f"Task {task_id} deleted.")
            else:
                messagebox.showerror("Error", f"Could not delete task {task_id}.")
                self.update_status("Error: Could not delete task.")

    def _mark_task_complete(self):
        """Handles the 'Mark as Complete' button click."""
        task_id = self._get_selected_task_id()
        if not task_id:
            return

        if self.task_manager.update_task(task_id, new_status='completed'):
            self.refresh_task_list()
            self.update_status(f"Task {task_id} marked as complete.")
        else:
            messagebox.showerror("Error", f"Could not update task {task_id}.")
            self.update_status("Error: Could not update task.")

    def _apply_sort_priority(self):
        """Sorts the display by priority."""
        sorted_tasks = self.task_manager.get_tasks_by_priority()
        self.refresh_task_list(tasks=sorted_tasks)
        self.update_status("Tasks sorted by priority (pending tasks only).")

    def _apply_sort_difficulty(self):
        """Sorts the display by difficulty."""
        sorted_tasks = self.task_manager.get_tasks_by_difficulty()
        self.refresh_task_list(tasks=sorted_tasks)
        self.update_status("Tasks sorted by difficulty (pending tasks only).")

    def _undo_action(self):
        """Handles the 'Undo' button click."""
        self.task_manager.undo_last_action()
        self.refresh_task_list()
        self.update_status("Last action undone.")
