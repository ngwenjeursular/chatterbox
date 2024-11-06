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

socket.on('connect', function() {
	console.log('Connected to the server');
	socket.emit('join', { room: room, username: username, current_user: username });
});

socket.on('connect', () => {
    console.log('Connected to socket after refresh');
});

// Example room joining on connect
socket.on('connect', () => {
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

document.getElementById('message-input').addEventListener('keydown', function (event) {
	if (event.key === 'Enter' && !event.shiftKey) {
		event.preventDefault(); 
		sendMessage();
	}
});

document.addEventListener('DOMContentLoaded', () => {
	const room = chatRoomContainer.getAttribute('data-room');
	loadMessages(room);
});


function saveMessage(room, username, message, timestamp) {
	fetch('/save_message', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			room: room,
			username: username,
			message: message,
			timestamp: timestamp
		})
	})
	.then(response => {
		if (response.ok) {
			return response.json();
		} else {
			throw new Error('Non-JSON response or server error');
		}
	})
	.then(data => {
		console.log(data.status); // Logs "Message saved" on success
	})
	.catch(error => console.error('Error saving message:', error));
	
}

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


function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    const username = chatRoomContainer.getAttribute('data-username');
    const room = chatRoomContainer.getAttribute('data-room');
    const timestamp = new Date().toISOString();

	if (message.trim() === "") return;

    console.log('Sending message:', { room, username, message, timestamp }); // Log message data


	console.log("Emitting message:", message);
    // Emit message to the WebSocket server
    if (message !== '') {
		socket.emit('send_message', {
			room: room,
			username: username,
			message: message,
			timestamp: new Date().toISOString(),
			profilePicture: profilePicture,
			//'room_id': room_id,
		});
		messageInput.value = '';  // Clear the input after sending
	}

    // Save message to the database
    saveMessage(room, username, message, timestamp);

    messageInput.value = ''; // Clear the input field
}



/*
socket.on('receive_message', function(data) {
	const chatBox = document.getElementById('chat-box');

	const messageContainer = document.createElement('div');
	messageContainer.classList.add('message-container');

	if (data.type === 'system') {
		const messageElement = document.createElement('div');
		messageElement.classList.add('system-message');
		
		const systemMessage = data.is_self ? 'You joined the room' : data.message;
		messageElement.innerHTML = `<p>${systemMessage}</p><span>${data.time}</span>`;
		messageContainer.appendChild(messageElement);
	} else {
		messageContainer.classList.add('message-container');
		messageContainer.classList.add(data.username === username ? 'outgoing' : 'incoming');

		if (data.profilePicture) {
			const profilePicElement = document.createElement('img');
			profilePicElement.src = data.profilePicture;
			profilePicElement.alt = 'Profile Picture';
			profilePicElement.classList.add('mini-profile-pic');
			messageContainer.appendChild(profilePicElement);
		}

		const messageContent = document.createElement('div');
		messageContent.classList.add('message-content');

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

		if (data.time) {
			const timestampElement = document.createElement('div');
			timestampElement.classList.add('timestamp');
			timestampElement.innerText = data.time;
			messageContent.appendChild(timestampElement);
		}

		messageContainer.appendChild(messageContent);
	}

	chatBox.appendChild(messageContainer);
	chatBox.scrollTop = chatBox.scrollHeight;
});
*/
/*
socket.on('receive_message', function(data) {
	const chatBox = document.getElementById('chat-box');
	console.log("Received message data:", data); // Debugging output

	if (!chatBox) {
		console.error("Chat box not found!");
		return;
	}

	const messageContainer = document.createElement('div');
	messageContainer.classList.add('message-container');
	messageContainer.classList.add(data.username === username ? 'outgoing' : 'incoming');

	// Profile picture check
	if (data.profilePicture) {
		const profilePicElement = document.createElement('img');
		profilePicElement.src = data.profilePicture;
		profilePicElement.alt = 'Profile Picture';
		profilePicElement.classList.add('mini-profile-pic');
		messageContainer.appendChild(profilePicElement);
	}

	const messageContent = document.createElement('div');
	messageContent.classList.add('message-content');

	const messageText = document.createElement('div');
	messageText.classList.add('text');
	messageText.innerText = data.message;
	messageContent.appendChild(messageText);

	const timestampElement = document.createElement('div');
	timestampElement.classList.add('timestamp');
	timestampElement.innerText = data.time;
	messageContent.appendChild(timestampElement);

	messageContainer.appendChild(messageContent);

	chatBox.appendChild(messageContainer);
	chatBox.scrollTop = chatBox.scrollHeight;
});
*/


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




