import requests
import bs4 as BeautifulSoup

def scrape_website():
    url = 'url'
    response = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(response.content, 'html.parser')

    links = [url + link.get('href') for link in soup.find_all('a',href=True)]

    contents = []

    for link in links:
        response = requests.get(link)
        page_soup = BeautifulSoup.BeautifulSoup(response.content, 'html.parser')

        title = page_soup.find_all('title').text if page_soup.find_all('title') else None
        content = page_soup.get_text()

        contents.append({'title': title, 'content': content, 'url': link})

    return contents

contents = scrape_website()

