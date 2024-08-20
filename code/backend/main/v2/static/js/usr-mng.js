// popup logic

// insert popup
document.getElementById('insert-popup').onclick = function () {
    document.querySelector('.popup-container-insert').style.display = "flex";
}
document.getElementById('close-popup-insert').onclick = function () {
    document.querySelector('.popup-container-insert').style.display = "none";
}

// update popup
const updatepopup = document.querySelector(".popup-container-update");
const insertpopup = document.getElementById('insert-popup');
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
    });
});

flashbuttons.forEach(button => {
    button.addEventListener("click", function () {
        document.querySelector('.flash-msg-div').style.display = "none";
    });
});

document.getElementById('close-popup-update').onclick = function () {
    document.querySelector('.popup-container-update').style.display = "none";
}
// When the user clicks anywhere outside of the popup, close it
window.addEventListener("click", function (event) {
    if (event.target === updatepopup) {
        updatepopup.style.display = "none";
    }
    // else if (event.target === insertpopup) {
    //     insertpopup.style.display = "none";
    // }
});
