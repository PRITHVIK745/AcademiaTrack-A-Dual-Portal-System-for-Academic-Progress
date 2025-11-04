import sqlite3

for sem in range(1, 8):  # For sem1.db to sem7.db
    db_name = f"sem{sem}.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Prepare columns for 6 subjects × (IA1, IA2, IA3, Att1, Att2, Att3)
    fields = ["username TEXT PRIMARY KEY"]
    for i in range(1, 7):
        fields += [
            f"sub{i}_ia1 TEXT", f"sub{i}_att1 TEXT",
            f"sub{i}_ia2 TEXT", f"sub{i}_att2 TEXT",
            f"sub{i}_ia3 TEXT", f"sub{i}_att3 TEXT"
        ]
    fields_sql = ", ".join(fields)

    cursor.execute(f"CREATE TABLE IF NOT EXISTS marks ({fields_sql})")
    conn.commit()
    conn.close()

print("✅ Databases sem1.db to sem7.db created with appropriate marks table structure.")
