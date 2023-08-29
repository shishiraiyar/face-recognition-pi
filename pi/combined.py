from io import BytesIO
import face_recognition
from time import sleep
from picamera import PiCamera
from PIL import Image
import numpy as np
import os
from os import listdir

camera = None
knownFaces = []
names = []

def camInit():
    global camera
    camera = PiCamera() #takes time 
    camera.start_preview()
    sleep(1) 

def takePic():
    global camera 
    stream = BytesIO()
    camera.capture(stream, format='jpeg', resize=(500,500))    
    stream.seek(0)
    image = Image.open(stream)
    return image


def encodeKnownFaces():
    global knownFaces, names
    # get the path/directory
    folder_dir = "./known" 
    for image in os.listdir(folder_dir):
        if (image.endswith(".jpeg")):
            image = image.split(".")[0]
            print(f"Loading face of {image}")
            encoding = face_recognition.face_encodings(face_recognition.load_image_file(folder_dir + "/" + image))[0]
            names.append(image)
            knownFaces.append(encoding)



# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.

def faceRecognition(unknownImage):
    global knownFaces, names
    # -1 No face
    # 0 Allowed
    # 1 Thief
    unknownImage = np.array(unknownImage)
    unknownFaceencodings = face_recognition.face_encodings(unknownImage)

    if (len(unknownFaceencodings) == 0):
        print("No face")
        return -1

    results = face_recognition.compare_faces(knownFaces, unknownFaceencodings[0])
    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    for i in range(len(results)):
        if results[i]:
            print(f"My name is {names[i]}")
            return 0
    print("I am a thief hehehehehe")

    return 1


if __name__ == "__main__":
    print("Initialising")
    camInit()
    encodeKnownFaces()
    print("Get ready to take pic")
    img = takePic()
    faceRecognition(img)


