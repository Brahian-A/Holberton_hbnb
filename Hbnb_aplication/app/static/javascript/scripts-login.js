document.addEventListener("DOMContentLoaded", function() {
    const activadorCheckbox = document.getElementById("activador");
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");

    function changeVisibility(){
        if (activadorCheckbox.checked){
            registerForm.classList.add('form-active');
            loginForm.classList.remove('form-active');
        } else {
            registerForm.classList.remove('form-active');
            loginForm.classList.add('form-active');
        }
    }
    activadorCheckbox.checked = false;
    changeVisibility();

    activadorCheckbox.addEventListener('change', changeVisibility);

});