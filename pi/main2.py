import socketio
from threading import Thread
from datetime import datetime
from time import sleep
from FaceRecognition import Camera, FaceRecognition
import io
import requests

sio = socketio.Client()
server_url = 'http://192.168.62.108:5000'
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

# sio.connect('https://facerecognitionpi.onrender.com/')
sio.connect(server_url)

sio.emit("identify", "pi")



# Keep the client running
def threadFunc():
    sio.wait()

t = Thread(target=threadFunc)
t.start()

print("lolol")
cam = Camera()
fr = FaceRecognition()
#fr.encodeKnownFaces()       ##
#fr.storeEncodingsToFile()   ##
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
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='JPEG')
        image_bytes = img_byte_array.getvalue()
        files = {'image': ('image.jpg', image_bytes)}
        response = requests.post(server_url + "/housePicture", files=files)
        sio.emit("updateImage")
        continue

    else:
        sio.emit('log',  f"{retVal} has entered the house at {curTime:%Y-%m-%d %H:%M}")
        # Unlock door
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='JPEG')
        image_bytes = img_byte_array.getvalue()
        files = {'image': ('image.jpg', image_bytes)}
        response = requests.post(server_url + "/housePicture", files=files)
        sio.emit("updateImage")

