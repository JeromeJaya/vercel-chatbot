const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

// Replace with your actual Gemini API key
const API_KEY = 'YOUR_GEMINI_API_KEY'; // Replace with your key
const API_URL = 'https://api.gemini.com/v1/chat'; // Adjust based on the Gemini API docs

sendButton.addEventListener('click', async () => {
    const message = userInput.value;
    if (!message) return;

    // Display user message
    appendMessage(`You: ${message}`);

    // Send message to the Gemini API
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        appendMessage(`Bot: ${data.reply}`); // Adjust based on the API response structure
    } catch (error) {
        appendMessage('Bot: Sorry, there was an error.');
        console.error(error);
    }

    // Clear input
    userInput.value = '';
});

function appendMessage(message) {
    const msgDiv = document.createElement('div');
    msgDiv.textContent = message;
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom
}