function loadMessages(room) {
	const roomCode = chatRoomContainer.getAttribute('data-room');

	fetch(`/room/get_messages/${roomCode}`)
		.then(response => response.json())
		.then(messages => {
			
			const messageContainer = document.getElementById('message-input');
			messageContainer.innerHTML = ''; // Clear any existing messages



			messages.forEach(msg => {
				const messageElement = document.createElement('div');
				messageElement.classList.add('message');
				messageElement.innerHTML = `<strong>${msg.username}</strong>: ${msg.message} <em>${msg.timestamp}</em>`;
				messageContainer.appendChild(messageElement);
			});
		})
		.catch(error => console.error('Error loading messages:', error));
}


document.addEventListener("DOMContentLoaded", function () {
	const createdAtElement = document.getElementById("created-at");
	const rawTimestamp = createdAtElement.getAttribute("data-created-at");
	createdAtElement.textContent = formatTimestamp(rawTimestamp);
});

document.getElementById('leave-room-button').addEventListener('click', function() {
	socket.emit('leave', { 'username': username, 'room': room });
	window.location.href = '/start-chat';
});


// Event listener for receiving new messages via WebSocket
socket.on('send_message', function(data) {
	const messageContainer = document.getElementById('message-container');
	const messageElement = document.createElement('div');
	messageElement.classList.add('message');
	messageElement.innerHTML = `<strong>${data.username}</strong>: ${data.message} <em>${data.timestamp}</em>`;
	messageContainer.appendChild(messageElement);
	messageContainer.scrollTop = messageContainer.scrollHeight;
});

// Event listener for the send button
document.getElementById('send-btn').addEventListener('click', sendMessage);

// Optional: Send message on "Enter" key press
document.getElementById('message-input').addEventListener('keyup', function(event) {
	if (event.key === 'Enter') {
		sendMessage();
	}
});


/* Fetch messages on page load*
document.addEventListener('DOMContentLoaded', () => {
	const roomCode = chatRoomContainer.getAttribute('data-room');


	// Fetch existing messages for the room
	fetch(`/get_messages/${roomCode}`)
		.then(response => response.json())
		.then(messages => {
			const messageContainer = document.getElementById('message-container');
			messages.forEach(data => {
				// Display each message in the chat
				const messageElement = document.createElement('div');
				messageElement.classList.add('message');
				messageElement.innerHTML = `<strong>${data.username}</strong>: ${data.message} <em>${data.time}</em>`;
				messageContainer.appendChild(messageElement);
			});
			//messageContainer.scrollTop = messageContainer.scrollHeight;
		})
		.catch(error => console.error('Error fetching messages:', error));
});
*/

/*
document.addEventListener('DOMContentLoaded', () => {
	const roomCode = chatRoomContainer.getAttribute('data-room');
    const messageContainer = document.getElementById('message-display-container');

    // Fetch existing messages when the page loads
    fetch(`/room/load_messages/${roomCode}`)  // Assuming `roomCode` is defined globally
	.then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(messages => {
        messages.forEach(data => displayMessage(data));
    })
    .catch(error => console.error("Error loading messages:", error));

    function displayMessage(data) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.innerHTML = `<strong>${data.username}</strong>: ${data.message} <em>${data.timestamp}</em>`;
        messageContainer.appendChild(messageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    // Event listener for new messages sent by the client
    document.getElementById('chat-form').onsubmit = function() {
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value;
        socket.emit('send_message', {
            room: roomCode,
            message: message,
            username: userName  // Make sure `userName` is defined globally or fetched from the server
        });
        messageInput.value = '';
        return false;
    };

    // Socket listener for incoming messages
    socket.on('receive_message', data => {
        displayMessage(data);
    });
});

*******/

