import socketio

# Create a SocketIO client instance
sio = socketio.Client()

# Define the event handlers
@sio.on('unlockDoor')
def unlockDoor():
    print("DOOR UNLOCKED")
    # Add your logic for handling event1 here

@sio.on('event2')
def handle_event2(data):
    print("Received event2:", data)
    # Add your logic for handling event2 here

# Connect to the server

sio.connect('http://your_server_ip:your_server_port')

sio.emit("identify", "pi")


sio.emit('intruderDetected')


# Keep the client running
sio.wait()
print("lolol")