import sqlite3


conn = sqlite3.connect("database/database.db")

cursor = conn.cursor()


cursor.execute(
    """
    INSERT INTO users(username, password)
    VALUES(?, ?)
    """,
    ("admin", "admin123")
)


conn.commit()

conn.close()


print("Admin user created successfully!")