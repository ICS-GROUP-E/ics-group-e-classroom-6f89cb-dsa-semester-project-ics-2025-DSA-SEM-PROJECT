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









