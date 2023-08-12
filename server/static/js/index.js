const socket = io()

socket.emit("identify", "browser")





document.getElementById("unlockButton").addEventListener("click", ()=>{
    socket.emit("unlock")
})


socket.on("showConsole", (stuff)=>{
    console.log(stuff)
  })