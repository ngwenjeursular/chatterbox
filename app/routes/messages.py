from flask import Blueprint, request, jsonify
from app.models.messages import db, Message  # Assuming a Message model exists in app/models.py
from datetime import datetime

# Set up Blueprint for messages
messages_bp = Blueprint('messages', __name__)

# @messages_bp.route('/save_message', methods=['POST'])
# def save_message():
# 	"""
# 	Save a new message to the database for persistence.
# 	"""
# 	room = request.json.get('room')
# 	username = request.json.get('username')
# 	message = request.json.get('message')
# 	timestamp = request.json.get('timestamp')

# 	# Create a new message entry
# 	new_message = Message(room=room, username=username, message=message, timestamp=timestamp)
# 	db.session.add(new_message)
# 	db.session.commit()

# 	return jsonify({'status': 'Message saved'}), 201


# doesn't work
# @messages_bp.route('/save_message', methods=['POST'])
# def save_message():
#     data = request.json

#     try:
#         # Parse the timestamp string into a Python datetime object
#         timestamp = datetime.fromisoformat(data['timestamp'].replace("Z", "+00:00"))  # Add timezone information if necessary
#         room = data['room']
#         username = data['username']
#         message = data['message']

#         room_id = data.get('room_id')
#         if not room_id:
#             print("Error: room_id not found in data:", data)
#             return  # Handle this case appropriately

#         # Create and save the new message
#         new_message = Message(room=room, room_id=room_id, username=username, message=message, timestamp=timestamp)
#         db.session.add(new_message)
#         db.session.commit()

#         return jsonify({"status": "Message saved"}), 200

#     except Exception as e:
#         print(f"Error saving message: {e}")
#         return jsonify({"status": "Error", "error": str(e)}), 500

from datetime import datetime
import logging

@messages_bp.route('/save_message', methods=['POST'])
def save_message():
    print("Message received for saving")
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    try:
        room = data.get('room')
        username = data.get('username')
        message = data.get('message')
        profile_picture = data.get('profile_picture')
        timestamp = data.get('timestamp')

        # Ensure no required field is missing
        if None in [room, username, message]:
            return jsonify({"status": "error", "message": "Missing required data"}), 400

        # Parse timestamp in ISO format or set to current time
        if timestamp:
            try:
                timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError as ve:
                logging.error(f"Invalid timestamp format: {ve}")
                return jsonify({"status": "error", "message": "Invalid timestamp format"}), 400
        else:
            timestamp = datetime.utcnow()

        # Create and save the new message
        new_message = Message(room=room, username=username, message=message, profile_picture=profile_picture, timestamp=timestamp)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({"status": "Message saved"}), 200

    except Exception as e:
        logging.error(f"Error saving message: {e}")
        return jsonify({"status": "error", "message": "Server error occurred"}), 500


