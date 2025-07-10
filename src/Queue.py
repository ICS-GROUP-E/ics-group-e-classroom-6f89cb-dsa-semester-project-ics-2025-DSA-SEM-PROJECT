from collections import deque

class LibrarySystem:
    def __init__(self):
        self.books = {}  # book_id: {title, available_copies, checked_out_to, reservation_queue}

    def add_book(self, book_id, title, copies):
        self.books[book_id] = {
            'title': title,
            'available_copies': copies,
            'checked_out_to': [],
            'reservation_queue': deque()
        }

    def check_out_book(self, user_id, book_id):
        if book_id not in self.books:
            print(" Book not found.")
            return False

        book = self.books[book_id]

        if book['available_copies'] > 0:
            book['available_copies'] -= 1
            book['checked_out_to'].append(user_id)
            print(f" {user_id} successfully checked out '{book['title']}'. Copies left: {book['available_copies']}")
            return True
        else:
            # Add to reservation queue
            if user_id not in book['reservation_queue']:
                book['reservation_queue'].append(user_id)
                print(f" No copies available. {user_id} added to waitlist at position {len(book['reservation_queue'])}")
            else:
                print(f" {user_id} is already in the waitlist.")
            return False

    def return_book(self, book_id, user_id):
        if book_id not in self.books:
            print(" Book not found.")
            return

        book = self.books[book_id]

        if user_id in book['checked_out_to']:
            book['checked_out_to'].remove(user_id)
            book['available_copies'] += 1
            print(f" {user_id} returned '{book['title']}'. Copies now: {book['available_copies']}")

            # Notify next in queue
            if book['reservation_queue']:
                next_user = book['reservation_queue'].popleft()
                book['available_copies'] -= 1
                book['checked_out_to'].append(next_user)
                print(f" Notified {next_user} — they now have the book '{book['title']}'. Copies left: {book['available_copies']}")
            else:
                print(" No reservations in queue.")
        else:
            print(" This user did not check out this book.")

    def view_book_status(self, book_id):
        if book_id not in self.books:
            print(" Book not found.")
            return
        book = self.books[book_id]
        print(f"\n Book: {book['title']}")
        print(f"Available copies: {book['available_copies']}")
        print(f"Checked out to: {book['checked_out_to']}")
        print(f"Waitlist queue: {list(book['reservation_queue'])}")
