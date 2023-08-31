from picamera import PiCamera
from io import BytesIO
from PIL import Image
from time import sleep
import os
import face_recognition
import numpy as np
import pickle


class Camera:
    IMAGE_SIZE = (500,500)
    def __init__(self):
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(1)

    def takePic(self):
        stream = BytesIO()
        self.camera.capture(stream, format='jpeg', resize= self.IMAGE_SIZE)    
        stream.seek(0)
        image = Image.open(stream)
        return image
        
class FaceRecognition:
    knownFacesDir = "./known"
    def __init__(self):
        self.names = []
        self.knownFaces = []

    def encodeKnownFaces(self):
        for fileName in os.listdir(self.knownFacesDir):
            fileName = fileName.split(".")[0]
            print(f"Loading face of {fileName}")
            imgFile = face_recognition.load_image_file(os.path.join(self.knownFacesDir, fileName))
            encoding = face_recognition.face_encodings(imgFile, num_jitters=10)[0]
            self.names.append(fileName)
            self.knownFaces.append(encoding)

    def checkFace(self, image):
        image = np.array(image)
        print("Encoding...")
        unknownFaceencodings = face_recognition.face_encodings(image)
        if (len(unknownFaceencodings) == 0):
            print("No face")
            return -1

        results = face_recognition.compare_faces(self.knownFaces, unknownFaceencodings[0])
        for i in range(len(results)):
            if results[i]:
                print(f"My name is {self.names[i]}")
                return self.names[i]
        print("I am a thief hehehehehe")

        return 1
    
    def storeEncodingsToFile(self, fileName="./dataset.dat"):
        allFaceEncodings = {}
        for i in range(len(self.names)):
            allFaceEncodings[self.names[i]] = self.knownFaces[i]

        with open(fileName, 'wb') as f:
            pickle.dump(allFaceEncodings, f)

    def loadEncodingsFromFile(self, fileName="./dataset.dat"):
        with open(fileName, 'rb') as f:
            allFaceEncodings = pickle.load(f)

        self.names = list(allFaceEncodings.keys())
        self.knownFaces = np.array(list(allFaceEncodings.values()))

            

