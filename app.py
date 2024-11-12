
# import eventlet
# eventlet.monkey_patch()


from app import create_app, socketio
from flask_socketio import SocketIO, send, emit
from flask_socketio import SocketIO, join_room, leave_room
from flask import request
from datetime import datetime

from flask_login import current_user
from flask import url_for, session
import random
from app.models.messages import db,  Message
from app.models.room import Room  # Adjust this import path to match your project structure




app = create_app('development')
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    print('Client connected')  # This should print when the client connects

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')  # This should print when the client disconnects

# @socketio.on('send_message')
# def handle_message(data):
#     print('Message received:', data) # This will print the message data to the terminal
#     data['time'] = datetime.now().strftime('%H:%M')
#     # Emit the message to all clients in the room
#     socketio.emit('receive_message', data, room=data['room'])



@socketio.on('send_message')
def handle_send_message(data):
    """Handle message sent from client to broadcast to other users."""

    # Set username and retrieve profile picture based on authentication status
    if current_user.is_authenticated:
        username = current_user.nickname if current_user.nickname else current_user.username
        profile_picture_url = (
            url_for('static', filename=f'uploads/{current_user.profile_picture}')
            if current_user.profile_picture
            else 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))
        )
    else:
        username = session.get('guest_name', 'Guest')
        profile_picture_url = session.get('guest_profile_picture', 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000)))

    # Debugging print to verify message content and sender
    print(f"Message from {username}: {data['message']}")

    # Formatting the message details
    data['time'] = datetime.now().strftime('%H:%M')  # Format as HH:MM
    room = data['room']
    message = data['message']

    room_name = data['room']
    # # Get room_id and check if it’s in the data
    # room_id = data.get('room_id')
    # if not room_id:
    #     print("Error: room_id not found in data:", data)  # Debugging output
    #     return  # Early return to handle this case


    if not room:  # Check if room is not found (more concise)
        # Handle case where room doesn't exist
        print(f"Room '{room_name}' not found.")
    else:

        # ... rest of the code to create and save the message using room.id
        # Save message to the database
        new_message = Message(room=room, username=username, message=message, profile_picture=profile_picture_url)
        db.session.add(new_message)
        db.session.commit()

    # Emit the message to all users in the room
    socketio.emit('receive_message', {
        'message': message,
        'username': username,
        'profilePicture': profile_picture_url,
        'time': data['time']
    }, room=room)


from flask_login import current_user
from flask import url_for, session
from datetime import datetime
import random

# @socketio.on('send_message')
# def handle_send_message(data):
# 	"""Handle message sent from client to broadcast to other users."""
# 	# Set username and profile picture based on authentication status
# 	if current_user.is_authenticated:
# 		username = current_user.nickname if current_user.nickname else current_user.username
# 		profile_picture_url = (
# 			url_for('static', filename=f'uploads/{current_user.profile_picture}')
# 			if current_user.profile_picture else 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))
# 		)
# 	else:
# 		username = session.get('guest_name', 'Guest')
# 		profile_picture_url = 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))

# 	# Debugging print to verify message content and sender
# 	print(f"Message from {username}: {data['message']}")
	
# 	# Formatting the message details
# 	data['time'] = datetime.now().strftime('%H:%M')  # Format as HH:MM
# 	room = data['room']
# 	message = data['message']
	
# 	# Emit the message to all users in the room
# 	socketio.emit('receive_message', {
# 		'message': message,
# 		'username': username,
# 		'profilePicture': profile_picture_url,
# 		'time': data['time']
# 	}, room=room)




room_users = {}


# @socketio.on('join')
# def on_join(data, sid=None):
#     room = data['room']
#     username = data.get('username')
#     # added
#     sid = request.sid

#     # Initialize the room list if it doesn't exist
#     if room not in room_users:
#         #room_users[room] = set()
#         room_users[room] = {}
        

#     # Determine if the user is already in the room
#     is_new_join = username not in room_users[room]

#     if is_new_join:  # First time joining, show the "You joined the room" message to the user
#         join_room(room)
#         #room_users[room].add(username)
#         # added
#         room_users[room][username] = sid

#         # Notify only the joining user with "You joined the room"
#         emit('receive_message', {
#             'type': 'system',
#             'message': 'You joined the room',
#             'is_self': True,
#             'time': datetime.now().strftime('%H:%M')
#         }, to=sid)  # Use `sid` to send only to the joining user

#         # Notify other users in the room about the new user
#         emit('receive_message', {
#             'type': 'system',
#             'message': f'{username} has entered the room.',
#             'time': datetime.now().strftime('%H:%M')
#         }, room=room, include_self=False)  # Only others in the room see this message

#     print(f'{username} has joined the room: {room}')



# @socketio.on('leave')
# def on_leave(data):
#     """
#     Handles user leaving a chat room.
#     Removes user from room, broadcasts leave message, and deletes room if empty.
#     """

#     room = data['room']
#     username = data.get('username')
#     # Capture the session ID of the leaving user
#     # added
#     #sid = request.sid


#     if room in room_users and username in room_users[room]:
#         # added
#         #sid = room_users[room][username]  # Retrieve the stored sid

#         # Remove the user from the room and broadcast leave message
#         leave_room(room)
#         del room_users[room][username]

#         emit('receive_message', {
#             'type': 'system',
#             'message': f'{username} has left the room.',
#             'time': datetime.now().strftime('%H:%M')
#         }, room=room)

#         # Clean up the room if empty
#         if not room_users[room]:
#             del room_users[room]

#         # If room is empty after this user leaves, delete the room
#         if len(room_users[room]) == 0:
#             del room_users[room]  # Remove from server-side tracking
#             socketio.server.leave_room(request.sid, room)  # Leave room directly
#             print(f"Room '{room}' deleted from server as it has no more users.")

#     print(f'{username} has left the room: {room}')


@socketio.on('join')
def on_join(data, sid=None):
    """
    Handles user joining a room.
    Initializes room if not present and adds user.
    Notifies all users of the join.
    """
    room = data['room']
    username = data.get('username')

    # Check if the room exists in room_users before joining
    # added
    # if room not in room_users:
    #     print(f"Room '{room}' does not exist and won't be recreated on join.")
    #     emit('receive_message', {
    #         'type': 'system',
    #         'message': 'The room no longer exists. Please create a new room.',
    #         'is_self': True,
    #         'time': datetime.now().strftime('%H:%M')
    #     }, to=sid)
    #     return

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


# this leave function is not working
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


@socketio.on('disconnect')
def handle_disconnect():
    """
    Handles unexpected client disconnects.
    Removes the user from room data if applicable.
    """
    sid = request.sid
    for room, users in room_users.items():
        if sid in users:
            users.discard(sid)  # Remove the user based on session ID
            emit('receive_message', {
                'type': 'system',
                'message': f'A user has disconnected.',
                'time': datetime.now().strftime('%H:%M')
            }, room=room)
            if not users:
                del room_users[room]
                print(f"Room '{room}' deleted on disconnect.")
            break


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
