import sqlite3

def add_columns(db_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    for i in range(1, 7):  # sub1 to sub6
        for ia in ['ia1', 'ia2', 'ia3']:
            mark_col = f"sub{i}_{ia}"
            att_col = f"sub{i}_att{ia[-1]}"

            try:
                cursor.execute(f"ALTER TABLE marks ADD COLUMN {mark_col} TEXT")
                print(f"✔ Added column {mark_col} to {db_name}")
            except sqlite3.OperationalError:
                print(f"• Column {mark_col} already exists in {db_name}")

            try:
                cursor.execute(f"ALTER TABLE marks ADD COLUMN {att_col} TEXT")
                print(f"✔ Added column {att_col} to {db_name}")
            except sqlite3.OperationalError:
                print(f"• Column {att_col} already exists in {db_name}")

    con.commit()
    con.close()

# Apply to sem1 to sem7
for sem in range(1, 8):
    add_columns(f"sem{sem}.db")
