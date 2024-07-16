import requests
from bs4 import BeautifulSoup
import json
import schedule
import time

def scrape_and_save():
    print("Scraping started...")
    url = "https://bilginhukuk.av.tr/"
    try:
        r = requests.get(url)
        r.raise_for_status()  #Checks HTTP errors
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return

    soup = BeautifulSoup(r.text, "lxml")

    a_tags = soup.find_all("a")

    hrefs = [a.get("href") for a in a_tags if a.get("href")]
    hrefs = list(set(hrefs))

    necessary_urls = [link for link in hrefs if "youtube" not in link and "category" not in link and link.startswith("http")]

    content = {}
    for link in necessary_urls:
        try:
            r2 = requests.get(link)
            r2.raise_for_status()  #Checks HTTP errors
            soup2 = BeautifulSoup(r2.text, "lxml")
            h2_texts = [h2.text.strip() for h2 in soup2.find_all("h2")]
            p_texts = [p.text.strip() for p in soup2.find_all("p")]
            content[link] = {"h2": h2_texts, "p": p_texts}
        except requests.RequestException as e:
            print(f"Error scraping {link}: {e}")

    #Save to JSON
    with open("content.json", "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

    print("Scraping completed and data saved.")

scrape_and_save()

#Schedule the scraping task (Works every day at 1 a.m.)
schedule.every().day.at("01:00").do(scrape_and_save)

while True:
    schedule.run_pending()
    time.sleep(1)