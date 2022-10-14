//Reminder : make numbers go right to left

let onScreen;
let answer = 0;
let screen = document.getElementById("screen");
let showOnce = false;


function displayButton(id){
    let content = id.innerHTML;
    if (content === "=") {
        screen.innerText = eval(onScreen);
        showOnce = true;
    } else if (content === "C") {
        screen.innerText = "";
        answer = 0;
    } else {
        if (showOnce === true) {
            if (isNaN(content)) {
                showOnce = false;
            } else {
                screen.innerText = "";
                showOnce = false;
            }
        }
        onScreen = screen.innerHTML;
        onScreen += content;
        screen.innerText = onScreen;
    }
}

document.addEventListener("keyup", function(event) {
    if (event.keyCode === 8) {
        onScreen = onScreen.slice(0, -1);
        screen.innerText = onScreen;
    }
});