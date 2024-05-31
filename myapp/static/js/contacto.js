document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir que el formulario se envíe
    
    var email = document.getElementById('email').value;
    
    alert("Nos pondremos en contacto contigo.");
});
