function copyRoomCode() {
	var roomCodeInput = document.getElementById("roomCode");
	roomCodeInput.select();
	roomCodeInput.setSelectionRange(0, 99999); // For mobile devices
	document.execCommand("copy");
	alert("Room code copied: " + roomCodeInput.value);
}

// Establish socket connection
var socket = io('http://127.0.0.1:5000', {
	transports: ['websocket']
});


// Example room joining on connect
socket.on('connect', () => {
	console.log('Connected to the server');
	console.log('Connected to socket after refresh');
	const chatRoomContainer = document.getElementById('chatRoomContainer');
	const roomCode = chatRoomContainer.getAttribute('data-room');
	socket.emit('join', { room: roomCode, username: username });
});


socket.on('disconnect', function() {
	console.log('Disconnected from the server');
});

const chatRoomContainer = document.querySelector('.chat-room-container');
const room = chatRoomContainer.getAttribute('data-room');
const username = chatRoomContainer.getAttribute('data-username');
const profilePicture = chatRoomContainer.getAttribute('data-profile-picture');


document.getElementById('message-input').addEventListener('input', function () {
	this.style.height = 'auto'; 
	this.style.height = (this.scrollHeight) + 'px'; 
});


function formatTimestamp(timestamp) {
	const now = new Date();
	const time = new Date(timestamp);
	const diffInMs = now - time;
	const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
	const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
	const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));

	if (diffInMinutes < 1) {
		return "just now";
	} else if (diffInMinutes < 60) {
		return `${diffInMinutes} minute${diffInMinutes > 1 ? 's' : ''} ago`;
	} else if (diffInHours < 24) {
		return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;
	} else if (diffInDays < 7) {
		const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
		return `on ${dayNames[time.getDay()]}`;
	} else {
		return time.toLocaleDateString();
	}
}



const saveMessage = _.debounce((room, username, message, timestamp) => {
	console.log("Saving message to database:", { room, username, message, timestamp });
	
	// AJAX call
	fetch('/save_message', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ room, username, message, timestamp })
	});
}, 1000); // 1000ms debounce delay to reduce multiple calls


function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    const username = chatRoomContainer.getAttribute('data-username');
    const room = chatRoomContainer.getAttribute('data-room');
    const timestamp = new Date().toISOString();

    if (message.trim() === "") return;

    console.log("Emitting message:", message);
    
    socket.emit('send_message', {
        room: room,
        username: username,
        message: message,
        timestamp: timestamp,
        profilePicture: profilePicture,
    });

    // Clear input and save message only once with debounce
    messageInput.value = '';
    saveMessage(room, username, message, timestamp);
}

// Set to store IDs of rendered messages to avoid duplicates
const addedMessageIds = new Set();



socket.on('receive_message', function(data) {
	

		const chatBox = document.getElementById('chat-box');
		console.log('Received message data:', data);

	
		const messageContainer = document.createElement('div');
		messageContainer.classList.add('message-container');

		// System message handling
		if (data.type === 'system') {
			const messageElement = document.createElement('div');
			messageElement.classList.add('system-message');
			
			// Display a personalized message for the current user
			const systemMessage = data.is_self ? 'You joined the room' : data.message;

			// Populate system message and timestamp
			messageElement.innerHTML = `<p>${systemMessage}</p><span>${data.time}</span>`;
			messageContainer.appendChild(messageElement);
		}  else {
			messageContainer.classList.add('message-container');
	
			// Apply 'outgoing' or 'incoming' based on username
			if (data.username === username) {
				messageContainer.classList.add('outgoing');
			} else {
				messageContainer.classList.add('incoming');
			}
	
			// Profile picture only for user messages
			if (data.profilePicture) {
				const profilePicElement = document.createElement('img');
				profilePicElement.src = data.profilePicture;
				profilePicElement.alt = 'Profile Picture';
				profilePicElement.classList.add('mini-profile-pic');
				messageContainer.appendChild(profilePicElement);
			}
	
			// Create content container for username, message, and timestamp
			const messageContent = document.createElement('div');
			messageContent.classList.add('message-content');
	
			// Add username for incoming messages
			if (data.username !== username) {
				const usernameElement = document.createElement('span');
				usernameElement.classList.add('username');
				usernameElement.innerText = data.username;
				messageContent.appendChild(usernameElement);
			}
	
			// Actual message text
			const messageText = document.createElement('div');
			messageText.classList.add('text');
			messageText.innerText = data.message;
			messageContent.appendChild(messageText);
	
			// Timestamp for the message
			if (data.time) {
				const timestampElement = document.createElement('div');
				timestampElement.classList.add('timestamp');
				timestampElement.innerText = data.time;
				messageContent.appendChild(timestampElement);
			}
	
			messageContainer.appendChild(messageContent);
		}
	
		// Append to chatBox and scroll to latest message
		chatBox.appendChild(messageContainer);
		chatBox.scrollTop = chatBox.scrollHeight;

});






