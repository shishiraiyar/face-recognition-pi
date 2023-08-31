const socket = io()

socket.emit("identify", "browser")





document.getElementById("unlockButton").addEventListener("click", ()=>{
    socket.emit("unlock")
})


socket.on("showConsole", (stuff)=>{
    console.log(stuff)
    showStuff(stuff)
  })

function showStuff(message, colour="#ff0000"){
    const errorBox = document.createElement("div")
    errorBox.className = "errorBox"
    errorBox.innerHTML = `<h3 class="errorMsg">${message}</h3>`
    document.body.appendChild(errorBox)
    
    setTimeout(() => {
        // errorBox.remove();
        errorBox.style.opacity = '0';
    }, 5000);
    errorBox.addEventListener('transitionend', () => errorBox.remove());
}
