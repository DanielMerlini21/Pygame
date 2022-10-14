let blocks_names = ["block_1", "block_2", "block_3", "block_4", "block_5", "block_6"];
let pick = blocks_names[Math.floor((Math.random()*6))];
let findRgb = 0

function randomRgbColor(){
    let color = [
        Math.floor((Math.random()*250)+1),
        Math.floor((Math.random()*250)+1),
        Math.floor((Math.random()*250)+1)
    ];

    return "rgb(" + color.toString() + ")"
 }

blocks_names.forEach(setUpBlocks)

function setUpBlocks(value) {
    let x = randomRgbColor();
    document.getElementById(value).style.backgroundColor = x;
    document.getElementById(value).style.color = x;
    if (value === pick) {
        findRgb = x
    }

}

document.getElementById("rgb_find").innerText = findRgb;

function check(id) {
    if (id.innerHTML.toString() === pick) {
        document.getElementById("displayWin").innerText = "Well Done!";
        blocks_names.forEach(endGame)
    } else {
        document.getElementById("displayWin").innerText = "Wrong!";
        id.style.backgroundColor = "black";
        id.style.color = "black";
    }
}

function resetColors() {
    pick = blocks_names[Math.floor((Math.random()*6))];
    blocks_names.forEach(setUpBlocks)
    document.getElementById("displayWin").innerText = "";
    document.getElementById("rgb_find").innerText = findRgb;
}

function endGame (value) {
    document.getElementById(value).style.backgroundColor = findRgb;
    document.getElementById(value).style.color = findRgb;
}