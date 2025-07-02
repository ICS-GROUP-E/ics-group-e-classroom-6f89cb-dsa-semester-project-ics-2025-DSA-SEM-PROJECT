import tkinter as tk
from tkinter import ttk
from src.linkedlist import StudentLinkedList


class StudentApp:
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        self.window.title("Student Records")
        self.window.geometry("600x400")

        # Initialize linked list
        self.student_list = StudentLinkedList()

        # Build the GUI
        self.create_widgets()

    def delete_student(self):
        """Delete a student by ID from the linked list"""
        student_id = self.id_entry.get().strip()  # Get ID and remove extra spaces

        if not student_id:  # If ID field is empty
            self.display_area.insert(tk.END, "❗ Error: Please enter a Student ID\n")
            return

        if self.student_list.delete_student(student_id):
            self.display_area.insert(tk.END, f"✅ Deleted student {student_id}\n")
            # Clear the ID field after successful deletion
            self.id_entry.delete(0, tk.END)
        else:
            self.display_area.insert(tk.END, f"❌ Error: Student {student_id} not found\n")

    def search_student(self):
        """Search for a student by ID and display results"""
        student_id = self.id_entry.get().strip()

        if not student_id:
            self.display_area.insert(tk.END, "❗ Error: Please enter a Student ID\n")
            return

        student = self.student_list.search_student(student_id)
        self.display_area.delete(1.0, tk.END)  # Clear previous results

        if student:
            self.display_area.insert(tk.END,
                                     f"🔍 Student Found:\n"
                                     f"ID: {student['id']}\n"
                                     f"Name: {student['name']}\n"
                                     f"Course: {student['course']}\n"
                                     f"GPA: {student['gpa']}\n"
                                     )
        else:
            self.display_area.insert(tk.END, f"❌ No student found with ID: {student_id}\n")

    def create_widgets(self):
        """Create all buttons, labels, and inputs"""
        # Title
        tk.Label(self.window, text="Student Records", font=("Arial", 20)).pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(self.window)
        input_frame.pack(pady=10)

        # Student ID
        tk.Label(input_frame, text="ID:").grid(row=0, column=0, padx=5)
        self.id_entry = tk.Entry(input_frame)
        self.id_entry.grid(row=0, column=1, padx=5)

        # Name
        tk.Label(input_frame, text="Name:").grid(row=1, column=0, padx=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=1, column=1, padx=5)

        # Course
        tk.Label(input_frame, text="Course:").grid(row=2, column=0, padx=5)
        self.course_entry = tk.Entry(input_frame)
        self.course_entry.grid(row=2, column=1, padx=5)

        # GPA
        tk.Label(input_frame, text="GPA:").grid(row=3, column=0, padx=5)
        self.gpa_entry = tk.Entry(input_frame)
        self.gpa_entry.grid(row=3, column=1, padx=5)

        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Show All", command=self.show_students).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Delete", command=self.delete_student, bg="#ff9999").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Search", command=self.search_student, bg="#99ff99").pack(side=tk.LEFT, padx=5)

        # Display Area
        self.display_area = tk.Text(self.window, height=10, width=70)
        self.display_area.pack(pady=10)

    def add_student(self):
        """Add a new student from GUI inputs"""
        try:
            student_id = self.id_entry.get()
            name = self.name_entry.get()
            course = self.course_entry.get()
            gpa = float(self.gpa_entry.get())

            self.student_list.add_student(student_id, name, course, gpa)
            self.display_area.insert(tk.END, f"Added: {name} ({student_id})\n")

            # Clear inputs
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.course_entry.delete(0, tk.END)
            self.gpa_entry.delete(0, tk.END)

        except ValueError as e:
            self.display_area.insert(tk.END, f"Error: {str(e)}\n")

    def show_students(self):
        """Display all students in the text area"""
        self.display_area.delete(1.0, tk.END)  # Clear previous content
        current = self.student_list.head

        if not current:
            self.display_area.insert(tk.END, "No students in records\n")
            return

        while current:
            self.display_area.insert(tk.END,
                                     f"ID: {current.student_id}\n"
                                     f"Name: {current.name}\n"
                                     f"Course: {current.course}\n"
                                     f"GPA: {current.gpa}\n"
                                     "------------------\n"
                                     )
            current = current.next

    def run(self):
        """Start the application"""
        self.window.mainloop()


# Run the app
if __name__ == "__main__":
    app = StudentApp()
    app.run()