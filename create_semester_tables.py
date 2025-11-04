import sqlite3

def create_table(sem_number):
    db_name = f'sem{sem_number}.db'
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            username TEXT PRIMARY KEY,

            sub1_ia1 TEXT, sub1_ia2 TEXT, sub1_ia3 TEXT,
            sub1_att_held TEXT, sub1_att_attended TEXT,

            sub2_ia1 TEXT, sub2_ia2 TEXT, sub2_ia3 TEXT,
            sub2_att_held TEXT, sub2_att_attended TEXT,

            sub3_ia1 TEXT, sub3_ia2 TEXT, sub3_ia3 TEXT,
            sub3_att_held TEXT, sub3_att_attended TEXT,

            sub4_ia1 TEXT, sub4_ia2 TEXT, sub4_ia3 TEXT,
            sub4_att_held TEXT, sub4_att_attended TEXT,

            sub5_ia1 TEXT, sub5_ia2 TEXT, sub5_ia3 TEXT,
            sub5_att_held TEXT, sub5_att_attended TEXT,

            sub6_ia1 TEXT, sub6_ia2 TEXT, sub6_ia3 TEXT,
            sub6_att_held TEXT, sub6_att_attended TEXT
        )
    """)

    con.commit()
    con.close()
    print(f"✔ Created table in {db_name}")

# Loop through sem1.db to sem7.db
for i in range(1, 8):
    create_table(i)