document.addEventListener("DOMContentLoaded", function () {
	const createdAtElement = document.getElementById("created-at");
	const rawTimestamp = createdAtElement.getAttribute("data-created-at");
	createdAtElement.textContent = formatTimestamp(rawTimestamp);
});

document.getElementById('leave-room-button').addEventListener('click', function() {
	socket.emit('leave', { 'username': username, 'room': room });
	window.location.href = '/start-chat';
});


// Event listener for the send button
document.getElementById('send-btn').addEventListener('click', sendMessage);

// Send message on "Enter" key press
document.getElementById('message-input').addEventListener('keyup', function(event) {
	if (event.key === 'Enter') {
		sendMessage();
	}
});



document.addEventListener('DOMContentLoaded', () => {
	const chatBox = document.getElementById('chat-box');
    const messageContainer = document.getElementById('message-container');

	// Get the room code from the data-room attribute
	const chatRoomContainer = document.getElementById('chatRoomContainer');
	const roomCode = chatRoomContainer ? chatRoomContainer.getAttribute('data-room') : null;
	const username = chatRoomContainer.getAttribute('data-username');
	const profilePicture = chatRoomContainer.getAttribute('data-profile-picture');


	console.log("Room code in JavaScript:", roomCode);  // Log to verify roomCode value


	if (!roomCode) {
		console.error("Room code is undefined. Check if it's passed to the template correctly.");
	}


	
	// Track the latest message's timestamp to avoid duplicates
	let latestMessageTimestamp = null;

	// Load messages once on page load
	if (roomCode) {
		fetch(`/room/load_messages/${roomCode}`)
			.then(response => response.json())
			.then(messages => {
				const chatBox = document.getElementById("chat-box"); 
				chatBox.innerHTML = ""; 

				messages.forEach(data => {
					displayStyledMessage(data);
					// Update the latestMessageTimestamp
					if (!latestMessageTimestamp || data.timestamp > latestMessageTimestamp) {
						latestMessageTimestamp = data.timestamp;
					}
				});
			})
			.catch(error => console.error("Error loading messages:", error));
	}
		

	// Function to display styled messages
	function displayStyledMessage(data, isRealTime = true) {
		const messageContainer = document.createElement('div');
		messageContainer.classList.add('message-container', data.username === username ? 'outgoing' : 'incoming');

		
		// Profile picture handling
		const profilePicElement = document.createElement('img');
		profilePicElement.src = data.profilePicture || '/static/uploads/default.jpg';
		profilePicElement.alt = 'Profile Picture';
		profilePicElement.classList.add('mini-profile-pic');
		messageContainer.appendChild(profilePicElement);

		const messageContent = document.createElement('div');
		messageContent.classList.add('message-content');

		// Username display for incoming
		if (data.username !== username) {
			const usernameElement = document.createElement('span');
			usernameElement.classList.add('username');
			usernameElement.innerText = data.username;
			messageContent.appendChild(usernameElement);
		}

		const messageText = document.createElement('div');
		messageText.classList.add('text');
		messageText.innerText = data.message;
		messageContent.appendChild(messageText);

		const timestampElement = document.createElement('div');
		timestampElement.classList.add('timestamp');
		
		// 24-hour format timestamp
		const timestamp = new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
		timestampElement.innerText = data.time || timestamp;
		messageContent.appendChild(timestampElement);

		messageContainer.appendChild(messageContent);
		chatBox.appendChild(messageContainer);
		chatBox.scrollTop = chatBox.scrollHeight;

		//hapa
		//if (isRealTime) saveMessage(data);
	}
	

});


