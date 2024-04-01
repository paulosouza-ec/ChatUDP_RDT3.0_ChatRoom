-The goal of this project is to create a single-room chat system where users can connect, send public messages, private messages, leave the room, list connected users, and even kick other users.

The chat server maintains a table of logged in users, storing their usernames and their IP addresses and ports. The client connects to the server, sends messages and receives messages from other users in the room.

Implemented Features:
- Chat room connection
- Sending and receiving public messages
- Sending private messages
- Displaying the list of connected users
- Kick out users from the room
- Reliable transmission using the RDT 3.0 protocol
- 
How to use:
1. Clone this repository to your local machine.
2. Run the chat server using the server.py file.
3. Run the chat client using the client.py file and follow the instructions presented on the command line to connect to the room, send messages, etc.
