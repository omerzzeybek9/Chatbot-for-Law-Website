import requests
from bs4 import BeautifulSoup
import json


def scrape_and_save():
    print("Scraping started...")
    url = "https://bilginhukuk.av.tr/"

    try:
        r = requests.get(url)
        r.raise_for_status()  # Checks HTTP errors
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return

    soup = BeautifulSoup(r.text, "lxml")
    a_tags = soup.find_all("a")

    hrefs = [a.get("href") for a in a_tags if a.get("href")]
    hrefs = list(set(hrefs))  #Remove duplicates

    # Filter URLs based on categories and external links
    urls = [link for link in hrefs if "category" in link]

    all_urls = set(urls)  #Use set to avoid duplicates
    for link in urls:
        try:
            r2 = requests.get(link)
            r2.raise_for_status()  # Checks HTTP errors
            soup2 = BeautifulSoup(r2.text, "lxml")
            a_tags2 = soup2.find_all("a")
            refs = [a.get("href") for a in a_tags2 if a.get("href")]
            all_urls.update(refs)  # Add new URLs
        except requests.RequestException as e:
            print(f"Error scraping {link}: {e}")

    all_urls = list(all_urls)
    necessary_urls = [link for link in all_urls if "category" not in link and not any(
        ext in link for ext in ["facebook", "youtube", "linkedin", "author", "twitter", "instagram"])]

    content = []
    for link in necessary_urls:
        try:
            r2 = requests.get(link)
            r2.raise_for_status()
            soup2 = BeautifulSoup(r2.text, "lxml")
            paragraphs = soup2.find_all("p")
            headers = soup2.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])  #Include all header tags

            page_content = {
                "url": link,
                "text": [p.get_text(strip=True) for p in paragraphs] + [header.get_text(strip=True) for header in
                                                                        headers]
            }
            content.append(page_content)
        except requests.RequestException as e:
            print(f"Error scraping {link}: {e}")

    with open('data.jsonl', 'w', encoding='utf-8') as f:
        for entry in content:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')

    print("Scraping finished and data saved.")


scrape_and_save()
