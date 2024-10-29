from flask_socketio import SocketIO, send, join_room, leave_room
from flask_login import current_user
from flask import url_for
from datetime import datetime


socketio = SocketIO()

@socketio.on('send_message')
def handle_send_message(data):
    """Handle message sent from client to broadcast to other users."""
    print(f"Message from {current_user.nickname}: {data['message']}")
    data['time'] = datetime.now().strftime('%H:%M')  # Format as HH:MM
    message = data['message']
    room = data['room']
    username = current_user.nickname
    #profile_picture = current_user.profile_picture or 'default_picture.jpg'  # Fallback to default if no picture
    # Construct the profile picture URL
    profile_picture_url = url_for('static', filename=f'uploads/{current_user.profile_picture}') \
                          if current_user.profile_picture else url_for('static', filename='8ec02100c2a966b6.jpg')  # Use a default if no picture


    print(f"Message from {username}: {message}")

    # Send the message, username, and profile picture to all connected users in the room
    socketio.emit('receive_message', {
        'message': message,
        'username': username,
        'profilePicture': profile_picture_url,
        #'profile_picture': profile_picture
    }, room=room)

@socketio.on('connect')
def on_connect():
    print("Client connected")


