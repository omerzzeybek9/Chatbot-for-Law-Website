import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import requests
import google.generativeai as genai

api_key = "api-key"

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


