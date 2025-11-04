# setup_notes_db.py
import sqlite3

con = sqlite3.connect('notes.db')
con.execute("DROP TABLE IF EXISTS notes")

con.execute("""
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch TEXT,
    year INTEGER,
    semester INTEGER,
    subject TEXT,
    filename TEXT,
    uploaded_at TEXT
)
""")

con.commit()
con.close()
print("✅ notes.db ready.")
