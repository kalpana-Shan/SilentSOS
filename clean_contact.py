import sqlite3

conn = sqlite3.connect(r'D:\Hackathons\silentsos-backend\silentsos.db')

# Delete all placeholder/wrong contacts
conn.execute("DELETE FROM trusted_contacts WHERE email IN ('youremail@gmail.com', 'your.real.email@gmail.com')")
conn.commit()
print("Deleted bad contacts:", conn.total_changes, "rows")

# Verify what's left
rows = conn.execute("SELECT id, name, email FROM trusted_contacts").fetchall()
print("Remaining contacts:")
for r in rows:
    print(f"  ID {r[0]}: {r[1]} → {r[2]}")

conn.close()