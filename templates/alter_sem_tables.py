import sqlite3

def add_columns_if_not_exists(db_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    for i in range(1, 7):  # sub1 to sub6
        for ia in ['ia1', 'ia2', 'ia3']:
            mark_col = f"sub{i}_{ia}"
            att_col = f"sub{i}_att{ia[-1]}"
            try:
                cursor.execute(f"ALTER TABLE marks ADD COLUMN {mark_col} TEXT")
            except:
                pass
            try:
                cursor.execute(f"ALTER TABLE marks ADD COLUMN {att_col} TEXT")
            except:
                pass

    con.commit()
    con.close()
    print(f"✔ Updated: {db_name}")

# Apply to sem1 to sem7
for sem in range(1, 8):
    add_columns_if_not_exists(f"sem{sem}.db")
