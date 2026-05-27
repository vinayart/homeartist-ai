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

    conn = sqlite3.connect("database.db")

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
# SINGLE BLOG PAGE
# ============================================

@app.route("/blog/<int:id>")
def blog(id):

    conn = get_db_connection()

    blog = conn.execute("""
    SELECT * FROM blogs
    WHERE id = ?
    """, (id,)).fetchone()

    conn.close()

    return render_template("blog.html", blog=blog)

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
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )