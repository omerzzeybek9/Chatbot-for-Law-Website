import sqlite3
from cgitb import text
import json
#Fetch data from Sqlite
def fetch_data():
    conn = sqlite3.connect("content.db")
    c = conn.cursor()
    c.execute("SELECT * FROM content")
    rows = c.fetchall()
    conn.close()
    return rows

data = fetch_data()


articles = []
for row in data:
    article = {
        "id": row[0],
        "url": row[1],
        "content":  json.loads(row[2])
    }
    articles.append(article)

paragraphs = []
for article in articles:
        content = " ".join(article["content"].get("p", []))
        paragraphs.append(content)

with open("dataset.jsonl", "w", encoding="utf-8") as f:
    for paragraph in paragraphs:
        f.write(json.dumps({"text": paragraph}, ensure_ascii=False) + '\n')