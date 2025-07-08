import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import time

structure_details = {
    "List": {"operations": 0, "total_time": 0.0, "last_operation": "None"},
    "Dictionary": {"operations": 0, "total_time": 0.0, "last_operation": "None"},
    "LinkedList": {"operations": 0, "total_time": 0.0, "last_operation": "None"},
    "Stack": {"operations": 0, "total_time": 0.0, "last_operation": "None"},
}
def log_operation(structure_name, operation_name, start_time, end_time):
    elapsed = end_time - start_time
    struct = structure_details[structure_name]
    struct["operations"] += 1
    struct["total_time"] += elapsed
    struct["last_operation"] = operation_name

# Operation counters
total_operations = 0
structure_usage = {
    "List": 0,
    "Dictionary": 0,
    "LinkedList": 0,
    "Stacks": 0
}

#Report method------------------------------------------------------------------------------------------------------------
def generate_pdf_report():
    try:
        filename = f"medicine_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        # Title
        c.setFont("Helvetica-Bold", 30)
        title="Pharmacy Inventory System Report"
        c.drawString(50, height - 50, title)

        text_width = c.stringWidth(title, "Helvetica-Bold", 30)
        c.setLineWidth(1)
        c.line(50, height - 55, 50 + text_width, height - 55)

        y = height - 100
        c.setFont("Helvetica", 12)

        # Section: Summary Info
        most_used_structure = max(structure_usage, key=structure_usage.get)

        c.drawString(50, y, f"Total Operations Performed: {total_operations}")
        y -= 20
        c.drawString(50, y, f"Data Structures Used: {', '.join(structure_usage.keys())}")
        y -= 20
        c.drawString(50, y, f"Most Active Structure: {most_used_structure} ({structure_usage[most_used_structure]} uses)")

        y -= 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "")
        y -= 20
        c.drawString(50, y, "Detailed Breakdown (per Data Structure)")
        y -= 20
        c.setFont("Helvetica", 11)

        for struct_name, data in structure_details.items():
            avg_time = data["total_time"] / data["operations"] if data["operations"] > 0 else 0.0

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, f"{struct_name}")
            y -= 20

            c.setFont("Helvetica", 11)
            c.drawString(70, y, f"Operations: {data['operations']}")
            y -= 20
            c.drawString(70, y, f"Average Execution Time: {avg_time:.10f}s")
            y -= 20
            c.drawString(70, y, f"Last Operation: {data['last_operation']}")
            y -= 30

        c.save()
        messagebox.showinfo("Success", f"Report saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", f" Failed to generate report: {e}")

#Database Connection ---------------------------------------------------------------------------------------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="medicines"
    )
#Standard data structures-------------------------------------------------------------------------------------------------------------
class ListManager:
    def __init__(self):
        self.data = []

    def insert(self, item):
        self.data.append(item)

    def get_all(self):
        return self.data
#---------------------------------------------------------------------------------------

class DictManager:
    def __init__(self):
        self.records = {}

    def add(self, key, value):
        self.records[key] = value

    def get(self, key):
        return self.records.get(key, None)

    def get_all(self):
        return self.records

#---------------------------------------------------------------------------------------------------------------
class MedicineNode:
    def __init__(self, name, quantity, price, expiry):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.expiry = expiry
        self.next = None

