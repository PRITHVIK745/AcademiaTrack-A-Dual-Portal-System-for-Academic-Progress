import sqlite3

con = sqlite3.connect('students.db')
cursor = con.cursor()

# Try to add 'year' column
try:
    cursor.execute("ALTER TABLE students ADD COLUMN year INTEGER")
    print("✅ 'year' column added.")
except sqlite3.OperationalError as e:
    print("⚠️", e)

# Try to add 'semester' column
try:
    cursor.execute("ALTER TABLE students ADD COLUMN semester INTEGER")
    print("✅ 'semester' column added.")
except sqlite3.OperationalError as e:
    print("⚠️", e)

# Optional: Add 'marks' and 'attendance' columns if not already present
try:
    cursor.execute("ALTER TABLE students ADD COLUMN marks TEXT DEFAULT ''")
    print("✅ 'marks' column added.")
except sqlite3.OperationalError as e:
    print("⚠️", e)

try:
    cursor.execute("ALTER TABLE students ADD COLUMN attendance TEXT DEFAULT ''")
    print("✅ 'attendance' column added.")
except sqlite3.OperationalError as e:
    print("⚠️", e)

con.commit()
con.close()
print("\n🎉 All required columns are now present in 'students' table.")
