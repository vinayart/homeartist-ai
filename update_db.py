import sqlite3

# CONNECT DATABASE
conn = sqlite3.connect("homeartist.db")

cursor = conn.cursor()

# ADD slug COLUMN
cursor.execute("""
ALTER TABLE blogs
ADD COLUMN slug TEXT
""")

conn.commit()

print("slug column added successfully")

conn.close()