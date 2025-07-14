import time
from tkinter import messagebox
from database.database import conn2


# Dummy logger to prevent errors if you can't import
def log_operation(structure, operation, start, end):
    duration = end - start
    print(f"[{structure}] {operation} took {duration:.6f} seconds")

# Linked list classes
class MedicineNode:
    def __init__(self, name, quantity, price, expiry):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.expiry = expiry
        self.next = None

class MedicineLinkedList:
    def __init__(self):
        self.head = None

    def load_from_database(self):
        cursor = conn2.cursor()
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
                return True
            current = current.next
        return False

    def update_database(self, name, quantity, price, expiry):
        cursor = conn2.cursor()
        sql = "UPDATE meddata SET Quantity = %s, Price = %s, Expiry = %s WHERE Name = %s"
        cursor.execute(sql, (quantity, price, expiry, name))
        conn2.commit()
        cursor.close()

# Initialize medicine list
medicine_list = MedicineLinkedList()
medicine_list.load_from_database()

# Function to call from GUI button
def update_medicine(entries, product_table):
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
            structure_usage["LinkedList"] += 1

            start = time.perf_counter()
            end = time.perf_counter()
            log_operation("LinkedList", "UPDATE", start, end)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating DB: {e}")
    else:
        messagebox.showerror("Not Found", f"Medicine '{name}' not found in records.")

    # Clear and reload table manually (since you can’t use load_data_into_table)
    for row in product_table.get_children():
        product_table.delete(row)

    cursor = conn2.cursor()
    cursor.execute("SELECT * FROM meddata")
    rows = cursor.fetchall()
    for row in rows:
        product_table.insert("", "end", values=row)
    cursor.close()

    # Reset fields manually (since you can’t use reset_fields)
    for entry in entries.values():
        entry.delete(0, "end")


class StackManager:
    def _init_(self):
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
        structure_usage["Stacks"] += 1  

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
#Function to undo ----------------------------------------------------------------------
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



# Reading database as a dictionary
class DictManager:
    def _init_(self):
        self.records = {}

    def add(self, key, value):
        self.records[key] = value

    def get(self, key):
        return self.records.get(key, None)

    def get_all(self):
        return self.records
read_dict = DictManager()

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









