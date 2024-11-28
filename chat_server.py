import asyncio
import websockets
import os

# List of connected clients
connected_clients = set()

# WebSocket handler to handle incoming messages
async def handle_connection(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast the message to all other clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    finally:
        connected_clients.remove(websocket)

# Start the WebSocket server on port 8765
async def main():
    server = await websockets.serve(handle_connection, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

# Start WebSocket server in an asyncio loop
asyncio.get_event_loop().run_until_complete(main())

# Create a simple HTML chat client to be served by a basic HTTP server
html_chat_client = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Chat</title>
    <style>
        body { font-family: Arial, sans-serif; }
        #messages { max-height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
        input { padding: 5px; width: 80%; }
        button { padding: 5px; }
    </style>
</head>
<body>
    <h1>Chat System</h1>
    <div id="messages"></div>
    <input type="text" id="message-input" placeholder="Type a message..." />
    <button onclick="sendMessage()">Send</button>

    <script>
        const socket = new WebSocket('ws://localhost:8765');
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('message-input');

        socket.onopen = function() {
            console.log("Connected to WebSocket server");
        };

        socket.onmessage = function(event) {
            const message = event.data;
            messagesDiv.innerHTML += '<div>' + message + '</div>';
            messagesDiv.scrollTop = messagesDiv.scrollHeight;  // Scroll to the bottom
        };

        function sendMessage() {
            const message = messageInput.value;
            if (message) {
                socket.send(message);
                messageInput.value = '';
            }
        }
    </script>
</body>
</html>
"""
