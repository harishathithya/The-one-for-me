from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Explicit API key setup
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

conversation_history = []

SYSTEM_PROMPT = """You are "The One with Me" - a friendly, supportive AI buddy! 🤖

Your personality:
- Super casual and chill
- Use emojis naturally 😊
- Be supportive and friendly
- Help with studies, motivation, and casual chats

Keep responses conversational and positive! 🌟
"""

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'No JSON data received'
            }), 400

        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'error': 'Empty message'
            }), 400

        conversation_history.append({
            'role': 'user',
            'content': user_message
        })

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history
        )

        assistant_message = response.content[0].text

        conversation_history.append({
            'role': 'assistant',
            'content': assistant_message
        })

        return jsonify({
            'response': assistant_message,
            'success': True
        })

    except Exception as e:
        print("FULL ERROR:", str(e))

        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/clear', methods=['POST'])
def clear_chat():
    global conversation_history
    conversation_history = []

    return jsonify({
        'success': True
    })


# IMPORTANT FOR VERCEL
app = app