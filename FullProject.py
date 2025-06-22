import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk

# -------------------- Data Structures --------------------
class ListManager:
    def __init__(self):
        self.data = []

    def insert(self, item):
        self.data.append(item)

    def get_all(self):
        return self.data


class DictManager:
    def __init__(self):
        self.records = {}

    def add(self, key, value):
        self.records[key] = value

    def get(self, key):
        return self.records.get(key, None)

    def get_all(self):
        return self.records


class LinkedListManager:
    class Node:
        def __init__(self, medicine_id, data):
            self.medicine_id = medicine_id
            self.data = data
            self.next = None

    def __init__(self):
        self.head = None

    def insert(self, medicine_id, data):
        new_node = self.Node(medicine_id, data)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node

    def update(self, medicine_id, new_data):
        curr = self.head
        while curr:
            if curr.medicine_id == medicine_id:
                curr.data = new_data
                return True
            curr = curr.next
        return False

    def search(self, medicine_id):
        curr = self.head
        while curr:
            if curr.medicine_id == medicine_id:
                return curr.data
            curr = curr.next
        return None


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


# -------------------- Database Connection --------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="medicines"
    )

# -------------------- Managers --------------------
create_list = ListManager()
read_dict = DictManager()
update_list = LinkedListManager()
delete_stack = StackManager()

# -------------------- GUI Setup --------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Pharmacy Inventory Management System")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}+0+0")

# -------------------- Title --------------------
title_frame = ctk.CTkFrame(app, fg_color="white")
title_frame.pack(side="top", fill="x")
title_label = ctk.CTkLabel(title_frame, text="PHARMACY INVENTORY SYSTEM", font=ctk.CTkFont("Arial", size=35, weight="bold"), text_color="blue")
title_label.pack(pady=20)
# -------------------- Functions --------------------
def reset_fields():
    for entry in entries.values():
        entry.delete(0, ctk.END)

def add_data():
    name = entries["Name"].get()
    qty = entries["Quantity"].get()
    price = entries["Price"].get()
    expiry = entries["Expiry Date"].get()
    if not all([name, qty, price, expiry]):
        messagebox.showerror("Error", "All fields required")
        return
    data = [name, qty, price, expiry]
    create_list.insert(data)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meddata (Name, Quantity, Price, Expiry) VALUES (%s, %s, %s, %s)", data)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Medicine added successfully")
        read_data()
        reset_fields()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def read_data():
    for item in product_table.get_children():
        product_table.delete(item)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meddata")
        rows = cursor.fetchall()
        for row in rows:
            product_table.insert("", "end", values=row)
            read_dict.add(row[0], row)
        conn.close()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def update_data():
    selected = product_table.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record to update")
        return
    values = product_table.item(selected, "values")
    med_id = values[0]
    new_data = [entries["Name"].get(), entries["Quantity"].get(), entries["Price"].get(), entries["Expiry Date"].get()]
    if not all(new_data):
        messagebox.showerror("Error", "All fields required")
        return
    update_list.insert(med_id, new_data)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE meddata SET Name=%s, Quantity=%s, Price=%s, Expiry=%s WHERE Med_id=%s", (*new_data, med_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record updated")
        read_data()
        reset_fields()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def delete_data():
    selected = product_table.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record to delete")
        return
    values = product_table.item(selected, "values")
    med_id = values[0]
    delete_stack.push(values)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meddata WHERE Med_id=%s", (med_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record deleted")
        read_data()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

def exit_app():
    app.destroy()


# -------------------- Form --------------------
form_frame = ctk.CTkFrame(app)
form_frame.pack(pady=10, padx=30, fill="x")
fields = [("Name", 0), ("Quantity", 1), ("Price", 2), ("Expiry Date", 3)]
entries = {}
for field, row in fields:
    lbl = ctk.CTkLabel(form_frame, text=field + ":", font=ctk.CTkFont("Arial", 15, "bold"))
    lbl.grid(row=row, column=0, sticky="w", pady=5, padx=10)
    ent = ctk.CTkEntry(form_frame, font=ctk.CTkFont("Arial", 14), width=300)
    ent.grid(row=row, column=1, pady=5, padx=10)
    entries[field] = ent
# -------------------- Buttons --------------------
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)
ctk.CTkButton(button_frame, text="ADD DATA", command=add_data, width=130, font=ctk.CTkFont("Arial", 15, "bold")).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="READ DATA", command=read_data, width=130, font=ctk.CTkFont("Arial", 15, "bold")).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="UPDATE", command=update_data, width=130, font=ctk.CTkFont("Arial", 15, "bold")).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="DELETE", command=delete_data, width=130, font=ctk.CTkFont("Arial", 15, "bold")).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="RESET", command=reset_fields, width=130, font=ctk.CTkFont("Arial", 15, "bold")).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="EXIT", command=exit_app, width=130, font=ctk.CTkFont("Arial", 15, "bold")).pack(side="left", padx=10)

# -------------------- Table --------------------
table_frame = ctk.CTkFrame(app)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)
scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
product_table = ttk.Treeview(table_frame, columns=("Med_id", "Name", "Quantity", "Price", "Expiry"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
scroll_x.config(command=product_table.xview)
scroll_y.config(command=product_table.yview)
product_table.heading("Med_id", text="Med_id")
product_table.heading("Name", text="Name")
product_table.heading("Quantity", text="Quantity")
product_table.heading("Price", text="Price")
product_table.heading("Expiry", text="Expiry Date")
product_table['show'] = 'headings'
product_table.pack(fill="both", expand=True)
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 15, "bold"))
style.configure("Treeview", font=("Arial", 14))


# -------------------- Start --------------------
read_data()
button_frame.pack(pady=20)

app.mainloop()
