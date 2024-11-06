from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db

class Room(db.Model):

    __tablename__ = 'rooms'


    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String(6), unique=True, nullable=False)
    creator = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
	#messages = db.relationship('Message', backref='roomz', lazy='dynamic')

    def __repr__(self):
        return f"<Room {self.room_code}>"