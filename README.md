# ChatterBox Chat Room

ChatterBox is a real-time chat room application designed for smooth, instantaneous communication between users in a shared space. Built with Socket.io, Flask, and modern front-end styling, ChatterBox offers a user-friendly, minimalist interface suitable for both desktop and mobile use.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure and Styling](#code-structure-and-styling)
- [Customization](#customization)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Real-time Messaging:** Users can chat in real time, seeing each message immediately as it’s sent.
- **Responsive Design:** Optimized for both desktop and mobile views, ensuring accessibility on all devices.
- **User Identification:** Customizable usernames and profile pictures make it easy to identify users in each chat room.
- **System Notifications:** Clear, styled messages for events like joining and leaving rooms.
- **Copyable Room Code:** Each room has a unique code for easy sharing and quick access.
- **Message and Button Styling:** Modern, clean design with accessible styling for better user interaction.

## Technologies Used
- **Frontend:** HTML, CSS (Flexbox, and responsive design), JavaScript
- **Backend:** Python (Flask)
- **WebSockets:** Socket.io for real-time message broadcasting
- **Version Control:** Git

## Installation
To set up ChatterBox on your local machine, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/chatterbox.git
    ```

2. Navigate to the project folder:
    ```bash
    cd chatterbox
    ```

3. Install dependencies: Make sure you have Python and Flask installed. Install dependencies with:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the server:
    ```bash
    flask run
    ```

5. Access the application: Open your web browser and go to `http://127.0.0.1:5000`.

## Usage
- **Creating a Room:** Upon loading the app, users can create a new chat room with a unique code.
- **Joining a Room:** Enter the room code provided to join an existing chat room.
- **Sending Messages:** Type messages in the input box and hit “Send.” Messages will display in real time.
- **Copy Room Code:** Click "Copy" next to the room code to share it with others easily.

### Room Interface
- **Message Display:** Messages appear instantly within the chat box, along with system notifications (e.g., “You joined the room”).
- **Message Input Box:** Type a message here; it spans the full width for easy typing.
- **Send Button:** Click to send the message; it's styled for easy recognition and user-friendliness.

## Code Structure and Styling
The project codebase is structured for ease of understanding and maintenance:

- **HTML and CSS:** Following a modern, minimalist style with a black, white, and #f4f4f4 color palette. CSS classes are named semantically for quick reference.
- **JavaScript:** Socket.io manages real-time events, with each message transmitted and displayed as a single instance. Efforts were made to prevent duplicate message issues.
- **Flask Backend:** Serves static files and handles the WebSocket connection for each room.

### Key Styling Choices
- **Centered Interface:** The entire chat room container is centered on the page.
- **Flexible Layouts:** Using Flexbox for intuitive alignment of elements like the chat input and send button.
- **Message Visibility:** System messages (e.g., “You joined the room”) are styled for clear visibility.

## Customization
To tailor ChatterBox for your needs, consider modifying the following:

- **Message Styles:** Update `.system-message` or `.message-content` CSS classes to adjust appearance.
- **Room Code Copy Functionality:** Adjust the JavaScript function `copyRoomCode()` if needed.
- **Responsive Design:** Further optimize for various screen sizes by tweaking breakpoints in the CSS file.

## Future Improvements
- **Enhanced User Authentication:** Integrate a login system to track user sessions.
- **Message Reactions:** Add reactions (like emojis) for quick user responses.
- **File Sharing:** Enable image or document sharing within the chat.
- **Theme Switching:** Add a dark/light mode toggle for user preference.

## Contributing
Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

Enjoy chatting with ChatterBox—simple, stylish, and effective.