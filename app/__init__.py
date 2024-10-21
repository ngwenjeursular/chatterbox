from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from app.config import config
from flask_migrate import Migrate

db = SQLAlchemy()
socketio = SocketIO()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

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

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        db.create_all()

    return app