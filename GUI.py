import tkinter as tk
from tkinter import ttk, messagebox


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
                         bg="white",fg="black",width=15)
insertButton.grid(row=0, column=4, pady=10, padx=50)

updateButton = tk.Button(formFrame,text="Update Data",font=("Calibri", 12),
                         bg="white",fg="black",width=15)
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
                          bg="white", fg="black", width=15)
search_button.grid(row=0, column=2, padx=50, pady=10)
#Delete data frame------------------------------------------------------------------------------------------------------
deleteFrame = tk.LabelFrame(spane, text="Delete data", fg="black", font=("Calibri", 10, "bold"), bd=2)
deleteFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


delete_label = tk.Label(deleteFrame, text="           Name:", font=("Calibri", 12))
delete_label.grid(row=0, column=0, padx=5, pady=10, sticky="e")

delete_entry = tk.Entry(deleteFrame, font=("Calibri", 12), width=30)
delete_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

delete_button = tk.Button(deleteFrame, text="Delete Data", font=("Calibri", 12),
                          bg="white", fg="black", width=15)
delete_button.grid(row=0, column=2, padx=5, pady=10)

undo_button = tk.Button(deleteFrame, text="Undo", font=("Calibri", 12),
                          bg="white", fg="black", width=10)
undo_button.grid(row=0, column=3, padx=5, pady=10)
#Report frame-----------------------------------------------------------------------------------------------------------
reportFrame = tk.LabelFrame(root, text="Report", fg="black", font=("Calibri", 10, "bold"), bd=2)
reportFrame.pack( padx=10, pady=10, fill = "x")

report_button = tk.Button(reportFrame, text="Download report", font=("Calibri", 12),
                          bg="white", fg="black", width=15)
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
root.mainloop()