# Linked List
class MedicineLinkedList:

    def __init__(self):
        self.head = None

    def load_from_database(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meddata")
        results = cursor.fetchall()
        cursor.close()

        for _, name, quantity, price, expiry in results:
            self.append(name, quantity, price, expiry)

    def append(self, name, quantity, price, expiry):
        new_node = MedicineNode(name, quantity, price, expiry)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def update_node(self, name, quantity, price, expiry):
        current = self.head
        while current:
            if current.name == name:
                current.quantity = quantity
                current.price = price
                current.expiry = expiry
                return True  # Found and updated
            current = current.next
        return False  # Not found

    def update_database(self, name, quantity, price, expiry):
        conn = connect_db()
        cursor = conn.cursor()
        sql = "UPDATE meddata SET Quantity = %s, Price = %s, Expiry = %s WHERE Name = %s"
        cursor.execute(sql, (quantity, price, expiry, name))
        conn.commit()
        cursor.close()


medicine_list = MedicineLinkedList()
medicine_list.load_from_database()
#-----------------------------------------------------------------------------------------------------------------------
class StackManager:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def peek(self):
        return self.stack[-1] if self.stack else None

    def is_empty(self):
        return len(self.stack) == 0
#Managers---------------------------------------------------------------------------------------------------------------
create_list = ListManager()
read_dict = DictManager()


#Function to reset fields-----------------------------------------------------------------------------------------------------------------------
def reset_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)
#Function to insert data-----------------------------------------------------------------------------------------------------------------------
new_medicines=ListManager()
def create_medicine():
    name = entries["Name"].get()
    qty = entries["Quantity"].get()
    price = entries["Price"].get()
    expiry = entries["Expiry Date"].get()
    if not all([name, qty, price, expiry]):
        messagebox.showerror("Error", "All fields required")
        return

    new_medicines.insert(name)
    new_medicines.insert(qty)
    new_medicines.insert(price)
    new_medicines.insert(expiry)
    values= new_medicines.get_all()
    try:

        conn = connect_db()
        cursor = conn.cursor()
        sql="INSERT INTO meddata (Name, Quantity, Price, Expiry) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Medicine added successfully")
        load_data_into_table()
        reset_fields()
        global total_operations, structure_usage
        total_operations += 1
        structure_usage["List"] += 1  # change this according to the structure used
        start = time.perf_counter()
        # your action here
        end = time.perf_counter()
        log_operation("List", "POP", start, end)


    except Exception as e:

        messagebox.showerror("Database Error", str(e))
#Function to search data-----------------------------------------------------------------------------------------------------------------------
def search_medicine():
    query = search_entry.get().strip().lower()
    if not query:
        messagebox.showwarning("Search Error", "Please enter a medicine name.")
        return
    conn2 = connect_db()

    path = conn2.cursor()
    path.execute("select * from meddata")
    ans = path.fetchall()  # Brings the rows back as tuples

    # DB Operations
    medicine_Types = DictManager()

    for Med_id, Name, Quantity, Price, Expiry in ans:
        medicine_Types.add(Name.lower(), {
            "ID": Med_id,
            "Quantity": Quantity,
            "Price": Price,
            "Expiry Date": Expiry
        })
    result = medicine_Types.records.get(query)
    if result:
        info = f"Medicine ID: {result['ID']}\n" \
               f"Quantity: {result['Quantity']}\n" \
               f"Price: {result['Price']}\n" \
               f"Expiry Date: {result['Expiry Date']}"
        messagebox.showinfo("Medicine Found", info)
        global total_operations, structure_usage
        total_operations += 1
        structure_usage["Dictionary"] += 1  # change this according to the structure used
        start = time.perf_counter()
        end = time.perf_counter()
        log_operation("Dictionary", "POP", start, end)


    else:
        messagebox.showerror("Not Found", f"No medicine found with name '{query}'")
    reset_fields()
    search_entry.delete(0, tk.END)

#Function to update data------------------------------------------------------------------------------------------------
def update_medicine():
    name = entries["Name"].get()
    quantity = entries["Quantity"].get()
    price = entries["Price"].get()
    expiry = entries["Expiry Date"].get()

    if not (name and quantity and price and expiry):
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    success = medicine_list.update_node(name, quantity, price, expiry)
    if success:
        try:
            medicine_list.update_database(name, quantity, price, expiry)
            messagebox.showinfo("Success", "Medicine updated successfully!")
            global total_operations, structure_usage
            total_operations += 1
            structure_usage["LinkedList"] += 1  # change this according to the structure used

            start = time.perf_counter()
            end = time.perf_counter()
            log_operation("LinkedList", "POP", start, end)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating DB: {e}")
    else:
        messagebox.showerror("Not found", f"Medicine '{name}' not found in records.")
    load_data_into_table()
    reset_fields()
