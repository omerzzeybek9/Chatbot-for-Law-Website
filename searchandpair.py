from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def find_relevant_content(query, contents):
    texts = [content['content'] for content in contents]
    vectorizer = TfidfVectorizer().fit(texts + [query])

    vectors = vectorizer.transform(texts + [query])
    query_vector = vectors[-1]
    content_vectors = vectors[:-1]

    cosine_similarities = cosine_similarity(query_vector, content_vectors)
    similar_content_index = cosine_similarities.argmax()

    return contents[similar_content_index]

