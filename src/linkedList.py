# === LIBRARY BOOK LINKED LIST (CORE IMPLEMENTATION) ===

# --- 1. NODE CLASS ---
class Node:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.next = None


# --- 2. LINKED LIST CLASS ---
class BookLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_book(self, title, author, isbn):
        new_node = Node(title, author, isbn)
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
            if str(current.isbn) == str(isbn).strip():
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


# --- 3. SAMPLE USAGE ---
if __name__ == "__main__":
    library = BookLinkedList()

    # Add some books