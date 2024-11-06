from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import current_user, login_required
from app import  socketio


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def index():
    # If the user is authenticated
	if current_user.is_authenticated:
		#nickname = current_user.nickname
		nickname = current_user.nickname if current_user.nickname else current_user.username

		profile_picture = current_user.profile_picture
		# Pass the nickname to the template
		return render_template('base2.html', nickname=nickname, profile_picture=profile_picture, logged_in=True)
	else:
		# For guest users
		return render_template('base2.html', logged_in=False)


@home_bp.route('/guest-login')
def guest_login():
    return render_template('guest-login.html')


@home_bp.route('/start-chat')
def start_chat():
    return render_template('start-chat.html')


@home_bp.route('/user')
def user():
    if 'logged_in' in session and session['logged_in']:
        nickname = session.get('nickname', 'User')
        return render_template('user.html', nickname=nickname)
    else:
        flash('Please log in to access this page.')
        return redirect(url_for('auth.login'))


# A SocketIO event for messages
@socketio.on('message')
def handle_message(msg):
    # Broadcast the message to all connected clients
    socketio.send(msg, broadcast=True)