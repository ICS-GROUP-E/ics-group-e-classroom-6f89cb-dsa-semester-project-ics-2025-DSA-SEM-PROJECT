# doctorlookup_ui.py

import tkinter as tk
from tkinter import messagebox
from ..core.bst_doctorlookup import Doctor, DoctorBST
from ..core import db_connection as db
import logging

# Setup real-time logging to console
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class DoctorLookupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor Lookup System (BST + SQLite)")
        self.tree = DoctorBST()

        # Initialize database and load existing doctors
        db.initialize_db()
        for name, specialty in db.fetch_all_doctors():
            self.tree.insertDoctor(Doctor(name, specialty))

        self.create_widgets()

    def create_widgets(self):
        # Input labels and fields
        tk.Label(self.root, text="Name").grid(row=0, column=0)
        tk.Label(self.root, text="Specialty").grid(row=1, column=0)

        self.name_entry = tk.Entry(self.root)
        self.specialty_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)
        self.specialty_entry.grid(row=1, column=1)

        # Buttons
        tk.Button(self.root, text="Add Doctor", command=self.add_doctor).grid(row=0, column=2)
        tk.Button(self.root, text="Search", command=self.search_doctor).grid(row=1, column=2)
        tk.Button(self.root, text="Update", command=self.update_doctor).grid(row=2, column=2)
        tk.Button(self.root, text="Delete", command=self.delete_doctor).grid(row=3, column=2)
        tk.Button(self.root, text="Show All", command=self.display_all).grid(row=4, column=2)

        # Output list box
        self.result_listbox = tk.Listbox(self.root, width=50)
        self.result_listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def add_doctor(self):
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip()
        if name and specialty:
            doctor = Doctor(name, specialty)
            self.tree.insertDoctor(doctor)
            db.insert_doctor_db(name, specialty)
            logging.info(f"Doctor '{name}' added.")
            messagebox.showinfo("Success", f"Doctor '{name}' added.")
        else:
            messagebox.showwarning("Input Error", "Both fields are required.")

    def search_doctor(self):
        name = self.name_entry.get().strip()
        doctor = self.tree.searchDoctor(name)
        self.result_listbox.delete(0, tk.END)
        if doctor:
            self.result_listbox.insert(tk.END, f"Found: {doctor}")
            logging.info(f"Doctor '{name}' found.")
        else:
            self.result_listbox.insert(tk.END, f"Doctor '{name}' not found.")
            logging.warning(f"Doctor '{name}' not found.")

    def update_doctor(self):
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip()
        if self.tree.updateDoctor(name, specialty):
            db.update_doctor_db(name, specialty)
            logging.info(f"Doctor '{name}' updated to {specialty}.")
            messagebox.showinfo("Updated", f"Doctor '{name}' updated.")
        else:
            logging.warning(f"Doctor '{name}' not found for update.")
            messagebox.showerror("Error", f"Doctor '{name}' not found.")

    def delete_doctor(self):
        name = self.name_entry.get().strip()
        self.tree.deleteDoctor(name)
        db.delete_doctor_db(name)
        logging.info(f"Doctor '{name}' deleted.")
        messagebox.showinfo("Deleted", f"Doctor '{name}' deleted (if existed).")

    def display_all(self):
        doctors = self.tree.inorderTraversal()
        self.result_listbox.delete(0, tk.END)
        for doc in doctors:
            self.result_listbox.insert(tk.END, str(doc))
        logging.info("Displayed all doctors.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DoctorLookupApp(root)
    root.mainloop()
