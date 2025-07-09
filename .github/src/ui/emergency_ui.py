import tkinter as tk
from tkinter import messagebox
from database.patient_service import PatientService

class EmergencyTriageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚑 Emergency Triage System")
        self.center_window(550, 450)
        self.root.configure(bg="#f0f4f8")  # Light background

        self.primary_color = "#005f73"
        self.button_color = "#0a9396"
        self.text_color = "#001219"

        # Main frame
        frame = tk.Frame(root, bg="#f0f4f8", padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        # Header
        tk.Label(
            frame,
            text="Emergency Triage System",
            font=("Segoe UI", 18, "bold"),
            bg="#f0f4f8",
            fg=self.primary_color
        ).pack(pady=10)

        # Name input
        name_frame = tk.Frame(frame, bg="#f0f4f8")
        name_frame.pack(fill="x", pady=5)
        tk.Label(name_frame, text="Patient Name:", bg="#f0f4f8", fg=self.text_color, anchor="w", width=20).pack(side="left")
        self.name_entry = tk.Entry(name_frame, font=("Segoe UI", 10))
        self.name_entry.pack(fill="x", expand=True)

        # Priority input
        priority_frame = tk.Frame(frame, bg="#f0f4f8")
        priority_frame.pack(fill="x", pady=5)
        tk.Label(priority_frame, text="Priority (1 = urgent):", bg="#f0f4f8", fg=self.text_color, anchor="w", width=20).pack(side="left")
        self.priority_entry = tk.Entry(priority_frame, font=("Segoe UI", 10))
        self.priority_entry.pack(fill="x", expand=True)

        # Buttons
        btn_frame = tk.Frame(frame, bg="#f0f4f8")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="➕ Add", command=self.add_patient, bg=self.button_color, fg="white", width=14).pack(side="left", padx=5)
        tk.Button(btn_frame, text="✅ Serve", command=self.serve_patient, bg=self.button_color, fg="white", width=14).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ Clear", command=self.clear_all_patients, bg="#ae2012", fg="white", width=14).pack(side="left", padx=5)

        # Queue list
        self.queue_listbox = tk.Listbox(
            frame,
            font=("Consolas", 11),
            bg="white",
            fg=self.text_color,
            width=50,
            height=10,
            selectbackground="#94d2bd"
        )
        self.queue_listbox.pack(pady=10)

        self.update_display()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def add_patient(self):
        name = self.name_entry.get()
        priority_text = self.priority_entry.get()

        if not name or not priority_text.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a name and numeric priority.")
            return

        priority = int(priority_text)
        PatientService.add_patient(name, priority)
        self.name_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.update_display()

    def serve_patient(self):
        patients = PatientService.get_all_patients()
        if not patients:
            messagebox.showinfo("Queue Empty", "No patients in queue.")
            return

        patient_id, name, priority, _ = patients[0]
        PatientService.delete_patient_by_id(patient_id)
        messagebox.showinfo("Serving Patient", f"Now serving: {name} (Priority {priority})")
        self.update_display()

    def clear_all_patients(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all patients?"):
            PatientService.clear_all()
            self.update_display()

    def update_display(self):
        self.queue_listbox.delete(0, tk.END)
        for (_, name, priority, _) in PatientService.get_all_patients():
            self.queue_listbox.insert(tk.END, f"{name} (Priority {priority})")