#Function to delete data-----------------------------------------------------------------------------------------------------------------------
delete_stack = StackManager()
def delete_medicine():

    name = delete_entry.get().strip()
    if not name:
        messagebox.showerror("Input Error", "Please enter a medicine name to delete.")
        return
    try:
        conn = connect_db()
        cursor= conn.cursor()
        cursor.execute("SELECT * FROM meddata WHERE Name = %s", (name,))
        record = cursor.fetchone()

        
        delete_stack.push(record)
        cursor.execute("DELETE FROM meddata WHERE Name = %s", (name,))
        conn.commit()
        conn.close()

        delete_entry.delete(0, tk.END)

        messagebox.showinfo("Success", f"'{name}' deleted successfully")
        global total_operations, structure_usage
        total_operations += 1
        structure_usage["Stacks"] += 1  # change this according to the structure used

        start = time.perf_counter()
        end = time.perf_counter()
        log_operation("Stacks", "POP", start, end)
        if not record:
            messagebox.showerror("Not Found", f"No medicine found with name '{name}'.")
            delete_entry.delete(0, tk.END)
            return
        load_data_into_table()
        reset_fields()
        
    except Exception as e:
        messagebox.showerror("Error", str(e))
        reset_fields()
#Function to undo --------------------------------------------------------------------------------------------------------
def undo_delete():
    if delete_stack.is_empty():
        messagebox.showinfo("Undo", "No deletions to undo.")
        return

    try:
        record = delete_stack.pop()
        conn = connect_db()
        cursor = conn.cursor()
        name, quantity, price, expiry = record[1], record[2], record[3], record[4]
        cursor.execute(
            "INSERT INTO meddata ( Name, Quantity, Price, Expiry) VALUES ( %s, %s, %s, %s)",
            (name, quantity, price, expiry))
        conn.commit()
        conn.close()

        messagebox.showinfo("Undo Success", f"Medicine '{record[1]}' restored successfully.")
        load_data_into_table()
    except Exception as e:
        messagebox.showerror("Undo Error", str(e))

#Function to load data-----------------------------------------------------------------------------------------------------------------------
def load_data_into_table():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT Med_ID, Name, Quantity, Price, Expiry FROM meddata")
        rows = cursor.fetchall()

        product_table.delete(*product_table.get_children())
        for row in rows:
            product_table.insert('', 'end', values=row)

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


#---------------------------------------------------------------------------------------------------------

root = tk.Tk()
root.state("zoomed")
root.title("Pharmacy Inventory Management System")

#Title frame creation---------------------------------------------------------------------------------------------------
title_frame = tk.Frame(root, bg="white",bd=2, relief = "groove")
title_frame.pack(side="top", fill="x")

#Title label creation---------------------------------------------------------------------------------------------------
title_label = tk.Label(
    title_frame,
    text="PHARMACY MANAGEMENT INVENTORY SYSTEM",
    font=("CALIBRI", 35, "bold"),
    fg="blue",
    bg="white"
)
title_label.pack(pady=20)
# -----pane frame-------------------------------------------------------------------------------------------------------
pane = tk.Frame(root, bd=2, relief = "groove")
pane.pack( padx=10, pady=10, fill = "x")

#formFrame--------------------------------------------------------------------------------------------------------------
formFrame = tk.LabelFrame(pane, text="Insert or Update data", fg="black", font=("Calibri", 10, "bold"), bd=2)
formFrame.grid(row=0, column = 0, padx=10,pady=10)
#Form label fields -----------------------------------------------------------------------------------------------------
fields = [
    ("Name", 0),
    ("Quantity", 1),
    ("Price", 2),
    ("Expiry Date", 3)]
entries = {}
for field, row in fields:
    lbl = tk.Label(
        formFrame,
        text=field + ":",
        font=("Calibri", 12, )
    )
    lbl.grid(row=row, column=0,sticky="e", pady=5, padx=10)
#--Entry creation-------------------------------------------------------------------------------------------------------
    ent = tk.Entry(
        formFrame,
        font=("Calibri", 12),
        width=30
    )
    ent.grid(row=row, column=1, sticky="w", pady=5, padx=10)
    entries[field] = ent
