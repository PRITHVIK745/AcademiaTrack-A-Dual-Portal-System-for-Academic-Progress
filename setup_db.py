# setup_db.py
import sqlite3

# --- Setup students.db ---
con = sqlite3.connect('students.db')
con.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        marks INTEGER,
        attendance INTEGER
    )
""")
con.execute("INSERT INTO students (username, password, marks, attendance) VALUES ('student1', 'pass123', 75, 90)")
con.execute("INSERT INTO students (username, password, marks, attendance) VALUES ('student2', 'pass456', 85, 95)")
con.commit()
con.close()

# --- Setup teachers.db ---
con = sqlite3.connect('teachers.db')
con.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
""")
con.execute("INSERT INTO teachers (username, password) VALUES ('teacher1', 'admin123')")
con.commit()
con.close()

# --- Setup logins.db ---
con = sqlite3.connect('logins.db')
con.execute("""
    CREATE TABLE IF NOT EXISTS logins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        role TEXT,
        timestamp TEXT
    )
""")
con.commit()
con.close()

print("Databases created successfully.")
