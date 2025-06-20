# === LIBRARY BOOK LINKED LIST (SINGLE-FILE IMPLEMENTATION) ===
import tkinter as tk
from tkinter import ttk


# --- 1. NODE CLASS ---
class BookNode:
    def __init__(self, title, author, isbn):
        self.title = title  # Book title (string)
        self.author = author  # Author name (string)
        self.isbn = isbn  # Unique ID (string/int)
        self.available = True  # Availability status
        self.next = None  # Pointer to next node


# --- 2. LINKED LIST CLASS ---
class BookLinkedList:
    def __init__(self):
        self.head = None  # First book
        self.tail = None  # Last book (optimizes appends)
        self.size = 0  # Track total books

    # --- CORE METHODS ---
    def add_book(self, title, author, isbn):
        """Adds book to END of list (O(1) with tail pointer)"""
        new_node = BookNode(title, author, isbn)
        if not self.head:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1
        return f"Added: {title}"

    def delete_book(self, isbn):
        """Removes book by ISBN (O(n) traversal)"""
        current = self.head
        previous = None

        while current:
            if current.isbn == isbn:
                if previous:
                    previous.next = current.next
                    if not current.next:  # Update tail if deleting last
                        self.tail = previous
                else:
                    self.head = current.next
                    if not self.head:  # List is now empty
                        self.tail = None
                self.size -= 1
                return f"Deleted: {current.title}"
            previous = current
            current = current.next
        return "Book not found"

    def search_by_title(self, title):
        """Returns first matching book (O(n))"""
        current = self.head
        while current:
            if current.title.lower() == title.lower():
                return current
            current = current.next
        return None

    # --- UTILITY METHODS ---
    def get_all_books(self):
        """Returns list of dicts (for GUI integration)"""
        books = []
        current = self.head
        while current:
            books.append({
                "title": current.title,
                "author": current.author,
                "isbn": current.isbn,
                "available": current.available
            })
            current = current.next
        return books

    def display_console(self):
        """Prints all books to console (debugging)"""
        current = self.head
        while current:
            status = "Available" if current.available else "Checked Out"
            print(f"{current.title} by {current.author} (ISBN: {current.isbn}) - {status}")
            current = current.next


# --- 3. DEMO GUI INTEGRATION ---
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = BookLinkedList()  # Linked List instance

        # Sample data
        self.books.add_book("The Hobbit", "J.R.R. Tolkien", "111")
        self.books.add_book("1984", "George Orwell", "222")

        # GUI Setup
        self.tree = ttk.Treeview(columns=("Title", "Author", "ISBN", "Status"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Status", text="Status")
        self.tree.pack(padx=10, pady=10)

        # Buttons
        tk.Button(text="Refresh List", command=self.update_display).pack()
        tk.Button(text="Add Test Book", command=self.add_test_book).pack()

        self.update_display()

    def update_display(self):
        """Updates GUI with current book data"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for book in self.books.get_all_books():
            status = "✓" if book["available"] else "✗"
            self.tree.insert("", "end", values=(
                book["title"],
                book["author"],
                book["isbn"],
                status
            ))

    def add_test_book(self):
        """Demo method for testing"""
        self.books.add_book("Dune", "Frank Herbert", "333")
        self.update_display()


# --- 4. TEST CASES ---
def run_tests():
    print("\n=== RUNNING TESTS ===")
    test_list = BookLinkedList()

    # Test add
    test_list.add_book("Test Book", "Test Author", "123")
    assert test_list.size == 1, "Add failed"

    # Test search
    assert test_list.search_by_title("test book").isbn == "123", "Search failed"

    # Test delete
    test_list.delete_book("123")
    assert test_list.size == 0, "Delete failed"
    print("All tests passed!")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    run_tests()  # Verify functionality

    # Launch demo GUI
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()