#Form button creations--------------------------------------------------------------------------------------------------
insertButton = tk.Button(formFrame,text="Insert Data",font=("Calibri", 12),
                         bg="white",fg="black",width=15,command=create_medicine)
insertButton.grid(row=0, column=4, pady=10, padx=50)

updateButton = tk.Button(formFrame,text="Update Data",font=("Calibri", 12),
                         bg="white",fg="black",width=15, command=update_medicine)
updateButton.grid(row=1, column=4, pady=10, padx=50)
#Spane frame------------------------------------------------------------------------------------------------------------
spane = tk.Frame(pane)
spane.grid(row=0, column=1)
#Search data frame------------------------------------------------------------------------------------------------------
searchFrame = tk.LabelFrame(spane, text="Search data", fg="black", font=("Calibri", 10, "bold"), bd=2)
searchFrame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

search_label = tk.Label(searchFrame, text="           Name:", font=("Calibri", 12))
search_label.grid(row=0, column=0, padx=5, pady=10, sticky="e")

search_entry = tk.Entry(searchFrame, font=("Calibri", 12), width=30)
search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

search_button = tk.Button(searchFrame, text="Search Data", font=("Calibri", 12),
                          bg="white", fg="black", width=15, command=search_medicine)
search_button.grid(row=0, column=2, padx=50, pady=10)
#Delete data frame------------------------------------------------------------------------------------------------------
deleteFrame = tk.LabelFrame(spane, text="Delete data", fg="black", font=("Calibri", 10, "bold"), bd=2)
deleteFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


delete_label = tk.Label(deleteFrame, text="           Name:", font=("Calibri", 12))
delete_label.grid(row=0, column=0, padx=5, pady=10, sticky="e")

delete_entry = tk.Entry(deleteFrame, font=("Calibri", 12), width=30)
delete_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

delete_button = tk.Button(deleteFrame, text="Delete Data", font=("Calibri", 12),
                          bg="white", fg="black", width=15, command=delete_medicine)
delete_button.grid(row=0, column=2, padx=5, pady=10)

undo_button = tk.Button(deleteFrame, text="Undo", font=("Calibri", 12),
                          bg="white", fg="black", width=10, command=undo_delete)
undo_button.grid(row=0, column=3, padx=5, pady=10)
#Report frame-----------------------------------------------------------------------------------------------------------
reportFrame = tk.LabelFrame(root, text="Report", fg="black", font=("Calibri", 10, "bold"), bd=2)
reportFrame.pack( padx=10, pady=10, fill = "x")

report_button = tk.Button(reportFrame, text="Download report", font=("Calibri", 12),
                          bg="white", fg="black", width=15,command=generate_pdf_report)
report_button.grid(row=0, column=0, padx=20, pady=10)
#Table frame------------------------------------------------------------------------------------------------------------
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
scroll_y = tk.Scrollbar(table_frame, orient="vertical")

product_table = ttk.Treeview(
    table_frame,
    columns=("medicineID", "name", "qty", "price", "expiry"),
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
scroll_x.config(command=product_table.xview)
scroll_y.config(command=product_table.yview)

# Table Headings
product_table.heading("medicineID", text="Medicine ID")
product_table.heading("name", text="Name")
product_table.heading("qty", text="Quantity")
product_table.heading("price", text="Price")
product_table.heading("expiry", text="Expiry Date")
product_table['show'] = 'headings'

# Column widths
product_table.column("medicineID", width=100)
product_table.column("name", width=150)
product_table.column("qty", width=120)
product_table.column("price", width=120)
product_table.column("expiry", width=180)

product_table.pack(fill="both", expand=True)

# -------------------- Table Font Styling ------------------------------------------------------------------------------
style = ttk.Style()
style.configure("Treeview.Heading", font=("Calibri", 12))
style.configure("Treeview", font=("Calibri", 12))

# Run application-------------------------------------------------------------------------------------------------------
load_data_into_table()
root.mainloop()

