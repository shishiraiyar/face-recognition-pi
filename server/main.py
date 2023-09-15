from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import base64
from PIL import Image


app = Flask(__name__)
socketio = SocketIO(app)

connections = {"browser": None, "pi": None}

@socketio.on('connect')
def handleConnect():
    print("CONNECTED", request.sid)

@socketio.on("identify")
def handleIdentify(who):
    connections[who] = request.sid

@socketio.on('disconnect')
def handleDisconnect():
    print('DISCONNECTED')

@app.route("/")
def home():
    return render_template("index.html")


@socketio.on("unlock")
def handleBaton():
    emit("unlockDoor", room=connections["pi"])

@socketio.on("intruderDetected")
def handleIntruder():
    print("AYYOOO KALLLAAA")
    emit("showConsole", "Intruder detected. Do you know them?", room=connections["browser"])
    pass

@socketio.on('log')
def handleLog(string):
    emit('doorUnlocked', room=connections['browser'])
    emit('showConsole', string, room=connections['browser'])

# @app.route('/housePicture', methods=['POST'])
# def handle_image():
#     data = request.json
#     print("PIC CAME")
#     decoded_image = base64.b64decode(data['image'])
#     with open("static/images/house.jpg", 'wb') as f:
#         f.write(decoded_image)
        
#     return jsonify({'message': 'Image received and saved successfully'})

@app.route('/housePicture', methods=['POST'])
def upload_image():
    try:
        uploaded_image = request.files['image']

        if uploaded_image:
            # Read the uploaded image and convert it to a PIL image
            pil_image = Image.open(uploaded_image)

            # Process the PIL image as needed (e.g., save it, perform operations)
            # For demonstration, we'll just save it to a file
            pil_image.save('static/images/house.jpg')

            return jsonify({'message': 'Image uploaded and processed successfully.'}), 200
        else:
            return jsonify({'error': 'No image uploaded.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('updateImage')
def handle_image_update():
     emit('updatePicture', room=connections['browser'])



if __name__ == "__main__":
    socketio.run(app=app, debug=True, host="0.0.0.0", port=5000)

"www.intruderDetector.com/intruderDetected" 



"www.intruderDetector.com/intruderDetected"

"""if intruder:
    socket.emit("intruder", {data data})

socket.on("unlock)
    unlockDoor()

"""