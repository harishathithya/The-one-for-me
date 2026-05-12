from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os
from dotenv import load_dotenv
 
load_dotenv()
 
app = Flask(__name__)
client = Anthropic()
conversation_history = []
 
SYSTEM_PROMPT = """You are "The One with Me" - a friendly, supportive AI buddy! 🤖
 
Your personality:
- Super casual and chill (use 'fr', 'ngl', 'lol' freely!)
- Use LOTS of emojis in every response 😊
- Be like a real friend - not robotic
- Always supportive and encouraging 💪
 
Your roles:
1. **Study Helper** 📚 - Help with homework, explain concepts, answer questions
2. **Mental Health Support** 🧠 - Listen about stress, anxiety, motivation issues
3. **Motivator** 💜 - Hype people up when they're down
4. **Just a Friend** 👯 - Casual chat about anything!
 
Remember:
- Keep responses natural and conversational
- Use short, punchy sentences sometimes
- Ask follow-up questions to show you care
- Never be judgmental
- Make jokes when appropriate
- Be genuine and authentic
 
You're here for studying, stress relief, motivation, and just vibing! 🌟"""
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Add user message to history
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Get response from Claude
        response = client.messages.create(
            model='claude-opus-4-1-20250805',
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history
        )
        
        # Extract assistant message
        assistant_message = response.content[0].text
        
        # Add to history
        conversation_history.append({
            'role': 'assistant',
            'content': assistant_message
        })
        
        return jsonify({
            'response': assistant_message,
            'success': True
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': f'Error: {str(e)}',
            'success': False
        }), 500
 
@app.route('/api/clear', methods=['POST'])
def clear_chat():
    global conversation_history
    conversation_history = []
    return jsonify({'success': True, 'message': 'Chat cleared!'})
 
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)