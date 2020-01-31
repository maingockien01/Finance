
var usernameInput = document.getElementById("username");
var passwordInput = document.getElementById("password");
var submitButton = document.getElementById("submit");
function isValid(){
    if (!usernameInput.value || !passwordInput.value || 0 === usernameInput.value || 0 === passwordInput.value) {
       submitButton.disabled = true;
    } else {
        submitButton.disabled = false;
    };
};

isValid();
passwordInput.addEventListener("input", isValid);
usernameInput.addEventListener("input", isValid);

