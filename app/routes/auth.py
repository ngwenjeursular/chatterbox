from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models.user import User
from app.forms import ProfileForm
from flask import current_app
from werkzeug.utils import secure_filename
import os
import secrets
from PIL import Image

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now log in.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home.index'))
        else:
            flash('Login failed. Check your username and password.')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


def save_picture(form_picture):
    """Save the uploaded profile picture, resize it, and return the filename."""
    random_hex = secrets.token_hex(8)  # Create a random name for the file
    _, f_ext = os.path.splitext(secure_filename(form_picture.filename))  # Extract extension
    picture_fn = random_hex + f_ext  # Create a new filename with a random hex and extension
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)  # Full path

    # Resize the image before saving
    output_size = (525, 525)  # Adjust the size for a round profile pic look
    i = Image.open(form_picture)
    i.thumbnail(output_size)  # Resize the image

    i.save(picture_path)  # Save the resized image

    return picture_fn  # Return only the filename


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    if form.validate_on_submit():
        current_user.email = form.email.data

        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)  # Call save_picture
            current_user.profile_picture = picture_file  # Store only the filename

        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('auth.profile'))

    # Pre-fill the form with current user data
    form.email.data = current_user.email
    return render_template('view_profile.html', form=form)
