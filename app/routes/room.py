from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user, AnonymousUserMixin
from datetime import datetime
from app.models.user import User
from app.models.messages import Message
from app.models.room import Room
from datetime import datetime
from app.forms import ProfileForm
import random
import string
from flask import jsonify
from app import db





room_bp = Blueprint('room', __name__)


@room_bp.route('/join_room', methods=['POST'])
def join_room():
	room_code = request.form.get('room_code')

	room = Room.query.filter_by(room_code=room_code).first()
	if not room:
		flash("Room not found", "error")
		return redirect(url_for('home.user'))

	# Retrieve user nickname or guest name
	if current_user.is_authenticated:
		#user_name = current_user.nickname
		user_name = current_user.nickname if current_user.nickname else current_user.username

	else:
		user_name = session.get('guest_name', 'Guest')

	# Add logic here to join the room using room_code

	# Redirect to chat room page
	return redirect(url_for('room.chat_room', room_code=room_code))

rooms = {}

def generate_room_code():
	"""Generates a 6-character room code"""
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@room_bp.route('/create_room', methods=['POST'])
def create_room():
	if not current_user.is_authenticated and not session.get('guest_name'):
		flash("Please enter your name to create a room.", "error")
		return redirect(url_for('home.index'))

	room_code = generate_room_code()


	# Get user or guest name
	if current_user.is_authenticated:
		#user_name = current_user.nickname
		user_name = current_user.nickname if current_user.nickname else current_user.username

	else:
		user_name = session.get('guest_name', 'Guest')

	# Record the time when the room is created
	created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	# Add logic here to create the room (e.g., saving to database)

	# Store room details in the rooms dictionary
	rooms[room_code] = {
		'creator': user_name,
		'created_at': created_at
	}

	# added
	room = Room(room_code=room_code, creator=user_name)
	db.session.add(room)
	db.session.commit()

	# Redirect user to the newly created room
	return redirect(url_for('room.chat_room', room_code=room_code, creator=user_name, time=created_at))


def get_current_user():
	"""
	This function returns the current logged-in user by checking the session.
	If no user is logged in, it returns None.
	"""
	# Check if the user_id is stored in the session (which usually happens when a user logs in)
	user_id = session.get('user_id')
	
	if user_id:
		# If the user_id exists, query the database for the user
		current_user = User.query.filter_by(id=user_id).first()
		if current_user:
			return current_user
	
	# If no user is logged in, return None
	return None

# @room_bp.route('/chat_room/<room_code>')
# def chat_room(room_code):

#     # Fetch the room details from the dictionary
#     room_details = rooms.get(room_code, None)
#     user = get_current_user()


#     if user:
#         user_name = current_user.nickname
#         profile_picture = user.profile_picture  # Use user's profile pic
#     else:
#         user_name = "Guest"
#         # Use random picture source for guests
#         profile_picture = 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))

#     if room_details is None:
#         # If room is not found, return a 404 or error message
#         return "Room not found", 404

#     # Retrieve user name
#     if current_user.is_authenticated:
#         user_name = current_user.nickname
#     else:
#         user_name = session.get('guest_name', 'Guest')

#     # Render the chat room template with the room creator and timestamp
#     return render_template('chat_room.html',
#                            room_code=room_code,
#                            username=user_name,
#                            creator=room_details['creator'],
#                            created_at=room_details['created_at'],
#                            profile_picture=profile_picture
#                            )



import random
from flask import session, render_template, redirect, url_for
from flask_login import current_user, AnonymousUserMixin

# @room_bp.route('/chat_room/<room_code>')
# def chat_room(room_code):
# 	# Fetch the room details from the dictionary
# 	room_details = rooms.get(room_code, None)
# 	user = get_current_user()

# 	if user:
# 		user_name = user.nickname
# 		profile_picture = url_for('static', filename='uploads/' + user.profile_picture)
# 	else:
# 		user_name = "Guest"
# 		profile_picture = 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))

# #		profile_picture = url_for('static', filename='uploads/default.jpg')  # Default image for guests


# 	if room_details is None:
# 		# If room is not found, return a 404 or error message
# 		return "Room not found", 404

# 	# Retrieve user name for display
# 	if current_user.is_authenticated:
# 		user_name = current_user.nickname
# 	else:
# 		user_name = session.get('guest_name', 'Guest')

