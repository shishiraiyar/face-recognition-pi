from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room


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
    emit("showConsole", "KALLAN KALLAN oodi Vaa KALLANN", room=connections["browser"])
    pass

@socketio.on('log')
def handleLog(string):
    emit('showConsole', string, room=connections['browser'])


if __name__ == "__main__":
    socketio.run(app=app, debug=True, host="0.0.0.0", port=5000)

"www.intruderDetector.com/intruderDetected" 



"www.intruderDetector.com/intruderDetected"

"""if intruder:
    socket.emit("intruder", {data data})

socket.on("unlock)
    unlockDoor()

"""