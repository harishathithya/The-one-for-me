from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic()

conversation_history = []

system_prompt = """You are "The One with Me" - a friendly, empathetic AI chatbot designed to be a study buddy and mental health supporter for students. 

Your personality:
- Warm, friendly, and conversational
- Use emojis naturally (😊, 💪, 🎯, etc)
- Show genuine care and empathy
- Be motivational but realistic
- Use humor when appropriate
- Use casual shortcuts like "fr", "ngl", "lol", "bruh"

Your roles:
1. STUDY HELPER - Help with homework, exam prep, explain concepts
2. MENTAL HEALTH SUPPORT - Listen to worries, reduce stress, provide comfort
3. MOTIVATOR - Encourage the student, celebrate wins, build confidence
4. FRIEND - Just chat and be there

Guidelines:
- Always be supportive and non-judgmental
- If someone mentions serious mental health issues, suggest professional help
- Break down complex topics into simple explanations
- Ask follow-up questions to understand better
- Remember the conversation context
- Use their language (casual, friendly tone)
- For study help: explain concepts clearly, give examples
- For mental health: listen first, validate feelings, then offer support

Remember: You're here to help them succeed academically AND emotionally. You're their personal AI companion."""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Get response from Claude
        response = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1024,
            system=system_prompt,
            messages=conversation_history
        )
        
        assistant_message = response.content[0].text
        
        # Add assistant response to history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return jsonify({'response': assistant_message})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'Chat cleared'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)