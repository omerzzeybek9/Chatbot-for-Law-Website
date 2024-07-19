import sqlite3
from cgitb import text

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

genai.configure(api_key=api_key)

size = 20000  #20,000 byte

def chunk_size(articles):
    parts = []
    for article in articles:
        content = " ".join(article["content"].get("p", []))
        content_bytes = content.encode('utf-8')
        content_decode = content_bytes.decode('utf-8')
        content_size = len(content_decode)
        offset = 0
        while offset < content_size:
            end_offset = min(offset + size, content_size)
            chunk = content_decode[offset:end_offset]
            parts.append(chunk)
            offset = end_offset
    return parts

parts = chunk_size(articles)

def chatbot(parts):
    i = parts[1]
    prompt = f"While answering the questions use this data {i}. Give contact details when they ask for help. Don't give long answers, speak Turkish"
    chat_response = genai.chat(prompt=prompt)

    print("Chatbot:", chat_response)

chatbot(parts)
def chat_with_bot(message):
  try:
    response = genai.chat(prompt=message)
    # Check for existence of "candidates" attribute
    if not hasattr(response, "candidates") or not response.candidates:
      return "Sorry, I couldn't understand your request."
    #Access content of the first candidate (assuming it exists)
    reply = response.candidates[0].content
    return reply
  except Exception as e:
    print(f"An error occurred: {e}")
    return "An error occurred. Please try again later."

user_message = "Hisseli taşınmazlardaki ilişkiler sonlandırıldı mı?"
bot_reply = chat_with_bot(user_message)
if bot_reply:
    print(f"Bot: {bot_reply}")
