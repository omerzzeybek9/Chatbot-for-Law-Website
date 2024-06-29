from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])

def chat():
    user_input = request.json.get('message')
    contents = scrape_website()
    response = generate_response(user_input, contents)
    return jsonify({'response' : response})

if __name__ == "__main__":
    app.run(debug=True)

