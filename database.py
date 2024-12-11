# database.py

import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('hospital_management.db')
cursor = conn.cursor()

# Create Hospital table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Hospital (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
''')

# Create Management table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Management (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manager_name TEXT NOT NULL,
        contact_number TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
