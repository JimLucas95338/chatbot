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
    [r"help me with (.*)", ["Sure, I can help you with %1. What exactly do you need?"]],
    [r"I need (.*)", ["I see, you need %1. How may I assist you with that?"]],
    [r"do you know about (.*)\\?", ["Yes, I know a few things about %1. What specific information are you looking for?"]],
    [r"tell me more about (.*)", ["What would you like to know about %1?"]],
    [r"I am feeling (.*)", ["I'm here to help. What's making you feel %1?"]],
    [r"what time is it\\?", ["I don't have real-time capabilities, but you should check your device's clock."]],
    [r"can you help with (.*)\\?", ["Sure, I can certainly try to help with %1. What do you need assistance with?"]],
    [r"where is (.*) located\\?", ["%1 is located at... Oops, I currently don't have access to location services."]],
    [r"do you speak (.*)\\?", ["I am designed primarily for English, but I can understand basic phrases in %1."]],
    [r"how do I fix (.*)", ["Fixing %1 can vary greatly. Could you provide more details about the problem?"]],
    [r"can I ask you a personal question\\?", ["Feel free to ask me anything. I'll do my best to respond appropriately."]],
    [r"thank you", ["You're welcome!", "No problem at all!"]],
    [r"you are (.*)", ["Thank you! Sometimes, I'm not sure how to respond to compliments.", "I'm just a program, but thank you for thinking I'm %1!"]],
    [r"joke", ["Why don't scientists trust atoms? Because they make up everything!", "What do you call a fake noodle? An Impasta!"]],
    [r"calculate (.*)", ["I can help with math. Please provide a clear mathematical expression."]],
    [r"what is the meaning of life\\?", ["That's a deep question. Some say it's 42, others might say it's about finding your own path."]],
    [r"how do I make (.*)", ["Making %1 can be quite interesting. Here are the steps generally involved: (provide general steps)"]],
    [r"what should I eat for (.*)", ["For %1, I recommend trying something nutritious and delicious. How about some pasta or a salad?"]],
    [r"who are you\\?", ["I'm an AI chatbot created to assist you with any questions or tasks you might have."]],
    [r"I love (.*)", ["%1 is really interesting. What do you like most about it?"]],
    [r"do you love me\\?", ["What is love baby don't hurt me"]],
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
