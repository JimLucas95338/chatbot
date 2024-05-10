import nltk
import random
import re
import spacy
from flask import Flask, request, jsonify, render_template, session
from nltk.chat.util import reflections, Chat
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Flask and session config
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Define pairs of patterns and responses
pairs = [
    # Your existing pairs here...
]

class CustomChat(Chat):
    def respond(self, text):
        # Retrieve context from session
        context = session.get('context', [])
        
        # Add the new user input to context
        context.append('User: ' + text)
        session['context'] = context
        
        # Process the text through patterns
        for pattern, responses in self._pairs:
            match = pattern.match(text)
            if match:
                response = random.choice(responses)
                if "%1" in response:
                    response = response.replace("%1", match.group(1))
                context.append('Bot: ' + response)  # Add bot response to context
                session['context'] = context
                return response
        return None

# Preprocess input text using NLP
def preprocess_input(text):
    # Tokenize and clean text
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalnum()]
    
    # Analyze text with spaCy for NER and sentiment
    doc = nlp(' '.join(tokens))
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    sentiment = doc._.polarity_scores if hasattr(doc._, 'polarity_scores') else {}

    # Logging for debugging
    print(f"Entities recognized: {entities}")
    print(f"Sentiment analysis: {sentiment}")
    
    return " ".join(tokens)

@app.route("/")
def index():
    session['context'] = []  # Initialize a new conversation context
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("userInput", "")
    preprocessed_input = preprocess_input(user_input)
    response = chatbot.respond(preprocessed_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
