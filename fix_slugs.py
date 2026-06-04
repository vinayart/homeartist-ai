import sqlite3

# ============================================
# CREATE SLUG FUNCTION
# ============================================

def create_slug(text):

    slug = text.lower()

    slug = slug.replace(" ", "-")

    slug = slug.replace(":", "")

    slug = slug.replace(",", "")

    slug = slug.replace(".", "")

    return slug

# ============================================
# DATABASE
# ============================================

conn = sqlite3.connect("homeartist.db")

cursor = conn.cursor()

# GET ALL BLOGS

cursor.execute("""
SELECT id, title FROM blogs
""")

blogs = cursor.fetchall()

# ============================================
# UPDATE SLUGS
# ============================================

for blog in blogs:

    blog_id = blog[0]

    title = blog[1]

    slug = create_slug(title)

    cursor.execute("""
    UPDATE blogs
    SET slug = ?
    WHERE id = ?
    """, (slug, blog_id))

conn.commit()

print("All slugs fixed successfully")

conn.close()