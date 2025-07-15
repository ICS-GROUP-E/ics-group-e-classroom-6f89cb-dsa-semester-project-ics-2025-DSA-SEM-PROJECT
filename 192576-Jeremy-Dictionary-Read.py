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
