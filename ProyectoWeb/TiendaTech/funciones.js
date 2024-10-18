
console.log("Archivo de validaciones cargado correctamente.");


// Función para validar campos de texto
function validateTextInput(event) {
    const input = event.target;
    const value = input.value;
    const regex = /\d/;

    if (regex.test(value)) {
        alert("No se permiten números en este campo.");
        input.value = value.replace(regex, '');
    }
}

// Función para validar campos de número
function validateNumberInput(event) {
    const input = event.target;
    const value = input.value;
    const regex = /[^\d]/;

    if (regex.test(value)) {
        alert("Solo se permiten números en este campo.");
        input.value = value.replace(regex, '');
    }
}

// Función para validar el correo electrónico
function validateEmailInput(event) {
    const input = event.target;
    const value = input.value;
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!regex.test(value)) {
        alert("Por favor, introduce un correo electrónico válido.");
    }
}

// Función para validar que no haya campos vacíos y aplicar otras validaciones antes de enviar el formulario
function validateForm(event) {
    event.preventDefault(); // Prevenir el envío del formulario para validaciones

    const form = document.getElementById('contactForm');
    const name = form.nombre.value.trim();
    const lastName = form.apellido.value.trim();
    const email = form.correo.value.trim();
    const phone = form.telefono.value.trim();
    const message = form.textarea.value.trim();
    

    if (!name || !lastName || !email || !phone || !message) {
        alert("Todos los campos deben ser completados.");
        return false;
    }

    // Validar el correo electrónico
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert("Por favor, introduce un correo electrónico válido.");
        return false;
    }

    // Si todas las validaciones pasan, se puede enviar el formulario
    alert("Formulario enviado exitosamente.");
    form.submit();
}

// Funciones de validación para el formulario "Trabaja con Nosotros"
function validateJobForm(event) {
    event.preventDefault(); // Prevenir el envío del formulario para validaciones

    const form = document.getElementById('jobForm');
    const name = form.nombre.value.trim();
    const lastName = form.apellido.value.trim();
    const email = form.correo.value.trim();
    const phone = form.telefono.value.trim();
    const file = form.detalle.files[0]; // Obtener el archivo adjunto

    // Validar campos
    if (!name || !lastName || !email || !phone || !file) {
        alert("Todos los campos deben ser completados.");
        return false;
    }

    // Validar el correo electrónico
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert("Por favor, introduce un correo electrónico válido.");
        return false;
    }

    // Si todas las validaciones pasan, se puede enviar el formulario
    alert("Formulario 'Trabaja con Nosotros' enviado exitosamente.");
    form.submit();
}