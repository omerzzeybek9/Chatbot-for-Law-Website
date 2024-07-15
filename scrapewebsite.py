import requests
from bs4 import BeautifulSoup
import json

url = "url"

r = requests.get(url)

soup = BeautifulSoup(r.text, "lxml")

a_tags = soup.find_all("a")

hrefs = [a.get("href") for a in a_tags if a.get("href")]

hrefs = list(set(hrefs))

necessary_urls = [link for link in hrefs if "youtube" not in link and "category" not in link]

content = {}
for link in necessary_urls:
    r2 = requests.get(link)
    soup2 = BeautifulSoup(r2.text, "lxml")
    h2_texts = [h2.text.strip() for h2 in soup2.find_all("h2")]
    p_texts = [p.text.strip() for p in soup2.find_all("p")]
    content[link] = {"h2": h2_texts, "p": p_texts}

with open("content.json", "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=4)

print("Content stored in content.json")