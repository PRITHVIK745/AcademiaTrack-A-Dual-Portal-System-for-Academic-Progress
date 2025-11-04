import sqlite3
import csv

# --- Students DB ---
con = sqlite3.connect('students.db')
con.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        marks INTEGER,
        attendance INTEGER,
        branch TEXT
    )
""")

with open('students.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            con.execute("INSERT INTO students (username, password, marks, attendance, branch) VALUES (?, ?, ?, ?, ?)",
                        (row['username'], row['password'], row['marks'], row['attendance'], row['branch']))
        except sqlite3.IntegrityError:
            pass  # Skip if username already exists
con.commit()
con.close()

# --- Teachers DB ---
con = sqlite3.connect('teachers.db')
con.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        branch TEXT
    )
""")

with open('teachers.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            con.execute("INSERT INTO teachers (username, password, branch) VALUES (?, ?, ?)",
                        (row['username'], row['password'], row['branch']))
        except sqlite3.IntegrityError:
            pass
con.commit()
con.close()

print("Students and Teachers imported successfully.")
