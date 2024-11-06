from app import db
from datetime import datetime

class Message(db.Model):
    """
    Model for storing messages with room, username, message, and timestamp fields.
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    profile_picture = db.Column(db.String(200), default='https://picsum.photos/seed/default/40')
    timestamp = db.Column(db.DateTime, nullable=False)


    def __init__(self, room, username, message, profile_picture=None, timestamp=None):
        self.room = room
        self.username = username
        self.message = message
        self.profile_picture = profile_picture or 'https://picsum.photos/seed/default/40'
        self.timestamp = timestamp if timestamp else datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'room': self.room,
            'username': self.username,
            'message': self.message,
            'profile_picture': self.profile_picture,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }