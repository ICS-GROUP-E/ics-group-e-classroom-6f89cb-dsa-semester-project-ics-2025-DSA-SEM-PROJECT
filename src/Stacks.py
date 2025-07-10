import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import unittest

# --- 1. DATA STRUCTURES ---

# Stack for activity logs


class ActivityNode:
    def __init__(self, action, details):
        self.action = action
        self.details = details
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.next = None


class ActivityStack:
    def __init__(self):
        self.top = None
        self.size = 0
        self.max_size = 10

    def push(self, action, details):
        new_node = ActivityNode(action, details)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        if self.size > self.max_size:
            self._remove_last()
        return f"Logged: {action}"

    def pop(self):
        if not self.top:
            return None
        popped = self.top
        self.top = self.top.next
        self.size -= 1
        return (popped.action, popped.details, popped.timestamp)

    def peek(self):
        return (self.top.action, self.top.details) if self.top else None

    def _remove_last(self):
        current = self.top
        while current.next and current.next.next:
            current = current.next
        current.next = None
        self.size -= 1

    def get_all_actions(self):
        actions = []
        current = self.top
        while current:
            actions.append({
                "action": current.action,
                "details": current.details,
                "timestamp": current.timestamp
            })
            current = current.next
        return actions

    def clear_stack(self):
        self.top = None
        self.size = 0

# Queue for checkout lines


class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class CheckoutQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        new_node = QueueNode(data)
        if not self.rear:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        if not self.front:
            return None
        data = self.front.data
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self.size -= 1
        return data

    def is_empty(self):
        return self.size == 0

# Linked List for book history


class HistoryNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class BookHistory:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = HistoryNode(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements)

# Binary Search Tree for efficient searches


class BSTNode:
    def __init__(self, isbn, title, author, status):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.status = status
        self.left = None
        self.right = None


class BookBST:
    def __init__(self):
        self.root = None

    def insert(self, isbn, title, author, status):
        if not self.root:
            self.root = BSTNode(isbn, title, author, status)
        else:
            self._insert_recursive(self.root, isbn, title, author, status)

    def _insert_recursive(self, node, isbn, title, author, status):
        if isbn < node.isbn:
            if node.left is None:
                node.left = BSTNode(isbn, title, author, status)
            else:
                self._insert_recursive(node.left, isbn, title, author, status)
        else:
            if node.right is None:
                node.right = BSTNode(isbn, title, author, status)
            else:
                self._insert_recursive(node.right, isbn, title, author, status)

    def search(self, isbn):
        return self._search_recursive(self.root, isbn)

    def _search_recursive(self, node, isbn):
        if node is None or node.isbn == isbn:
            return node
        if isbn < node.isbn:
            return self._search_recursive(node.left, isbn)
        return self._search_recursive(node.right, isbn)

# --- 2. BOOK MANAGEMENT CLASS ---


class BookManager:
    def __init__(self, db_name="library.db"):
        self.stack = ActivityStack()
        self.queue = CheckoutQueue()
        self.history = BookHistory()
        self.bst = BookBST()
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                          (isbn TEXT PRIMARY KEY, title TEXT, author TEXT, status TEXT)''')
        self.conn.commit()

    def add_book(self, isbn, title, author):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO books (isbn, title, author, status) VALUES (?, ?, ?, ?)",
                           (isbn, title, author, "Available"))
            self.conn.commit()
            self.stack.push("ADD", f"ISBN: {isbn}, Title: {title}")
            self.history.append(f"Added: {title} by {author}")
            self.bst.insert(isbn, title, author, "Available")
            return True
        except sqlite3.IntegrityError:
            return False

    def search_book(self, isbn):
        book = self.bst.search(isbn)
        if book:
            return (book.isbn, book.title, book.author, book.status)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        return cursor.fetchone()

    def update_book(self, isbn, title=None, author=None, status=None):
        cursor = self.conn.cursor()
        book = self.search_book(isbn)
        if book:
            new_title = title if title else book[1]
            new_author = author if author else book[2]
            new_status = status if status else book[3]
            cursor.execute("UPDATE books SET title = ?, author = ?, status = ? WHERE isbn = ?",
                           (new_title, new_author, new_status, isbn))
            self.conn.commit()
            self.stack.push("UPDATE", f"ISBN: {isbn}, Title: {new_title}")
            self.history.append(f"Updated: {new_title}")
            self.bst._insert_recursive(
                self.bst.root, isbn, new_title, new_author, new_status)
            return True
        return False

    def delete_book(self, isbn):
        cursor = self.conn.cursor()
        book = self.search_book(isbn)
        if book:
            cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
            self.conn.commit()
            self.stack.push("DELETE", f"ISBN: {isbn}, Title: {book[1]}")
            self.history.append(f"Deleted: {book[1]}")
            # Simplified BST deletion (for demo, remove and reinsert others)
            self.bst.root = None
            cursor.execute("SELECT * FROM books")
            for row in cursor.fetchall():
                self.bst.insert(row[0], row[1], row[2], row[3])
            return True
        return False

    def checkout_book(self, isbn, user):
        book = self.search_book(isbn)
        if book and book[3] == "Available":
            self.update_book(isbn, status="Checked Out")
            self.queue.enqueue(f"ISBN: {isbn}, User: {user}")
            self.stack.push("CHECKOUT", f"ISBN: {isbn}, User: {user}")
            return True
        return False

    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()

# --- 3. DEMO GUI INTEGRATION ---


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.manager = BookManager()

        # GUI Setup
        tk.Label(root, text="ISBN:").grid(row=0, column=0)
        self.isbn_entry = tk.Entry(root)
        self.isbn_entry.grid(row=0, column=1)

        tk.Label(root, text="Title:").grid(row=1, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=1, column=1)

        tk.Label(root, text="Author:").grid(row=2, column=0)
        self.author_entry = tk.Entry(root)
        self.author_entry.grid(row=2, column=1)

        tk.Label(root, text="User (for Checkout):").grid(row=3, column=0)
        self.user_entry = tk.Entry(root)
        self.user_entry.grid(row=3, column=1)

        tk.Button(root, text="Add Book", command=self.add_book).grid(
            row=4, column=0)
        tk.Button(root, text="Search Book",
                  command=self.search_book).grid(row=4, column=1)
        tk.Button(root, text="Update Book",
                  command=self.update_book).grid(row=5, column=0)
        tk.Button(root, text="Delete Book",
                  command=self.delete_book).grid(row=5, column=1)
        tk.Button(root, text="Checkout Book",
                  command=self.checkout_book).grid(row=6, column=0)
        tk.Button(root, text="Undo Last",
                  command=self.undo_action).grid(row=6, column=1)
        tk.Button(root, text="Refresh Log",
                  command=self.update_log).grid(row=7, column=0)
        tk.Button(root, text="Show History",
                  command=self.show_history).grid(row=7, column=1)

        self.log_tree = ttk.Treeview(
            columns=("Action", "Details", "Time"), show="headings")
        self.log_tree.heading("Action", text="Action")
        self.log_tree.heading("Details", text="Details")
        self.log_tree.heading("Time", text="Timestamp")
        self.log_tree.grid(row=8, column=0, columnspan=2, pady=10)

        self.history_label = tk.Label(root, text="History: ")
        self.history_label.grid(row=9, column=0, columnspan=2)

        self.update_log()

    def add_book(self):
        isbn = self.isbn_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        if self.manager.add_book(isbn, title, author):
            messagebox.showinfo("Success", "Book added!")
        else:
            messagebox.showerror("Error", "Book already exists!")
        self.update_log()

    def search_book(self):
        isbn = self.isbn_entry.get()
        book = self.manager.search_book(isbn)
        if book:
            messagebox.showinfo(
                "Result", f"Title: {book[1]}, Author: {book[2]}, Status: {book[3]}")
        else:
            messagebox.showerror("Error", "Book not found!")
        self.update_log()

    def update_book(self):
        isbn = self.isbn_entry.get()
        title = self.title_entry.get() or None
        author = self.author_entry.get() or None
        status = "Checked Out" if title or author else None
        if self.manager.update_book(isbn, title, author, status):
            messagebox.showinfo("Success", "Book updated!")
        else:
            messagebox.showerror("Error", "Book not found!")
        self.update_log()

    def delete_book(self):
        isbn = self.isbn_entry.get()
        if self.manager.delete_book(isbn):
            messagebox.showinfo("Success", "Book deleted!")
        else:
            messagebox.showerror("Error", "Book not found!")
        self.update_log()

    def checkout_book(self):
        isbn = self.isbn_entry.get()
        user = self.user_entry.get()
        if self.manager.checkout_book(isbn, user):
            messagebox.showinfo("Success", "Book checked out!")
        else:
            messagebox.showerror("Error", "Book not available!")
        self.update_log()

    def undo_action(self):
        result = self.manager.stack.pop()
        if result:
            messagebox.showinfo(
                "Undo", f"Undid: {result[0]}\nDetails: {result[1]}")
        else:
            messagebox.showwarning("Empty", "No actions to undo!")
        self.update_log()

    def update_log(self):
        for row in self.log_tree.get_children():
            self.log_tree.delete(row)
        for action in self.manager.stack.get_all_actions():
            self.log_tree.insert("", "end", values=(
                action["action"],
                action["details"],
                action["timestamp"]
            ))

    def show_history(self):
        history = self.manager.history.display()
        self.history_label.config(text=f"History: {history}")

# --- 4. UNIT TESTS ---


class TestDataStructures(unittest.TestCase):
    def setUp(self):
        self.manager = BookManager("test.db")

    def test_stack(self):
        self.manager.stack.push("TEST", "Data")
        self.assertEqual(self.manager.stack.size, 1)
        self.assertEqual(self.manager.stack.peek()[0], "TEST")

    def test_queue(self):
        self.manager.queue.enqueue("Data")
        self.assertFalse(self.manager.queue.is_empty())
        self.assertEqual(self.manager.queue.dequeue(), "Data")

    def test_book_add(self):
        self.assertTrue(self.manager.add_book("999", "Test", "Author"))
        book = self.manager.search_book("999")
        self.assertIsNotNone(book)

    def tearDown(self):
        self.manager.conn.close()


if __name__ == "__main__":
    # Run tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # Launch GUI
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
