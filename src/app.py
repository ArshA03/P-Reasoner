from flask import Flask, render_template, request, jsonify
from backend.chatbot import Chatbot
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
socketio = SocketIO(app)
chatbot = Chatbot()

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    user_message = data['message']
    response = chatbot.process_input(user_message)
    emit('receive_message', {
        'message': response,
        'sender': 'bot'
    })

@socketio.on('toggle_reasoning')
def handle_toggle():
    is_enabled = chatbot.toggle_reasoning()
    emit('reasoning_toggled', {
        'enabled': is_enabled
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)
