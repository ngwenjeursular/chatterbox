from flask import Blueprint, render_template
from app import  socketio


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('base.html')


# A SocketIO event for messages
@socketio.on('message')
def handle_message(msg):
    # Broadcast the message to all connected clients
    socketio.send(msg, broadcast=True)