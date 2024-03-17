import sqlite3
print(sqlite3.version)
print(sqlite3.sqlite_version)
conn = sqlite3.connect("fresher.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM stats")
rows = cursor.fetchall()

for row in rows:
    print(row)