import sqlite3

conn = sqlite3.connect(r'D:\Hackathons\silentsos-backend\silentsos.db')

# Change this to the real recipient email
email = "kalpanashanmugam721@gmail.com"

conn.execute(
    "INSERT INTO trusted_contacts (name, relation, phone, email) VALUES (?, ?, ?, ?)",
    ("Amma", "mother", "9999999999", email)
)
conn.commit()
print("Contact added!")

rows = conn.execute("SELECT * FROM trusted_contacts").fetchall()
print("All contacts:", rows)
conn.close()