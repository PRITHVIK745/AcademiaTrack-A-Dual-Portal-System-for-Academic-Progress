# check_columns.py

import sqlite3

db_name = 'sem1.db'  # Change this if checking other sems

con = sqlite3.connect(db_name)
cursor = con.cursor()

# List all columns in the 'marks' table
cursor.execute("PRAGMA table_info(marks)")
columns = cursor.fetchall()

print("Columns in 'marks' table:")
for col in columns:
    print(col[1])  # Column name
