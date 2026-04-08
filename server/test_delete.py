import sqlite3
import os

db_path = 'data.db'
if not os.path.exists(db_path):
    print(f'DB not found at {os.path.abspath(db_path)}')
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 1. Check & Delete collected data
    c.execute("select id from collected_data where title like '%Example Domain%' or source_url like '%example.com%'")
    data_ids = [r[0] for r in c.fetchall()]
    if data_ids:
        print(f"Deleting collected_data {data_ids}")
        c.execute(f"delete from collected_data where id in ({','.join(map(str, data_ids))})")
    
    # 2. Check & Delete tasks
    c.execute("select id from tasks where name like '%Example Domain%' or start_url like '%example.com%'")
    task_ids = [r[0] for r in c.fetchall()]
    if task_ids:
        print(f"Deleting tasks {task_ids}")
        c.execute(f"delete from tasks where id in ({','.join(map(str, task_ids))})")
    
    conn.commit()
    print("Done")
except Exception as e:
    print(e)
