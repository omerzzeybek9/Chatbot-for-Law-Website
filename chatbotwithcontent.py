import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import openai

api_key = "api_key"

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


#Can't use api right now because of billing :(
def train_chatbot(api_key, articles):
    
    openai.api_key = api_key

    train_data = []
    for article in articles:
        content = article["content"]["p"]
        train_data.append({"text": content})
        
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-instruct",
        messages=train_data,
        prompt = "You're an AI assistant at the Scholar Law Firm named Bilgin Hukuk. I have taught you the data on this site, use this data to give short and concise answers to people. When they ask for help, tell them to contact you with your contact details. Speak Turkish"
    )

    reply = response["choices"][0].message.content
    print(f"Bilgin AI: {reply}")

train_chatbot(api_key, articles)