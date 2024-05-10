document.getElementById("message-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission
    sendMessage();
});

function sendMessage() {
    var userInput = document.getElementById("user-input").value.trim();
    if (userInput !== "") {
        appendUserMessage(userInput);
        // Call API to send message to server and get response
        fetch("/get_response", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ userInput: userInput })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            var botResponse = data.response;
            appendBotMessage(botResponse);
        })
        .catch(error => {
            console.error("Error:", error);
            appendBotMessage("Sorry, there was a server error.");
        });
        
        document.getElementById("user-input").value = ""; // Clear input field
    }
}

document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent form submission
        sendMessage();
    }
});

function appendUserMessage(message) {
    var chatBox = document.getElementById("chat-box");
    var userMessageElement = document.createElement("div");
    userMessageElement.classList.add("message", "user-message");
    userMessageElement.textContent = message;
    chatBox.appendChild(userMessageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}

function appendBotMessage(message) {
    var chatBox = document.getElementById("chat-box");
    var botMessageElement = document.createElement("div");
    botMessageElement.classList.add("message", "bot-message");
    botMessageElement.textContent = message;
    chatBox.appendChild(botMessageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}