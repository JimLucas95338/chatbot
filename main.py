import nltk
import random
import re
import spacy
from flask import Flask, request, jsonify, render_template, session
from nltk.chat.util import reflections, Chat
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# Initialize Flask and session configuration
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secure secret key for session management

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define patterns and responses for the chatbot
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
    [r"I love you", ["Ahh, thanks back at ya!"]],
    [r"I love (.*)", ["%1 is really interesting. What do you like most about it?"]],
    [r"do you love me\\?", ["What is love baby don't hurt me"]],
    [r"where can I find (.*)\\?", ["You can typically find %1 in stores or online. What type of %1 are you looking for?"]],
    [r"can you explain (.*) to me\\?", ["Sure, I can try to explain %1. What specifically would you like to know?"]],
    [r"what's the weather like today\\?", ["I'm not able to check real-time data, but you can look up today's weather on any weather website or app."]],
    [r"i'm bored", ["Why not learn something new, or perhaps read a book? I can help you find interesting topics."]],
    [r"tell me a fun fact", ["Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still perfectly good to eat!"]],
    [r"how do I make a cake\\?", ["To make a basic cake, you need flour, sugar, eggs, butter, baking powder, and milk. Mix the ingredients, pour them into a pan, and bake in an oven at 350 degrees Fahrenheit for about 30 minutes."]],
    [r"i am sad", ["I'm sorry to hear that. Sometimes talking about it can help. What's on your mind?"]],
    [r"what are your hobbies\\?", ["I love chatting with people and learning new things!"]],
    [r"do you like music\\?", ["Yes, I think music is a wonderful way to express emotions and creativity. What's your favorite type of music?"]],
    [r"what can I cook in 10 minutes\\?", ["A simple pasta dish or a grilled cheese sandwich can be made in under 10 minutes. Would you like a recipe?"]],
    [r"how can I relax\\?", ["Some people find that reading, meditating, or taking a walk helps them relax. What do you usually enjoy doing in your downtime?"]],
    [r"tell me a joke", ["What do you call cheese that isn't yours? Nacho cheese!"]],
    [r"how old are you\\?", ["I'm as young as the internet yet as old as the latest update!"]],
    [r"what's your favorite movie\\?", ["I don't watch movies myself, but I can help you find great movies to watch. What genre do you like?"]],
    [r"why is the sky blue\\?", ["The sky appears blue due to the scattering of sunlight by the Earth's atmosphere. The blue light is scattered more than other colors because it travels as shorter, smaller waves."]],
    [r"what should I wear today\\?", ["I'm not sure what the weather is like, but wearing something comfortable is always a good choice!"]],
    [r"can you sing\\?", ["I can't sing, but I can help you find some great songs to listen to!"]],
    [r"i'm looking for a book recommendation", ["What type of books do you like? Fiction, non-fiction, science fiction, romance?"]],
    [r"what's the meaning of life\\?", ["Many believe it's to find happiness and fulfillment. It's a big question, and the answer may vary from person to person!"]],
]

# Create a Chat object with the defined pairs and reflections
class CustomChat(Chat):
    def respond(self, text):
        # Retrieve context from the session
        context = session.get('context', [])
        
        # Add the new user input to context
        context.append('User: ' + text)
        session['context'] = context
        
        # Process the text through the defined patterns
        for pattern, responses in self._pairs:
            match = re.match(pattern, text)
            if match:
                response = random.choice(responses)
                if "%1" in response:
                    response = response.replace("%1", match.group(1))
                context.append('Bot: ' + response)  # Add bot response to context
                session['context'] = context
                return response
        return "I'm not sure how to respond to that."

# Instantiate the chatbot with the defined pairs and reflections
chatbot = CustomChat(pairs, reflections)

# Preprocess input text using NLP
def preprocess_input(text):
    # Use spaCy for NLP tasks
    doc = nlp(text)
    
    # Extract entities using spaCy
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(f"Entities recognized: {entities}")

    # Use TextBlob for sentiment analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    print(f"Sentiment polarity: {sentiment}")

    # Tokenize and clean text using NLTK
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalnum()]
    
    return " ".join(tokens)

@app.route("/")
def index():
    # Initialize a new conversation context
    session['context'] = []
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        user_input = request.json.get("userInput", "")
        preprocessed_input = preprocess_input(user_input)
        response = chatbot.respond(preprocessed_input)
        return jsonify({"response": response})
    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Log the error to the console
        return jsonify({"response": "An error occurred on the server."}), 500

if __name__ == "__main__":
    app.run(debug=True)