# 	# Render the chat room template with the room creator and timestamp
# 	return render_template('chat_room.html',
# 						   room_code=room_code,
# 						   username=user_name,
# 						   creator=room_details['creator'],
# 						   created_at=room_details['created_at'],
# 						   profile_picture=profile_picture)



# this one works!
# @room_bp.route('/chat_room/<room_code>')
# def chat_room(room_code):
# 	"""
# 	Renders the chat room, setting the username and profile picture based on
# 	whether the user is authenticated or a guest.
# 	"""
# 	# Fetch the room details from the dictionary
# 	room_details = rooms.get(room_code, None)

# 	if room_details is None:
# 		return "Room not found", 404

# 	# Determine if user is authenticated or a guest
# 	if current_user.is_authenticated:
# 		user_name = current_user.nickname if current_user.nickname else current_user.username
# 		#profile_picture = url_for('static', filename='uploads/' + current_user.profile_picture)
# 		profile_picture = (
# 			url_for('static', filename='uploads/' + current_user.profile_picture)
# 			if current_user.profile_picture else 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))
# 		)
# 	else:
# 		# Set guest user details
# 		user_name = session.get('guest_name', 'Guest')
# 		profile_picture = 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))
# 		# Alternatively, use local default: profile_picture = url_for('static', filename='uploads/default.jpg')

# 	# Render the chat room template
# 	return render_template(
# 		'chat_room.html',
# 		room_code=room_code,
# 		username=user_name,
# 		creator=room_details['creator'],
# 		created_at=room_details['created_at'],
# 		profile_picture=profile_picture
# 	)





@room_bp.route('/chat_room/<room_code>')
def chat_room(room_code):
    """Renders the chat room, setting the username and profile picture based on whether the user is authenticated or a guest."""

    room = Room.query.filter_by(room_code=room_code).first_or_404()
    messages = (
        Message.query.filter_by(room=room_code)
        .order_by(Message.timestamp.desc())
        .limit(50)
        .all()
    )

    room_details = rooms.get(room_code, None)
    if room_details is None:
        return "Room not found", 404

    # Determine if user is authenticated or a guest
    if current_user.is_authenticated:
        user_name = current_user.nickname if current_user.nickname else current_user.username
        profile_picture = (
            url_for('static', filename='uploads/' + current_user.profile_picture)
            if current_user.profile_picture
            else 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))
        )
    else:
        # Set guest user details
        user_name = session.get('guest_name', 'Guest')
        # Only set a consistent guest profile picture if it hasn't been set before
        if 'guest_profile_picture' not in session:
            session['guest_profile_picture'] = 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))
        profile_picture = session['guest_profile_picture']

    return render_template(
        'chat_room.html',
        room_code=room_code,
        username=user_name,
        creator=room_details['creator'],
        created_at=room_details['created_at'],
        profile_picture=profile_picture,
        messages=messages
    )

@room_bp.route('/get_messages/<room_code>', methods=['GET'])
def get_messages(room_code):
	"""
	Fetches all previous messages for a specific room.
	"""
	messages = Message.query.filter_by(room=room_code).order_by(Message.timestamp).all()
	return jsonify([
		{
			'username': message.username,
			'message': message.message,
			'profilePicture': message.profile_picture,
			'time': message.timestamp.strftime('%H:%M')
		}
		for message in messages
	])


@room_bp.route('/load_messages/<room_code>')
def load_messages(room_code):
    # Query all messages for the specified room from the database
    messages = Message.query.filter_by(room=room_code).all()
    messages_data = [
        {
            "username": message.username,
            "message": message.message,
            "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "profile_picture": message.profile_picture
        }
        for message in messages
    ]
    return jsonify(messages_data)



@room_bp.route('/send_message', methods=['POST'])
def send_message():
    # Extract message data
    data = request.get_json()

    # Check for missing required fields
    if not all(field in data for field in ('message', 'room', 'username')):
        return jsonify({'error': 'Missing required fields'}), 400

    message = data['message']
    room = data['room']
    username = data['username']

    # Get profile picture from session if guest, else from user
    if 'guest_profile_picture' in session:
        profile_picture = session['guest_profile_picture']
    elif current_user.is_authenticated:
        profile_picture = url_for('static', filename='uploads/' + current_user.profile_picture) if current_user.profile_picture else 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))
    else:
        profile_picture = 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))

    # Emit the message to the socket
    emit('receive_message', {
        'message': message,
        'username': username,
        'profilePicture': profile_picture,
        'time': datetime.now().strftime("%H:%M:%S")
    }, room=room)

    return jsonify(success=True), 200