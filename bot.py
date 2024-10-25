from flask import Flask, request, jsonify, send_from_directory, session
import google.generativeai as genai
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
app.permanent_session_lifetime = timedelta(minutes=30)  # Set session timeout

# Configure the Gemini API
# It's better to use environment variables for API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyANBvblyYIMf1ONtkzFYTRLiz5Zxg4k_8Y')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # Ensure session is permanent
        session.permanent = True
        
        # Retrieve conversation history from session
        conversation = session.get('conversation', [])
        
        # Add user message to conversation
        conversation.append({"role": "user", "parts": [user_message]})
        
        # Generate a response using the Gemini API with conversation history
        response = model.generate_content(conversation)
        
        # Add bot response to conversation
        conversation.append({"role": "model", "parts": [response.text]})
        
        # Limit conversation history to last 10 messages (5 exchanges)
        if len(conversation) > 10:
            conversation = conversation[-10:]
        
        # Store updated conversation in session
        session['conversation'] = conversation
        
        return jsonify({'response': response.text})
    except Exception as e:
        # Log the error (in a production environment, you'd want to use a proper logging system)
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/clear', methods=['POST'])
def clear_conversation():
    session.pop('conversation', None)
    return jsonify({'message': 'Conversation cleared'})

if __name__ == '__main__':
    app.run(debug=True)
