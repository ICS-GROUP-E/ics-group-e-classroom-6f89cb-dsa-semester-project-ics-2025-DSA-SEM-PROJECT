# src/ui/doctorlookup_ui.py
# by Michelle
import tkinter as tk
from tkinter import messagebox
import logging
import sys
import os

# ✅ Add correct paths for custom modules
current_dir = os.path.dirname(__file__)
ds_path = os.path.abspath(os.path.join(current_dir, '..', 'ds'))
db_path = os.path.abspath(os.path.join(current_dir, '..', 'database'))

print(f"Current directory: {current_dir}")
print(f"DS path: {ds_path}")
print(f"DB path: {db_path}")
print(f"DS path exists: {os.path.exists(ds_path)}")
print(f"BST file exists: {os.path.exists(os.path.join(ds_path, 'bst_doctorlookup.py'))}")

sys.path.insert(0, ds_path)
sys.path.insert(0, db_path)

# ✅ Try importing with error handling
try:
    from bst_doctorlookup import Doctor, DoctorBST

    print("Successfully imported Doctor and DoctorBST")
except ImportError as e:
    print(f"Import error for BST: {e}")
    sys.exit(1)

try:
    import db_connection as db

    print("Successfully imported db_connection")
except ImportError as e:
    print(f"Import error for db_connection: {e}")
    sys.exit(1)

# ✅ Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s")


class DoctorLookupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor Lookup System")
        self.tree = DoctorBST()

        # Initialize DB and load existing doctors
        try:
            db.initialize_db()
            for name, specialty in db.fetch_all_doctors():
                self.tree.insertDoctor(Doctor(name, specialty))
            logging.info("Database initialized and doctors loaded")
        except Exception as e:
            logging.error(f"Database initialization error: {e}")
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")

        self.create_widgets()

    def create_widgets(self):
        # Create main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Input fields
        tk.Label(main_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Label(main_frame, text="Specialty:").grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.name_entry = tk.Entry(main_frame, width=30)
        self.specialty_entry = tk.Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.specialty_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

        tk.Button(button_frame, text="Add Doctor", command=self.add_doctor, width=12).pack(pady=2)
        tk.Button(button_frame, text="Search", command=self.search_doctor, width=12).pack(pady=2)
        tk.Button(button_frame, text="Update", command=self.update_doctor, width=12).pack(pady=2)
        tk.Button(button_frame, text="Delete", command=self.delete_doctor, width=12).pack(pady=2)
        tk.Button(button_frame, text="Show All", command=self.display_all, width=12).pack(pady=2)
        tk.Button(button_frame, text="Clear", command=self.clear_entries, width=12).pack(pady=2)

        # Results listbox
        tk.Label(main_frame, text="Results:").grid(row=2, column=0, padx=5, pady=(10, 0), sticky='nw')
        self.result_listbox = tk.Listbox(main_frame, width=80, height=15)
        self.result_listbox.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(main_frame)
        scrollbar.grid(row=3, column=3, sticky='ns', pady=5)
        self.result_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_listbox.yview)

        # Load all doctors on startup
        self.display_all()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.specialty_entry.delete(0, tk.END)

    def add_doctor(self):
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip()

        if not name or not specialty:
            messagebox.showwarning("Input Error", "Both name and specialty are required.")
            return

        try:
            # Check if doctor already exists
            if self.tree.searchDoctor(name):
                messagebox.showwarning("Duplicate", f"Doctor '{name}' already exists.")
                return

            doctor = Doctor(name, specialty)
            self.tree.insertDoctor(doctor)
            db.insert_doctor_db(name, specialty)
            logging.info(f"Added: {name}")
            messagebox.showinfo("Success", f"Doctor '{name}' added successfully.")
            self.display_all()
            self.clear_entries()
        except Exception as e:
            logging.error(f"Error adding doctor: {e}")
            messagebox.showerror("Error", f"Failed to add doctor: {e}")

    def search_doctor(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name to search.")
            return

        try:
            doctor = self.tree.searchDoctor(name)
            self.result_listbox.delete(0, tk.END)
            if doctor:
                self.result_listbox.insert(tk.END, f"Found: {doctor}")
                # Auto-fill specialty field for updates
                self.specialty_entry.delete(0, tk.END)
                self.specialty_entry.insert(0, doctor.specialty)
            else:
                self.result_listbox.insert(tk.END, f"Doctor '{name}' not found.")
        except Exception as e:
            logging.error(f"Error searching doctor: {e}")
            messagebox.showerror("Error", f"Search failed: {e}")

    def update_doctor(self):
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip()

        if not name or not specialty:
            messagebox.showwarning("Input Error", "Both name and specialty are required.")
            return

        try:
            if self.tree.updateDoctor(name, specialty):
                db.update_doctor_db(name, specialty)
                messagebox.showinfo("Updated", f"Doctor '{name}' updated successfully.")
                self.display_all()
                self.clear_entries()
            else:
                messagebox.showerror("Error", f"Doctor '{name}' not found.")
        except Exception as e:
            logging.error(f"Error updating doctor: {e}")
            messagebox.showerror("Error", f"Failed to update doctor: {e}")

    def delete_doctor(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name to delete.")
            return

        try:
            if self.tree.searchDoctor(name):
                # Confirm deletion
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Dr. {name}?"):
                    self.tree.deleteDoctor(name)
                    db.delete_doctor_db(name)
                    messagebox.showinfo("Deleted", f"Doctor '{name}' deleted successfully.")
                    self.display_all()
                    self.clear_entries()
            else:
                messagebox.showerror("Error", f"Doctor '{name}' not found.")
        except Exception as e:
            logging.error(f"Error deleting doctor: {e}")
            messagebox.showerror("Error", f"Failed to delete doctor: {e}")

    def display_all(self):
        try:
            self.result_listbox.delete(0, tk.END)
            doctors = self.tree.inorderTraversal()
            if doctors:
                self.result_listbox.insert(tk.END, f"Total Doctors: {len(doctors)}")
                self.result_listbox.insert(tk.END, "-" * 50)
                for doc in doctors:
                    self.result_listbox.insert(tk.END, str(doc))
            else:
                self.result_listbox.insert(tk.END, "No doctors found in the system.")
        except Exception as e:
            logging.error(f"Error displaying doctors: {e}")
            messagebox.showerror("Error", f"Failed to display doctors: {e}")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.geometry("700x500")
        app = DoctorLookupApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        logging.error(f"Application error: {e}")