import socketio
from threading import Thread
from datetime import datetime
from time import sleep
from FaceRecognition import Camera, FaceRecognition

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

sio.connect('https://facerecognitionpi.onrender.com/')
sio.emit("identify", "pi")


sio.emit('intruderDetected')

# Keep the client running
def threadFunc():
    sio.wait()

t = Thread(target=threadFunc)
t.start()

print("lolol")
cam = Camera()
fr = FaceRecognition()
fr.encodeKnownFaces()       ##
fr.storeEncodingsToFile()   ##
fr.loadEncodingsFromFile()


while(True):

    print("Taking picture")
    sleep(1)
    img = cam.takePic()
    retVal = fr.checkFace(img)
    curTime = datetime.now()
    if (retVal == -1):
        continue
    
    elif (retVal == 1):
        sio.emit("intruderDetected")
        continue

    else:
        sio.emit('log',  f"{retVal} has entered the house at {str(curTime)}")
        # Unlock door


    
