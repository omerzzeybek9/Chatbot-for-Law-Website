import sqlite3
import json

#Read data from JSON file and save it to Sqlite
def save_to_sqlite3():
    with open("content.json", "r", encoding="utf-8") as f:
        content = json.load(f)

    conn = sqlite3.connect("content.db")
    conn.execute('PRAGMA foreign_keys = ON')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE,
            content TEXT
        )
    ''')
    for link, text in content.items():
        content_json = json.dumps(text, ensure_ascii=False)
        try:
            conn.execute("INSERT INTO content (link, content) VALUES (?, ?)", (link, content_json))
        except sqlite3.IntegrityError:
            print(f"Link already exists: {link}")

    conn.commit()
    conn.close()

    print("Data saved to database.")

save_to_sqlite3()