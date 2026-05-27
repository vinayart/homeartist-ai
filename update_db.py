import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# ADD slug COLUMN
cursor.execute("""
ALTER TABLE blogs
ADD COLUMN slug TEXT
""")

conn.commit()

print("Slug column added successfully")

conn.close()