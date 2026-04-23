import sqlite3

conn = sqlite3.connect("predictions.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE predictions ADD COLUMN name TEXT")

conn.commit()
conn.close()

print("name column added successfully")