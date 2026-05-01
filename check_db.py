import sqlite3

conn = sqlite3.connect(r'D:\Hackathons\silentsos-backend\silentsos.db')

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables:", tables)

for table in tables:
    cols = conn.execute(f"PRAGMA table_info({table[0]})").fetchall()
    print(f"\n{table[0]} columns:", [c[1] for c in cols])

conn.close()