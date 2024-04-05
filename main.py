import nltk
import random
import re
from flask import Flask, request, jsonify, render_template
from nltk.chat.util import reflections
from nltk.chat.util import Chat
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Define pairs of patterns and responses
pairs = [
    [r"my name is (.*)", ["Hello %1, how can I assist you today?"]],
    [r"what is your name\\?", ["You can call me Chatbot. How can I help you?"]],
    [r"how are you\\?", ["I'm doing well, thank you!", "I am good."]],
    [r"quit", ["Bye! Take care.", "Goodbye, have a great day!"]],
    [r"hello", ["Hello, how can I assist you today?"]],
    [r"what can you do\\?", ["I can assist you with various tasks. Feel free to ask me anything!"]],
    [r"test2", ["Test completed successfully"]],
    [r"test", ["Second Test completed successfully"]],
]

app = Flask(__name__)

class CustomChat(Chat):
    def respond(self, str):
        for pattern, responses in self._pairs:
            match = pattern.match(str)
            if match:
                response = random.choice(responses)
                if "%1" in response:
                    return response.replace("%1", match.group(1))
                else:
                    return response
        return None  # Return None when there is no matching pattern

# Create a Chat object
chatbot = CustomChat(pairs, reflections)

# Preprocess input text using NLP
def preprocess_input(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove punctuation and convert to lowercase
    tokens = [word.lower() for word in tokens if word.isalnum()]
    # Join tokens into a single string
    text = " ".join(tokens)
    # Replace "\\?" with "?" to handle the question mark properly
    text = text.replace("\\?", "?")
    return text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("userInput", "")
    preprocessed_input = preprocess_input(user_input)
    response = chatbot.respond(preprocessed_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
