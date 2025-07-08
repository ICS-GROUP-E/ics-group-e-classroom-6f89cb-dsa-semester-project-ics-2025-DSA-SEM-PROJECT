import tkinter as tk
from tkinter import messagebox

# ✅ Fix this import — assumes you're running from project root
from ds.priorityqueue import PriorityQueue

class EmergencyTriageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Triage System")

        self.queue = PriorityQueue()

        # Input for name
        tk.Label(root, text="Patient Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=5)

        # Input for priority
        tk.Label(root, text="Priority (1 = urgent):").grid(row=1, column=0, padx=5, pady=5)
        self.priority_entry = tk.Entry(root)
        self.priority_entry.grid(row=1, column=1, padx=5)

        # Buttons
        tk.Button(root, text="Add Patient", command=self.add_patient).grid(row=2, column=0, pady=10)
        tk.Button(root, text="Serve Patient", command=self.serve_patient).grid(row=2, column=1)

        # Display queue
        self.queue_listbox = tk.Listbox(root, width=40)
        self.queue_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def add_patient(self):
        name = self.name_entry.get()
        priority_text = self.priority_entry.get()

        if not name or not priority_text.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a name and numeric priority.")
            return

        priority = int(priority_text)
        self.queue.insert(name, priority)
        self.name_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.update_display()

    def serve_patient(self):
        patient = self.queue.remove_highest_priority()
        if patient:
            messagebox.showinfo("Serving Patient", f"Now serving: {patient}")
            self.update_display()
        else:
            messagebox.showinfo("Queue Empty", "No patients in queue.")

    def update_display(self):
        self.queue_listbox.delete(0, tk.END)
        for patient in self.queue.list_patients():
            self.queue_listbox.insert(tk.END, patient)
