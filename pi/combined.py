from io import BytesIO
import face_recognition
from time import sleep
from picamera import PiCamera
from PIL import Image
import numpy as np

# Create the in-memory stream
stream = BytesIO()
camera = PiCamera() #takes time 
camera.start_preview()
sleep(2) 
#while starts here 
camera.capture(stream, format='jpeg', resize=(500,500))
# "Rewind" the stream to the beginning so we can read its content
stream.seek(0)
image = Image.open(stream)
image.save("test.jpeg")
#delay of some 5 seconds


# Load the jpg files into numpy arrays
obama_image = face_recognition.load_image_file("./known/jk1")
justin_image = face_recognition.load_image_file("./known/trump")


unknown_image = np.array(image)
# unknown_image = face_recognition.load_image_file("./unknown/jk2")

# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
try:
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
    justin_face_encoding = face_recognition.face_encodings(justin_image)[0]

    
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()

known_faces = [
    obama_face_encoding,
    justin_face_encoding,

]

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

print("Is the unknown face a picture of Obama? {}".format(results[0]))
print("Is the unknown face a picture of Justin? {}".format(results[1]))

print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))

