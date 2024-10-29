
import eventlet
eventlet.monkey_patch()


from app import create_app, socketio
from flask_socketio import SocketIO, send, emit
from flask_socketio import SocketIO, join_room, leave_room
from datetime import datetime



app = create_app('development')
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    print('Client connected')  # This should print when the client connects

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')  # This should print when the client disconnects

@socketio.on('send_message')
def handle_message(data):
    print('Message received:', data) # This will print the message data to the terminal
    data['time'] = datetime.now().strftime('%H:%M')
    # Emit the message to all clients in the room
    socketio.emit('receive_message', data, room=data['room'])


room_users = {}


@socketio.on('join')
def on_join(data, sid=None):
    room = data['room']
    username = data.get('username')

    # Initialize the room list if it doesn't exist
    if room not in room_users:
        room_users[room] = set()

    # Determine if the user is already in the room
    is_new_join = username not in room_users[room]

    if is_new_join:  # First time joining, show the "You joined the room" message to the user
        join_room(room)
        room_users[room].add(username)

        # Notify only the joining user with "You joined the room"
        emit('receive_message', {
            'type': 'system',
            'message': 'You joined the room',
            'is_self': True,
            'time': datetime.now().strftime('%H:%M')
        }, to=sid)  # Use `sid` to send only to the joining user

        # Notify other users in the room about the new user
        emit('receive_message', {
            'type': 'system',
            'message': f'{username} has entered the room.',
            'time': datetime.now().strftime('%H:%M')
        }, room=room, include_self=False)  # Only others in the room see this message

    print(f'{username} has joined the room: {room}')



@socketio.on('leave')
def on_leave(data):
    room = data['room']
    username = data.get('username')

    
    if room in room_users and username in room_users[room]:
        # Remove the user from the room and broadcast leave message
        leave_room(room)
        room_users[room].discard(username)

        emit('receive_message', {
            'type': 'system',
            'message': f'{username} has left the room.',
            'time': datetime.now().strftime('%H:%M')
        }, room=room)

        # Clean up the room if empty
        if not room_users[room]:
            del room_users[room]

    print(f'{username} has left the room: {room}')



if __name__ == '__main__':
    socketio.run(app, debug=True)
