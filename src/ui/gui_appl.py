import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from src.data_struct.Bsearch import BinarySearchTree
from src.database.sqlite import SQLiteService

class GUIApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.storage = SQLiteService()
        self.bst = BinarySearchTree(log_fn=self._log)
        self._load_data()

        self.pack(fill=tk.BOTH, expand=True)

        # --- INSERT SECTION ---
        insert_frame = ttk.LabelFrame(self, text="Insert New Node", padding=10)
        insert_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(insert_frame, text="Title:").grid(row=0, column=0)
        self.ins_title_ev = ttk.Entry(insert_frame, width=30)
        self.ins_title_ev.grid(row=0, column=1)

        ttk.Label(insert_frame, text="Details:").grid(row=0, column=2)
        self.ins_detail_ev = ttk.Entry(insert_frame, width=30)
        self.ins_detail_ev.grid(row=0, column=3)

        ttk.Button(insert_frame, text="Insert", command=self.insert).grid(row=0, column=4, padx=5)

        # --- UPDATE SECTION ---
        update_frame = ttk.LabelFrame(self, text="Update Existing Node", padding=10)
        update_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(update_frame, text="ID:").grid(row=0, column=0)
        self.upd_id_ev = ttk.Entry(update_frame, width=10)
        self.upd_id_ev.grid(row=0, column=1)

        ttk.Label(update_frame, text="New Title:").grid(row=0, column=2)
        self.upd_title_ev = ttk.Entry(update_frame, width=30)
        self.upd_title_ev.grid(row=0, column=3)

        ttk.Label(update_frame, text="New Details:").grid(row=0, column=4)
        self.upd_detail_ev = ttk.Entry(update_frame, width=30)
        self.upd_detail_ev.grid(row=0, column=5)

        ttk.Button(update_frame, text="Update", command=self.update).grid(row=0, column=6, padx=5)

        # --- TREE SUMMARY ---
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self, textvariable=self.status_var, padding=5, relief=tk.GROOVE)
        self.status_label.pack(fill=tk.X, padx=10, pady=(5, 0))

        # --- TREEVIEW ---
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Details"), show="headings")
        for col in ("ID", "Title", "Details"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # --- LOG ---
        ttk.Label(self, text="Log:").pack(anchor=tk.W, padx=10)
        self.log_txt = scrolledtext.ScrolledText(self, height=6)
        self.log_txt.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

        self.refresh()

    def _log(self, msg):
        self.log_txt.insert(tk.END, msg + "\n")
        self.log_txt.see(tk.END)

    def _load_data(self):
        for i, t, d in self.storage.read_all():
            self.bst.insert(i, (t, d))

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        nodes = list(self.bst.inorder())  # 🔧 FIXED: convert generator to list

        for k, (t, d) in nodes:
            self.tree.insert("", tk.END, values=(k, t, d))

        # Update status summary
        if not nodes:
            self.status_var.set("🔴 Tree is Empty")
        else:
            ids = [str(k) for k, _ in nodes]
            self.status_var.set(f"🟢 Tree contains {len(nodes)} nodes. Inorder Traversal: [{', '.join(ids)}]")

    def insert(self):
        t = self.ins_title_ev.get()
        d = self.ins_detail_ev.get()
        if not t or not d:
            messagebox.showwarning("Input Error", "Both Title and Details are required.")
            return
        i = self.storage.create_item(t, d)
        self.bst.insert(i, (t, d))
        self._log(f"Inserted: ID={i}, Title={t}")
        self.refresh()

    def update(self):
        try:
            k = int(self.upd_id_ev.get())
        except ValueError:
            messagebox.showwarning("Input Error", "ID must be a number.")
            return
        t = self.upd_title_ev.get()
        d = self.upd_detail_ev.get()
        if not t or not d:
            messagebox.showwarning("Input Error", "Both Title and Details are required.")
            return
        self.storage.update_item(k, t, d)
        self.bst.insert(k, (t, d))
        self._log(f"Updated: ID={k}, Title={t}")
        self.refresh()
