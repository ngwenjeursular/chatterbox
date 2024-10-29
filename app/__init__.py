from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, send, emit
from app.config import config
from flask_migrate import Migrate
from datetime import datetime, timedelta
import os

db = SQLAlchemy()
socketio = SocketIO()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)
    socketio.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Import and register blueprints
    from app.routes.home import home_bp
    from app.routes.auth import auth_bp
    from app.routes.profile import profile_bp
    from app.routes.room import room_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp)
    app.register_blueprint(room_bp, url_prefix='/room')

    with app.app_context():
        db.create_all()

    
    return app