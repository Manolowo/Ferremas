// loginmodal.js

// Obtener los modales
var loginModal = document.getElementById('loginModal');
var registerModal = document.getElementById('registerModal');

// Obtener el botón que abre el modal de inicio de sesión
var loginBtn = document.getElementById('openLoginModal');

// Obtener el enlace que abre el modal de registro
var registerLink = document.getElementById('openRegisterModal');

// Obtener los elementos <span> que cierran los modales
var closeLoginModal = document.getElementById('closeLoginModal');
var closeRegisterModal = document.getElementById('closeRegisterModal');

// Cuando el usuario hace clic en el botón, abre el modal de inicio de sesión
loginBtn.onclick = function() {
    loginModal.style.display = "block";
}

// Cuando el usuario hace clic en el enlace de registro, abre el modal de registro y cierra el modal de inicio de sesión
registerLink.onclick = function() {
    loginModal.style.display = "none";
    registerModal.style.display = "block";
}

// Cuando el usuario hace clic en <span> (x), cierra el modal de inicio de sesión
closeLoginModal.onclick = function() {
    loginModal.style.display = "none";
}

// Cuando el usuario hace clic en <span> (x), cierra el modal de registro
closeRegisterModal.onclick = function() {
    registerModal.style.display = "none";
}

// Cuando el usuario hace clic en cualquier lugar fuera del modal, cierra el modal
window.onclick = function(event) {
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    }
    if (event.target == registerModal) {
        registerModal.style.display = "none";
    }
}
