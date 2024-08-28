// popup logic

// insert popup
document.getElementById('insert-popup').onclick = function () {
    document.querySelector('.popup-container-insert').style.display = "flex";
    document.querySelector('.main').classList.add("blur");

}
document.getElementById('close-popup-insert').onclick = function () {
    document.querySelector('.popup-container-insert').style.display = "none";
    document.querySelector('.main').classList.remove("blur");
}

// update popup
const updatepopup = document.querySelector(".popup-container-update");
const insertpopup = document.querySelector(".popup-container-insert");
const updatebuttons = document.querySelectorAll(".update-popup");
const flashbuttons = document.querySelectorAll(".close-flash");

// put data output
const fuid_input = document.getElementById("update-usr-id");

// Add click event listener to each button
updatebuttons.forEach(button => {
    button.addEventListener("click", function () {
        document.getElementById("input-uid").value = this.getAttribute("data-uid");
        document.getElementById("input-username").value = this.getAttribute("data-username");
        updatepopup.style.display = "flex";
        document.querySelector('.main').classList.add("blur");
    });
});

flashbuttons.forEach(button => {
    button.addEventListener("click", function () {
        document.querySelector('.flash-msg-div').style.display = "none";
    });
});

document.getElementById('close-popup-update').onclick = function () {
    document.querySelector('.popup-container-update').style.display = "none";
    document.querySelector('.main').classList.remove("blur");
}
// When the user clicks anywhere outside of the popup, close it
window.addEventListener("click", function (event) {
    if (event.target === updatepopup) {
        updatepopup.style.display = "none";
        document.querySelector('.main').classList.remove("blur");
    }
    else if (event.target === insertpopup) {
        insertpopup.style.display = "none";
        document.querySelector('.main').classList.remove("blur");
    }
});
