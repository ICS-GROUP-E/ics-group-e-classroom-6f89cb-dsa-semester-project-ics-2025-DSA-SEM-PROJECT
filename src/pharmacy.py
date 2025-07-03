# Storing available medicine using dictionaries and using sets to prevent duplicate entries.

import sqlite3
import os

class Pharmacy:
    def __init__(self, db_file="data/hospital.db"):
        
        os.makedirs(os.path.dirname(db_file), exist_ok=True)

        
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                name TEXT PRIMARY KEY,
                stock INTEGER NOT NULL CHECK(stock >= 0),
                price REAL NOT NULL CHECK(price >= 0)
            )
        """)
        self.conn.commit()

    def add_medicine(self, name, stock, price):
        name = name.strip().capitalize()
        try:
            self.cur.execute("INSERT INTO medicines (name, stock, price) VALUES (?, ?, ?)", (name, stock, price))
            self.conn.commit()
            return f"{name} added successfully."
        except sqlite3.IntegrityError:
            return f"{name} already exists."

    def update_medicine(self, name, stock=None, price=None):
        name = name.strip().capitalize()
        self.cur.execute("SELECT * FROM medicines WHERE name = ?", (name,))
        if not self.cur.fetchone():
            return f"{name} not found."

        if stock is not None and price is not None:
            self.cur.execute("UPDATE medicines SET stock = ?, price = ? WHERE name = ?", (stock, price, name))
        elif stock is not None:
            self.cur.execute("UPDATE medicines SET stock = ? WHERE name = ?", (stock, name))
        elif price is not None:
            self.cur.execute("UPDATE medicines SET price = ? WHERE name = ?", (price, name))

        self.conn.commit()
        return f"{name} updated."

    def delete_medicine(self, name):
        name = name.strip().capitalize()
        self.cur.execute("DELETE FROM medicines WHERE name = ?", (name,))
        self.conn.commit()
        if self.cur.rowcount == 0:
            return f"{name} not found."
        return f"{name} removed."

    def search_medicine(self, name):
        name = name.strip().capitalize()
        self.cur.execute("SELECT stock, price FROM medicines WHERE name = ?", (name,))
        row = self.cur.fetchone()
        if row:
            return {"stock": row[0], "price": row[1]}
        return None

    def get_all_medicines(self):
        self.cur.execute("SELECT name, stock, price FROM medicines ORDER BY name ASC")
        rows = self.cur.fetchall()
        return {name: {"stock": stock, "price": price} for name, stock, price in rows}

    def __del__(self):
        self.conn.close()
