import sqlite3

class SQLiteService:
    def __init__(self, filename="app_data.db"):
        self.conn = sqlite3.connect(filename)
        self._ensure_table()

    def _ensure_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                details TEXT
            )"""
        )
        self.conn.commit()

    def create_item(self, title, details):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO items (title, details) VALUES (?, ?)", (title, details))
        self.conn.commit()
        return cur.lastrowid

    def read_all(self):
        return self.conn.execute("SELECT id, title, details FROM items").fetchall()

    def update_item(self, item_id, title, details):
        self.conn.execute(
            "UPDATE items SET title=?, details=? WHERE id=?",
            (title, details, item_id)
        )
        self.conn.commit()

    def delete_item(self, item_id):
        self.conn.execute("DELETE FROM items WHERE id=?", (item_id,))
        self.conn.commit()