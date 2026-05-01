import sqlite3

conn = sqlite3.connect(r'D:\Hackathons\silentsos-backend\silentsos.db')

# Change this to your real email
new_email = "silentsos.alert@gmail.com"

conn.execute("UPDATE contacts SET email=? WHERE user_id='test123'", (new_email,))
conn.commit()
print("Updated:", conn.total_changes, "rows")

# Verify
rows = conn.execute("SELECT * FROM contacts WHERE user_id='test123'").fetchall()
print("Contacts:", rows)
conn.close()