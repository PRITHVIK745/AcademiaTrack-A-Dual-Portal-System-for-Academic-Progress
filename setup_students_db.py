import sqlite3

con = sqlite3.connect('students.db')
con.execute("""
INSERT INTO students (
    username, password, name, branch, year, semester,
    sub1_marks, sub2_marks, sub3_marks, sub4_marks, sub5_marks, sub6_marks,
    sub1_attendance, sub2_attendance, sub3_attendance, sub4_attendance, sub5_attendance, sub6_attendance
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    'csd101', 'pass123', 'John', 'csd', 1, 1,
    '85', '88', '90', '78', '92', '87',
    '90%', '88%', '94%', '85%', '93%', '89%'
))
con.commit()
con.close()
print("✅ Inserted student manually.")
