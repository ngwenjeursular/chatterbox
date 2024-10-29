from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from app.models.user import User
from app.forms import ProfileForm
import random
import string


room_bp = Blueprint('room', __name__)


@room_bp.route('/join_room', methods=['POST'])
def join_room():
	room_code = request.form.get('room_code')

	# Retrieve user nickname or guest name
	if current_user.is_authenticated:
		user_name = current_user.nickname
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
		user_name = current_user.nickname
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

@room_bp.route('/chat_room/<room_code>')
def chat_room(room_code):

    # Fetch the room details from the dictionary
    room_details = rooms.get(room_code, None)
    user = get_current_user()


    if user:
        user_name = current_user.nickname
        profile_picture = user.profile_picture  # Use user's profile pic
    else:
        user_name = "Guest"
        # Use random picture source for guests
        profile_picture = 'https://picsum.photos/seed/{}/40'.format(random.randint(1, 1000))

    if room_details is None:
        # If room is not found, return a 404 or error message
        return "Room not found", 404

    # Retrieve user name
    if current_user.is_authenticated:
        user_name = current_user.nickname
    else:
        user_name = session.get('guest_name', 'Guest')

    # Render the chat room template with the room creator and timestamp
    return render_template('chat_room.html',
                           room_code=room_code,
                           username=user_name,
                           creator=room_details['creator'],
                           created_at=room_details['created_at'],
                           profile_picture=profile_picture
                           )