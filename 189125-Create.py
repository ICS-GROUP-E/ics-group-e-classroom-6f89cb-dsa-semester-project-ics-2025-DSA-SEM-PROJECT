class ListManager:
    def _init_(self):
        self.data = []

    def insert(self, item):
        self.data.append(item)

    def get_all(self):
        return self.data

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
        structure_usage["List"] += 1  
        start = time.perf_counter()
        
        end = time.perf_counter()
        log_operation("List", "POP", start, end)
