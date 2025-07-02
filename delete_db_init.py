import sqlite3


conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        name TEXT PRIMARY KEY,
        quantity INTEGER,
        price REAL,
        expiry TEXT
    )
''')

#Insert sample data
cursor.executemany('''
    INSERT OR IGNORE INTO medicines (name, quantity, price, expiry) VALUES (?, ?, ?, ?)
''', [
    ('Paracetamol', 20, 50.0, '2026-06-01'),
    ('Amoxil', 10, 120.0, '2025-12-30'),
    ('Panadol', 15, 60.0, '2027-01-10')
])

conn.commit()
conn.close()
