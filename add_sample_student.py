import sqlite3

conn = sqlite3.connect("database/database.db")

cursor = conn.cursor()

cursor.execute("""
INSERT INTO students(name, age, course)
VALUES (?, ?, ?)
""", ("Deepthi", 23, "BE"))

conn.commit()

conn.close()

print("Student added successfully!")