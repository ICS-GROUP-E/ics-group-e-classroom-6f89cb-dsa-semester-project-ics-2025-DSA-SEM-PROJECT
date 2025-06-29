# pharmacy_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from pharmacy import Pharmacy
from PIL import Image, ImageTk

class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Inventory System")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        
        self.bg_image = Image.open("data/hospital_bg.jpg")
        self.bg_image = self.bg_image.resize((900, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        
        self.content = tk.Frame(root, bg="#f8faff", bd=2)
        self.content.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        
        self.name_var = tk.StringVar()
        self.stock_var = tk.IntVar(value=0)
        self.price_var = tk.DoubleVar(value=0.0)
        self.pharmacy = Pharmacy()

        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#0078D4", foreground="white")
        style.map("TButton", background=[("active", "#005a9e")])
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25, fieldbackground="#e9f0fa")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#0078D4", foreground="white")

        
        tk.Label(self.content, text="Medicine Name:", font=("Segoe UI", 10), bg="#f8faff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(self.content, textvariable=self.name_var, font=("Segoe UI", 10)).grid(row=0, column=1, padx=5)

        tk.Label(self.content, text="Stock:", font=("Segoe UI", 10), bg="#f8faff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(self.content, textvariable=self.stock_var, font=("Segoe UI", 10)).grid(row=1, column=1, padx=5)

        tk.Label(self.content, text="Price:", font=("Segoe UI", 10), bg="#f8faff").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(self.content, textvariable=self.price_var, font=("Segoe UI", 10)).grid(row=2, column=1, padx=5)

        
        ttk.Button(self.content, text="Add", command=self.add_medicine).grid(row=0, column=2, padx=10)
        ttk.Button(self.content, text="Update", command=self.update_medicine).grid(row=1, column=2, padx=10)
        ttk.Button(self.content, text="Delete", command=self.delete_medicine).grid(row=2, column=2, padx=10)
        ttk.Button(self.content, text="Search", command=self.search_medicine).grid(row=3, column=2, padx=10)
        ttk.Button(self.content, text="Refresh Inventory", command=self.load_inventory).grid(row=3, column=0, columnspan=2, pady=10)

        
        self.tree = ttk.Treeview(self.content, columns=("Name", "Stock", "Price"), show="headings")
        self.tree.heading("Name", text="Medicine Name")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Price", text="Price")
        self.tree.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        
        self.status_label = tk.Label(self.content, text="", fg="blue", bg="#f8faff", font=("Segoe UI", 10))
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
        name = self.name_var.get().strip()
        result = self.pharmacy.search_medicine(name)
        if result:
            self.stock_var.set(result["stock"])
            self.price_var.set(result["price"])
            self.status_label.config(text=f"Found: {name}", fg="green")
        else:
            self.status_label.config(text="Medicine not found.", fg="red")

    def load_inventory(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for name, data in self.pharmacy.get_all_medicines().items():
            self.tree.insert("", "end", values=(name, data["stock"], data["price"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()
