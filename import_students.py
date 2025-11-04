import sqlite3
import csv
import os
import re

# Connect to the database
con = sqlite3.connect('students.db')
cursor = con.cursor()

student_root = 'student_data'

# Walk through all branch folders
for branch_folder in os.listdir(student_root):
    branch_path = os.path.join(student_root, branch_folder)
    if not os.path.isdir(branch_path):
        continue

    for file in os.listdir(branch_path):
        match = re.match(r'year(\d+)_sem(\d+)\.csv', file)
        if not match:
            print(f"❌ Skipping invalid file: {file}")
            continue

        year, semester = match.groups()
        filepath = os.path.join(branch_path, file)

        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    cursor.execute("""
                        INSERT INTO students (
                            username, password, name, branch, year, semester,
                            sub1_marks, sub2_marks, sub3_marks, sub4_marks, sub5_marks, sub6_marks,
                            sub1_attendance, sub2_attendance, sub3_attendance, sub4_attendance, sub5_attendance, sub6_attendance
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row['username'], row['password'], row['name'], branch_folder, int(year), int(semester),
                        row['sub1_marks'], row['sub2_marks'], row['sub3_marks'], row['sub4_marks'], row['sub5_marks'], row['sub6_marks'],
                        row['sub1_attendance'], row['sub2_attendance'], row['sub3_attendance'], row['sub4_attendance'], row['sub5_attendance'], row['sub6_attendance']
                    ))
                except sqlite3.IntegrityError:
                    print(f"⚠️ Skipping duplicate username: {row['username']}")

con.commit()
con.close()
print("✅ All student data imported successfully.")
