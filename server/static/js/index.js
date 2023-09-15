const socket = io()

socket.emit("identify", "browser")



document.getElementById("unlockImage").addEventListener("click", ()=>{
    socket.emit("unlock")
    changeLockUnlockImage(false)
    setTimeout(()=>{
        changeLockUnlockImage(true)
    }, 2000)
})


socket.on("showConsole", (stuff)=>{
    console.log(stuff)
    showStuff(stuff)
})

socket.on("doorUnlocked", ()=>{
    changeLockUnlockImage(false)
})

socket.on('updatePicture', ()=>{
    document.getElementById('housePicture').src = '../static/images/house.jpg'
})

function showStuff(message, colour="#ff0000"){
    const errorBox = document.createElement("div")
    errorBox.className = "errorBox"
    errorBox.innerHTML = `<h3 class="errorMsg">${message}</h3>`
    document.body.appendChild(errorBox)
    
    setTimeout(() => {
        errorBox.style.opacity = '0';
    }, 5000);
    errorBox.addEventListener('transitionend', () => errorBox.remove());
}

function changeLockUnlockImage(lock){
    //lock is a bool
    if (lock){
        document.getElementById("unlockImage").src = "../static/images/locked.png"
    }
    else{
        document.getElementById("unlockImage").src = "../static/images/unlocked.png"
    }

}