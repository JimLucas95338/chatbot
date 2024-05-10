# NLTK Chatbot

This repository contains a Flask-based chatbot that utilizes the Natural Language Toolkit (NLTK) for processing and responding to user queries. It can perform basic conversation and is designed to be a foundational platform for more complex chatbot features.

## Features

- Basic chatbot functionalities using pattern matching.
- Advanced Natural Language Processing (NLP) capabilities using spaCy for entity recognition and TextBlob for sentiment analysis.
- Preprocessing of user inputs to ensure effective pattern matching and NLP analysis.
- Utilizes NLTK's corpus, tokenization methods, and chat utilities.
- Flask-based web application to interact with the chatbot through a web interface.

## Prerequisites

Before you can run this chatbot, you need to have the following installed:
- Python 3.6 or higher
- Flask
- NLTK
- spaCy
- TextBlob

You can install the required libraries using the following command:
    pip install flask nltk spacy textblob
    python -m spacy download en_core_web_sm

## Installation

1. Clone this repository to your local machine using:
    git clone <https://github.com/JimLucas95338/chatbot>
2. Navigate to the cloned directory:
    cd chatbot
3. Install the required Python packages:
    pip install -r requirements.txt

## Usage

To start the server, run:
    python app.py
    Once the server is running, you can access the chatbot by navigating to `http://127.0.0.1:5000/` in your web browser.

## Customization

You can customize the chatbot responses by modifying the `pairs` list in `app.py`. Each pair consists of a regex pattern and a list of possible responses.

## Downloads

This application requires specific downloads which are handled by the script itself:

- **punkt**: This tokenizer divides a text into a list of sentences.
- **stopwords**: This helps in filtering out the unnecessary words during text processing.
- **en_core_web_sm**: spaCy's English model used for tasks like tokenization, part-of-speech tagging, and named entity recognition.


## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your enhancements.

## License

This project is open source and available under the [MIT License](LICENSE).
