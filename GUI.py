import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# -------------------- Main Window --------------------
app = tk.Tk()
app.title("Pharmacy Inventory Management System")

# Apply full-screen dimensions
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}+0+0")

# -------------------- Title Frame --------------------
title_frame = tk.Frame(app, bg="white")
title_frame.pack(side="top", fill="x")

title_label = tk.Label(
    title_frame,
    text="PHARMACY INVENTORY SYSTEM",
    font=("Arial", 35, "bold"),
    fg="blue",
    bg="white"
)
title_label.pack(pady=20)

# -------------------- Form Frame --------------------
form_frame = tk.Frame(app)
form_frame.pack(pady=10, padx=30, fill="x")

fields = [
    ("Name", 0),
    ("Quantity", 1),
    ("Price", 2),
    ("Expiry Date", 3)
]

entries = {}

for field, row in fields:
    lbl = tk.Label(
        form_frame,
        text=field + ":",
        font=("Arial", 15, "bold")
    )
    lbl.grid(row=row, column=0, sticky="w", pady=5, padx=10)

    ent = tk.Entry(
        form_frame,
        font=("Arial", 14),
        width=30
    )
    ent.grid(row=row, column=1, pady=5, padx=10)
    entries[field] = ent

# -------------------- Button Frame --------------------
button_frame = tk.Frame(app)
button_frame.pack(pady=20)

buttons = ["ADD DATA", "READ DATA", "UPDATE", "DELETE", "RESET", "EXIT"]
for btn_text in buttons:
    btn = tk.Button(
        button_frame,
        text=btn_text,
        width=15,
        font=("Arial", 15, "bold")
    )
    btn.pack(side="left", padx=10)

# -------------------- Table Frame --------------------
table_frame = tk.Frame(app)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
scroll_y = tk.Scrollbar(table_frame, orient="vertical")

product_table = ttk.Treeview(
    table_frame,
    columns=("medicineID" , "name", "qty", "price", "expiry"),
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
scroll_x.config(command=product_table.xview)
scroll_y.config(command=product_table.yview)

# Table Headings
product_table.heading("medicineID", text="medicineID")
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

# -------------------- Table Font Styling --------------------
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 15, "bold"))
style.configure("Treeview", font=("Arial", 14))

# -------------------- Launch --------------------
app.mainloop()
