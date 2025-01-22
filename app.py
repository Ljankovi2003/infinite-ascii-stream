from flask import Flask, jsonify
from flask_cors import CORS
from telethon import TelegramClient, sync
from telethon.tl.types import PeerChannel
import asyncio
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Telegram API credentials
API_ID = '20418380'
API_HASH = '88928238a385ae34bf1fb8165af0773e'


# Initialize the client
client = TelegramClient('session_name', API_ID, API_HASH)

# Channel usernames or IDs to monitor
CHANNELS = [
    '@gmgnsignals',
    '@PumpLiveKOTH',
    'channel_username_3'
]

def format_message(message):
    """Format a Telegram message for JSON response"""
    return {
        'id': message.id,
        'channel': message.chat.username or message.chat.title,
        'date': message.date.isoformat(),
        'text': message.text if message.text else '[Media Message]',
        'has_media': bool(message.media),
        'views': getattr(message, 'views', 0),
        'forwards': getattr(message, 'forwards', 0)
    }

async def get_channel_messages():
    """Retrieve messages from multiple channels"""
    messages = []
    
    try:
        # Connect if not already connected
        if not client.is_connected():
            await client.connect()
            

        # Fetch messages from each channel
        for channel in CHANNELS:
            try:
                entity = await client.get_entity(channel)
                channel_messages = await client.get_messages(entity, limit=10)
                messages.extend([format_message(msg) for msg in channel_messages])
            except Exception as e:
                print(f"Error fetching messages from {channel}: {str(e)}")
                continue

        # Sort all messages by date
        messages.sort(key=lambda x: x['date'], reverse=True)
        
    except Exception as e:
        print(f"Error in get_channel_messages: {str(e)}")
        raise

    return messages

@app.route('/api/messages', methods=['GET'])
async def get_messages():
    try:
        messages = await get_channel_messages()
        return jsonify({
            'status': 'success',
            'message_count': len(messages),
            'messages': messages
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/functions', methods=['GET'])
def get_functions():
    functions = [
        "function example1() { console.log('Example 1'); }",
        "function example2() { console.log('Example 2'); }",
        "function example3() { console.log('Example 3'); }"
    ]
    return jsonify(functions)

if __name__ == '__main__':
    # Start the Telegram client
    client.start()
    
    # Run Flask app with async support
    app.run(debug=True)