# =====================================================
# HOMEARTIST.ONLINE AI BLOG GENERATOR
# FULL PROFESSIONAL VERSION
# =====================================================

import requests
import feedparser
import sqlite3
import re
from datetime import datetime

# =====================================================
# DATABASE SETUP
# =====================================================

conn = sqlite3.connect("homeartist.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT,

    meta_description TEXT,

    content TEXT,

    created_at TEXT
)
""")

conn.commit()

# =====================================================
# GOOGLE TRENDS RSS
# =====================================================

url = "https://trends.google.com/trending/rss?geo=IN"

feed = feedparser.parse(url)

# =====================================================
# TREND CONVERTER
# =====================================================

def convert_trend(trend):

    trend_lower = trend.lower()

    # =====================================================
    # SPORTS
    # =====================================================

    if any(word in trend_lower for word in [
        "ipl", "cricket", "virat",
        "dhoni", "football", "match"
    ]):

        return {
            "topic": f"Cricket Inspired Custom Art & Mobile Cover Ideas Based on {trend}",
            "keywords": [
                "cricket art",
                "sports mobile cover",
                "custom player sketch",
                "IPL artwork",
                "sports wall art"
            ]
        }

    # =====================================================
    # MOVIES / CELEBRITIES
    # =====================================================

    elif any(word in trend_lower for word in [
        "movie", "film", "actor",
        "actress", "srk", "salman",
        "pushpa", "bollywood"
    ]):

        return {
            "topic": f"Celebrity Inspired Couple Art & Sketch Ideas from {trend}",
            "keywords": [
                "celebrity sketch",
                "movie style portrait",
                "cinematic couple art",
                "customized artwork"
            ]
        }

    # =====================================================
    # FESTIVALS
    # =====================================================

    elif any(word in trend_lower for word in [
        "diwali", "holi", "eid",
        "christmas", "festival"
    ]):

        return {
            "topic": f"Festival Inspired Handmade Art & Gift Ideas for {trend}",
            "keywords": [
                "festival art",
                "customized gifts",
                "festival portrait",
                "aesthetic handmade art"
            ]
        }

    # =====================================================
    # ANIME
    # =====================================================

    elif any(word in trend_lower for word in [
        "anime", "naruto",
        "pokemon", "doraemon"
    ]):

        return {
            "topic": f"Anime Style Mobile Cover & Portrait Art Inspired by {trend}",
            "keywords": [
                "anime mobile cover",
                "anime sketch",
                "anime couple art",
                "anime customized gifts"
            ]
        }

    # =====================================================
    # DEFAULT
    # =====================================================

    else:

        return {
            "topic": f"Trending Customized Art & Sketch Ideas Inspired by {trend}",
            "keywords": [
                "customized art",
                "mobile cover design",
                "couple portrait",
                "handmade sketch",
                "wall art"
            ]
        }

# =====================================================
# CLEAN AI OUTPUT
# =====================================================

def clean_text(text):

    text = re.sub(r"\*", "", text)

    text = re.sub(r"\#", "", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

# =====================================================
# GENERATE BLOG USING OLLAMA
# =====================================================

def generate_blog(prompt):

    response = requests.post(
        "http://127.0.0.1:11436/api/generate",
        json={

            "model": "gemma:2b",

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": 0.8,

                "num_predict": 900,

                "top_k": 40,

                "top_p": 0.9
            }
        }
    )

    if response.status_code != 200:

        print("❌ Error:", response.text)

        return None

    data = response.json()

    return clean_text(data["response"])

# =====================================================
# MAIN LOOP
# =====================================================

for entry in feed.entries[:5]:

    original_trend = entry.title

    converted = convert_trend(original_trend)

    topic = converted["topic"]

    keywords = ", ".join(converted["keywords"])

    print(f"\n🚀 Generating Blog For: {topic}")

    # =====================================================
    # MASTER AI PROMPT
    # =====================================================

    prompt = f"""
You are an elite SEO writer and branding expert for HomeArtist.online.

About Brand:
HomeArtist.online creates:

- Mobile Cover Art
- Couple Portrait Art
- Pencil Sketches
- Anime Art
- Handmade Drawings
- Customized Gifts
- Family Portraits
- Wall Art
- Aesthetic Digital Paintings

Current Topic:
{topic}

SEO Keywords:
{keywords}

TASK:
Write a HIGH QUALITY SEO optimized article.

RULES:
- Make article emotional and artistic
- Human readable
- Modern tone
- SEO optimized
- Use simple English
- Add emotional customer connection
- Mention customized and handmade feeling
- Make content attractive for Instagram users

INCLUDE:

1. SEO Friendly Title
2. Meta Description
3. Introduction
4. Mobile Cover Art Ideas
5. Couple Portrait Ideas
6. Handmade Sketch Ideas
7. Trending Aesthetic Styles
8. Instagram Reel Ideas
9. Why Customized Art Makes Better Gifts
10. Why Choose HomeArtist.online
11. Conclusion
12. 5 FAQs

ARTICLE LENGTH:
700 to 1200 words

STYLE:
Premium, modern, emotional, aesthetic.
"""

    # =====================================================
    # GENERATE CONTENT
    # =====================================================

    blog_content = generate_blog(prompt)

    if blog_content is None:
        continue

    # =====================================================
    # EXTRACT TITLE
    # =====================================================

    lines = blog_content.split("\n")

    title = lines[0][:150]

    meta_description = (
        f"Explore customized art ideas, couple portraits, "
        f"mobile cover art, and handmade sketches inspired by {original_trend}."
    )

    # =====================================================
    # SAVE TO DATABASE
    # =====================================================

    cursor.execute("""
    INSERT INTO blogs(
        title,
        meta_description,
        content,
        created_at
    )
    VALUES (?, ?, ?, ?)
    """, (

        title,

        meta_description,

        blog_content,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    print("✅ Blog Saved Successfully")

# =====================================================
# CLOSE DATABASE
# =====================================================

conn.close()

print("\n🎨 All HomeArtist Blogs Generated Successfully")