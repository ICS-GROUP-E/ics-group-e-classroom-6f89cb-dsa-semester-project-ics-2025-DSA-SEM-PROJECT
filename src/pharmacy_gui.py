# pharmacy_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from pharmacy import Pharmacy

class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Inventory System")
        self.pharmacy = Pharmacy()
        
        
        self.name_var = tk.StringVar()
        self.stock_var = tk.IntVar()
        self.price_var = tk.DoubleVar()

        tk.Label(root, text="Medicine Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(root, textvariable=self.name_var).grid(row=0, column=1, padx=5)

        tk.Label(root, text="Stock:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(root, textvariable=self.stock_var).grid(row=1, column=1, padx=5)

        tk.Label(root, text="Price:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(root, textvariable=self.price_var).grid(row=2, column=1, padx=5)

        
        tk.Button(root, text="Add", command=self.add_medicine).grid(row=0, column=2, padx=10)
        tk.Button(root, text="Update", command=self.update_medicine).grid(row=1, column=2, padx=10)
        tk.Button(root, text="Delete", command=self.delete_medicine).grid(row=2, column=2, padx=10)
        tk.Button(root, text="Search", command=self.search_medicine).grid(row=3, column=2, padx=10)
        tk.Button(root, text="Refresh Inventory", command=self.load_inventory).grid(row=3, column=0, columnspan=2, pady=5)

        
        self.tree = ttk.Treeview(root, columns=("Name", "Stock", "Price"), show="headings")
        self.tree.heading("Name", text="Medicine Name")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Price", text="Price")
        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        
        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.grid(row=5, column=0, columnspan=3)

        self.load_inventory()

    def add_medicine(self):
     name = self.name_var.get().strip()
     try:
        stock = int(self.stock_var.get())
        price = float(self.price_var.get())
     except ValueError:
        self.status_label.config(text="Stock and price must be numbers.", fg="red")
        return

     if not name:
        self.status_label.config(text="Medicine name is required.", fg="red")
        return
     if stock < 0 or price < 0:
        self.status_label.config(text="Stock and price must be non-negative.", fg="red")
        return

     msg = self.pharmacy.add_medicine(name, stock, price)
     self.status_label.config(text=msg, fg="green" if "success" in msg.lower() else "red")
     self.load_inventory()


    def update_medicine(self):
     name = self.name_var.get().strip()
     try:
        stock = int(self.stock_var.get())
        price = float(self.price_var.get())
     except ValueError:
        self.status_label.config(text="Stock and price must be numbers.", fg="red")
        return

     if not name:
        self.status_label.config(text="Medicine name is required.", fg="red")
        return
     if stock < 0 or price < 0:
        self.status_label.config(text="Stock and price must be non-negative.", fg="red")
        return

     msg = self.pharmacy.update_medicine(name, stock, price)
     self.status_label.config(text=msg, fg="green" if "updated" in msg.lower() else "red")
     self.load_inventory()

    def delete_medicine(self):
     name = self.name_var.get().strip()
     if not name:
        self.status_label.config(text="Enter a medicine name to delete.", fg="red")
        return
     msg = self.pharmacy.delete_medicine(name)
     self.status_label.config(text=msg, fg="green" if "removed" in msg.lower() else "red")
     self.load_inventory()


    def search_medicine(self):
        name = self.name_var.get()
        result = self.pharmacy.search_medicine(name)
        if result:
            self.stock_var.set(result["stock"])
            self.price_var.set(result["price"])
            self.status_label.config(text=f"Found: {name}")
        else:
            self.status_label.config(text="Medicine not found.")

    def load_inventory(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for name, data in self.pharmacy.get_all_medicines().items():
            self.tree.insert("", "end", values=(name, data["stock"], data["price"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()
