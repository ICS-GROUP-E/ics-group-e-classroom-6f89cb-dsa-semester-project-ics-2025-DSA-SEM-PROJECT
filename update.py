import time
from tkinter import messagebox

from database import conn2

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
