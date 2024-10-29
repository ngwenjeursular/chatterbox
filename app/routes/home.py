from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import current_user, login_required
from app import  socketio


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def index():
    # If the user is authenticated
	if current_user.is_authenticated:
		nickname = current_user.nickname
		profile_picture = current_user.profile_picture
		# Pass the nickname to the template
		return render_template('base.html', nickname=nickname, profile_picture=profile_picture, logged_in=True)
	else:
		# For guest users
		return render_template('base.html', logged_in=False)


# A SocketIO event for messages
@socketio.on('message')
def handle_message(msg):
    # Broadcast the message to all connected clients
    socketio.send(msg, broadcast=True)