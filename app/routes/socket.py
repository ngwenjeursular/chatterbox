from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_login import current_user
from flask import url_for
from datetime import datetime

from app import create_app, socketio
from flask import request
import random


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
                          if current_user.profile_picture else url_for('static', filename='default.jpg')  # Use a default if no picture


    print(f"Message from {username}: {message}")

    # Send the message, username, and profile picture to all connected users in the room
    socketio.emit('receive_message', {
        'message': message,
        'username': username,
        'profilePicture': profile_picture_url,
        'time': data['time'] # added
    }, room=room)


room_users = {}


@socketio.on('join')
def on_join(data, sid=None):
    """
    Handles user joining a room.
    Initializes room if not present and adds user.
    Notifies all users of the join.
    """
    room = data['room']
    username = data.get('username')

    # Ensure the room is initialized as a set, not a dict
    if room not in room_users:
        room_users[room] = set()  # Initialize room_users[room] as a set

    is_new_join = username not in room_users[room]

    if is_new_join:  
        join_room(room)
        room_users[room].add(username)

        # Notify only the joining user with "You joined the room"
        emit('receive_message', {
            'type': 'system',
            'message': 'You joined the room',
            'is_self': True,
            'time': datetime.now().strftime('%H:%M')
        }, to=sid)

        # Notify other users in the room about the new user
        emit('receive_message', {
            'type': 'system',
            'message': f'{username} has entered the room.',
            'time': datetime.now().strftime('%H:%M')
        }, room=room, include_self=False)

    print(f'{username} has joined the room: {room}')


@socketio.on('leave')
def on_leave(data):
    """
    Manages user exit from a chat room.
    Removes user from the room, notifies others, deletes room if empty.
    """
    room = data['room']
    username = data.get('username')

    if room in room_users:
        if username in room_users[room]:
            leave_room(room)
            room_users[room].discard(username)  # Correctly using discard with set

            # Notify others in the room about the user's departure
            emit('receive_message', {
                'type': 'system',
                'message': f'{username} has left the room.',
                'time': datetime.now().strftime('%H:%M')
            }, room=room)

            # If no users remain in the room, delete the room
            if len(room_users[room]) == 0:
                del room_users[room]  # Delete room data from tracking
                print(f"Room '{room}' deleted from server as it has no more users.")

        print(f"{username} has left the room: {room}")

    else:
        print(f"Attempted to access non-existent room: {room}")


@socketio.on('connect')
def on_connect():
    print("Client connected")


