# ============================================
# FILE: app.py
# COMPLETE HOMEARTIST FLASK APP
# ============================================

from flask import Flask, render_template
import sqlite3
from flask import send_from_directory

app = Flask(__name__)

# ============================================
# DATABASE FUNCTION
# ============================================

def get_db_connection():

    conn = sqlite3.connect("homeartist.db")

    conn.row_factory = sqlite3.Row

    return conn

# ============================================
# HOME PAGE
# ============================================

@app.route("/")
def home():

    conn = get_db_connection()

    blogs = conn.execute("""
    SELECT * FROM blogs
    ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template("index.html", blogs=blogs)

# ============================================
# SINGLE BLOG PAGE USING SEO SLUG
# ============================================

@app.route("/blog/<slug>")
def blog(slug):

    conn = get_db_connection()

    blog = conn.execute("""
    SELECT * FROM blogs
    WHERE slug = ?
    """, (slug,)).fetchone()

    conn.close()

    return render_template(
        "blog.html",
        blog=blog
    )

# ============================================
# START FLASK
# ============================================
@app.route("/sitemap.xml")
def sitemap():

    return send_from_directory(
        "static",
        "sitemap.xml"
    )
    
@app.route("/robots.txt")
def robots():

    return send_from_directory(
        "static",
        "robots.txt"
    )
from flask import jsonify

@app.route("/api/blogs")
def api_blogs():

    conn = get_db_connection()

    blogs = conn.execute("""
    SELECT title, slug, meta_description
    FROM blogs
    ORDER BY id DESC
    LIMIT 20
    """).fetchall()

    conn.close()

    return jsonify([
        {
            "title": blog["title"],
            "slug": blog["slug"],
            "description": blog["meta_description"]
        }
        for blog in blogs
    ])
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8086,
        debug=False
    )