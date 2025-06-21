# === LIBRARY BOOK LINKED LIST WITH DROPDOWN ADD ===
import tkinter as tk
from tkinter import ttk, messagebox


# --- 1. NODE CLASS (unchanged) ---
class BookNode:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.next = None


# --- 2. LINKED LIST CLASS (unchanged) ---
class BookLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_book(self, title, author, isbn):
        new_node = BookNode(title, author, isbn)
        if not self.head:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1
        return f"Added: {title}"

    def delete_book(self, isbn):
        current = self.head
        previous = None

        while current:
            if current.isbn == isbn:
                if previous:
                    previous.next = current.next
                    if not current.next:
                        self.tail = previous
                else:
                    self.head = current.next
                    if not self.head:
                        self.tail = None
                self.size -= 1
                return f"Deleted: {current.title}"
            previous = current
            current = current.next
        return "Book not found"

    def search_by_title(self, title):
        current = self.head
        while current:
            if current.title.lower() == title.lower():
                return current
            current = current.next
        return None

    def get_all_books(self):
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


# --- 3. ENHANCED GUI WITH DROPDOWN ---
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker with Dropdown")
        self.books = BookLinkedList()

        # Predefined book options for dropdown
        self.book_options = [
            ("The Hobbit", "J.R.R. Tolkien", "111"),
            ("1984", "George Orwell", "222"),
            ("Dune", "Frank Herbert", "333"),
            ("To Kill a Mockingbird", "Harper Lee", "444"),
            ("The Great Gatsby", "F. Scott Fitzgerald", "555"),
            ("Pride and Prejudice", "Jane Austen", "666"),
            ("The Catcher in the Rye", "J.D. Salinger", "777"),
            ("Brave New World", "Aldous Huxley", "888"),
            ("The Lord of the Rings", "J.R.R. Tolkien", "999"),
            ("Animal Farm", "George Orwell", "1010")
        ]

        # Main container frame
        main_frame = tk.Frame(root)
        main_frame.pack(padx=20, pady=20)

        # Dropdown section
        dropdown_frame = tk.Frame(main_frame)
        dropdown_frame.pack(fill=tk.X, pady=10)

        self.selected_book = tk.StringVar()
        self.selected_book.set("Select a book")  # Default option

        # Dropdown menu
        self.book_dropdown = ttk.Combobox(
            dropdown_frame,
            textvariable=self.selected_book,
            values=[book[0] for book in self.book_options],
            state="readonly"
        )
        self.book_dropdown.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Add button
        add_button = tk.Button(
            dropdown_frame,
            text="Add Book",
            command=self.add_from_dropdown
        )
        add_button.pack(side=tk.LEFT, padx=10)

        # Treeview display
        self.tree = ttk.Treeview(
            main_frame,
            columns=("Title", "Author", "ISBN", "Status"),
            show="headings"
        )
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Delete button
        delete_button = tk.Button(
            main_frame,
            text="Delete Selected",
            command=self.delete_selected
        )
        delete_button.pack(pady=10)

        # Initialize with sample data
        self.update_display()

    def add_from_dropdown(self):
        """Adds the selected book from dropdown"""
        selected_title = self.selected_book.get()

        if selected_title == "Select a book":
            messagebox.showwarning("Warning", "Please select a book first!")
            return

        # Find the selected book in our options
        for title, author, isbn in self.book_options:
            if title == selected_title:
                # Check if book already exists
                if self.books.search_by_title(title):
                    messagebox.showwarning("Warning", f"'{title}' already exists!")
                    return

                self.books.add_book(title, author, isbn)
                self.update_display()
                messagebox.showinfo("Success", f"Added: {title}")
                return

        messagebox.showerror("Error", "Book not found in options!")

    def delete_selected(self):
        """Properly deletes the selected book from both the Treeview and linked list"""
        selected_items = self.tree.selection()  # Get selected items

        if not selected_items:
            messagebox.showwarning("Warning", "Please select a book to delete first!")
            return

        # Get the first selected item (in case multiple are selected)
        selected_item = selected_items[0]

        # Get all values from the selected row
        item_values = self.tree.item(selected_item)['values']

        # Ensure we have enough values (title, author, ISBN, status)
        if len(item_values) < 3:
            messagebox.showerror("Error", "Invalid book data in selection")
            return

        selected_isbn = item_values[2]  # ISBN is the 3rd value (index 2)

        # Debug print (you can remove this later)
        print(f"Attempting to delete book with ISBN: {selected_isbn}")
        print(f"Current books in list: {[book['isbn'] for book in self.books.get_all_books()]}")

        # Delete from linked list
        result = self.books.delete_book(selected_isbn)

        if result.startswith("Deleted"):
            # Success - update display
            self.tree.delete(selected_item)
            messagebox.showinfo("Success", result)
        else:
            # Failure - show error
            messagebox.showerror("Error", result)

        # Force refresh of the display
        self.update_display()

    def update_display(self):
        """Updates the Treeview with current books"""
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


# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()