/*
document.addEventListener('DOMContentLoaded', () => {
	const roomCode = chatRoomContainer.getAttribute('data-room');
	const chatBox = document.getElementById('chat-box');

	// Fetch existing messages when the page loads
	fetch(`/room/load_messages/${roomCode}`)
		.then(response => {
			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}
			return response.json();
		})
		.then(messages => {
			messages.forEach(data => displayStyledMessage(data, false));  // Loaded messages, not real-time
		})
		.catch(error => console.error("Error loading messages:", error));

	// Display a styled message with content and user distinctions
	function displayStyledMessage(data, isRealTime = true) {
		const messageContainer = document.createElement('div');
		messageContainer.classList.add('message-container');

		// System message handling
		if (data.type === 'system') {
			const messageElement = document.createElement('div');
			messageElement.classList.add('system-message');
			
			// Show personalized message for the user
			const systemMessage = data.is_self ? 'You joined the room' : data.message;
			messageElement.innerHTML = `<p>${systemMessage}</p><span>${data.time}</span>`;
			messageContainer.appendChild(messageElement);

		} else {
			// Add 'outgoing' or 'incoming' class based on sender
			if (data.username === username) {
				messageContainer.classList.add('outgoing');
			} else {
				messageContainer.classList.add('incoming');
			}

			// Add profile picture if available
			if (data.profilePicture) {
				const profilePicElement = document.createElement('img');
				profilePicElement.src = data.profilePicture;
				profilePicElement.alt = 'Profile Picture';
				profilePicElement.classList.add('mini-profile-pic');
				messageContainer.appendChild(profilePicElement);
			}

			// Create message content structure
			const messageContent = document.createElement('div');
			messageContent.classList.add('message-content');

			// Add username for incoming messages
			if (data.username !== username) {
				const usernameElement = document.createElement('span');
				usernameElement.classList.add('username');
				usernameElement.innerText = data.username;
				messageContent.appendChild(usernameElement);
			}

			// Add the actual message text
			const messageText = document.createElement('div');
			messageText.classList.add('text');
			messageText.innerText = data.message;
			messageContent.appendChild(messageText);

			// Add timestamp if available
			if (data.time) {
				const timestampElement = document.createElement('div');
				timestampElement.classList.add('timestamp');
				timestampElement.innerText = data.time;
				messageContent.appendChild(timestampElement);
			}

			messageContainer.appendChild(messageContent);
		}

		// Append message to chatBox and scroll to the latest message
		chatBox.appendChild(messageContainer);
		chatBox.scrollTop = chatBox.scrollHeight;

		// Optionally save to database if it's a new message from the user
		if (isRealTime) saveMessageToDatabase(data);
	}

	// Function to save messages to the database
	// modified here
	function saveMessageToDatabase(data) {
		fetch(`/room/save_message`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				room: roomCode,
				message: data.message,
				username: data.username,
				timestamp: data.timestamp || new Date().toLocaleTimeString()
			})
		}).catch(error => console.error("Error saving message:", error));
	}

	// Event listener for sending a new message
	document.getElementById('chat-form').onsubmit = function() {
		const messageInput = document.getElementById('message-input');
		const message = messageInput.value;

		socket.emit('send_message', {
			room: roomCode,
			message: message,
			username: username  // Ensure `username` is defined globally
		});

		// Display the sent message immediately with the current timestamp
		displayStyledMessage({
			username: username,
			message: message,
			time: new Date().toLocaleTimeString()
		}, true);

		messageInput.value = '';
		return false;
	};

	// Socket listener for incoming messages
	socket.on('receive_message', data => {
		// Display received message only if it's not from the current user
		if (data.username !== username) {
			displayStyledMessage(data, false);  // `false` as it's not a new message from this user
		}
	});
});
*/




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


	if (roomCode) {
		fetch(`/room/load_messages/${roomCode}`)
			.then(response => response.json())
			.then(messages => {
				messages.forEach(data => displayStyledMessage(data));
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

		/*
		// Add profile picture if available
		if (data.profilePicture) {
			const profilePicElement = document.createElement('img');
			profilePicElement.src = data.profilePicture;
			profilePicElement.alt = `${data.username}'s profile picture`;
			profilePicElement.classList.add('profile-pic');
			messageElement.appendChild(profilePicElement);
		}
		*/

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

		if (isRealTime) saveMessageToDatabase(data);
	}

	// Function to save a message to the database
	function saveMessageToDatabase(data) {
		fetch(`/save_message`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				room: roomCode,
				message: data.message,
				username: data.username,
				timestamp: data.timestamp || new Date().toLocaleTimeString(),
				profilePicture: data.profilePicture
			})
		}).catch(error => console.error("Error saving message:", error));
	}

	// Send message on form submit
	document.getElementById('chat-form').onsubmit = function() {
		const messageInput = document.getElementById('message-input');
		const message = messageInput.value;

		socket.emit('send_message', {
			room: roomCode,
			message: message,
			username: username,
			profilePicture: profilePicture
		});

		messageInput.value = '';
		return false;
	};

	/*
	// Socket listener for receiving new messages
	// no effect
	socket.on('receive_message', data => {
		if (data.username !== username) {
			displayStyledMessage(data, false);
		}
	});

	*/
	// Rejoin room on reconnect after page refresh
	socket.on('connect', () => {
		socket.emit('join_room', { room: roomCode, username: username });
		console.log('Connected to socket after refresh');
	});
});

