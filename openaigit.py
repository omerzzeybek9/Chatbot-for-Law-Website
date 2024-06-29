import openai

openai.api_key = "open-ai-key"

def generate_response(user_input, contents):
    relevant_content = find_relevant_content(user_input, contents)
    content = relevant_content['content']

    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = f"Using the following content, answer the question: {content}\n\nQuestion: {user_input}",
        max_tokens = 150,
        temperature = 0.7
    )

    return response.choices[0].text.strip()
