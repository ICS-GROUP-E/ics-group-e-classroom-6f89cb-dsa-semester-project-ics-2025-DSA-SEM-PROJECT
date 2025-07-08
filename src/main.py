import tkinter as tk
from tkinter import ttk
from src.ui.gui_appl import GUIApp  # BST Tab

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DSA app")
        self.geometry("1000x600")

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Add tabs
        bst_tab = GUIApp(notebook)
        notebook.add(bst_tab, text="Binary Tree (UPDATE)")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
