import sqlite3
from datetime import datetime

# ============================================
# DATABASE CONNECTION
# ============================================

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# ============================================
# GET ALL BLOG SLUGS
# ============================================

cursor.execute("""
SELECT slug FROM blogs
""")

blogs = cursor.fetchall()

# ============================================
# CREATE XML CONTENT
# ============================================

xml = """<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

# ============================================
# HOMEPAGE URL
# ============================================

today = datetime.now().strftime("%Y-%m-%d")

xml += f"""
<url>

    <loc>
    https://YOUR-RENDER-URL.onrender.com/
    </loc>

    <lastmod>{today}</lastmod>

    <changefreq>daily</changefreq>

    <priority>1.0</priority>

</url>
"""

# ============================================
# BLOG URLS
# ============================================

for blog in blogs:

    slug = blog[0]

    xml += f"""
<url>

    <loc>
    https://YOUR-RENDER-URL.onrender.com/blog/{slug}
    </loc>

    <lastmod>{today}</lastmod>

    <changefreq>daily</changefreq>

    <priority>0.8</priority>

</url>
"""

# ============================================
# CLOSE XML
# ============================================

xml += "\n</urlset>"

# ============================================
# SAVE SITEMAP
# ============================================

with open(
    "static/sitemap.xml",
    "w",
    encoding="utf-8"
) as file:

    file.write(xml)

print("sitemap.xml generated successfully")