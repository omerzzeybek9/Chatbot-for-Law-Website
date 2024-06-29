from flask import Flask, request, jsonify
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup

openai.api_key = "openai-api-key"


def scrape_website():
    base_url = 'url'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = [base_url + link.get('href') for link in soup.find_all('a', href=True) if link.get('href').startswith('/')]

    contents = []

    for link in links:
        page_response = requests.get(link)
        page_soup = BeautifulSoup(page_response.content, 'html.parser')

        title = page_soup.find('title').text if page_soup.find('title') else 'No title'
        content = page_soup.get_text()

        contents.append({'title': title, 'content': content, 'url': link})

    return contents


def find_relevant_content(query, contents):
    texts = [content['content'] for content in contents]
    vectorizer = TfidfVectorizer().fit(texts + [query])

    vectors = vectorizer.transform(texts + [query])
    query_vector = vectors[-1]
    content_vectors = vectors[:-1]

    cosine_similarities = cosine_similarity(query_vector, content_vectors)
    similar_content_index = cosine_similarities.argmax()

    return contents[similar_content_index]


def generate_response(user_input, contents):
    relevant_content = find_relevant_content(user_input, contents)
    content = relevant_content['content']

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Using the following content, answer the question: {content}\n\nQuestion: {user_input}",
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    contents = scrape_website()
    response = generate_response(user_input, contents)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)