/*!
* Start Bootstrap - Business Casual v7.0.9 (https://startbootstrap.com/theme/business-casual)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-casual/blob/master/LICENSE)
*/
// Highlights current date on contact page
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    menuToggle.classList.toggle("open");
});
//PRELOADER
window.addEventListener('load', function () {
    const preloader = document.getElementById('preloader');
    const mainContent = document.getElementById('main-content');

    // Asegura que todo el contenido esté completamente cargado antes de ocultar el preloader
    setTimeout(() => {
        // Oculta el preloader y muestra el contenido principal
        preloader.style.display = 'none';
        mainContent.style.display = 'block';

        // Comprueba si se debe mostrar el banner de cookies
        if (cookieBanner && !Cookielaw.getCookie('cookielaw_accepted')) {
            cookieBanner.style.display = 'block';
        }
    }, 700); // Puedes ajustar el retraso si es necesario
});
//FIN DE PRELOADER



//Loader
function mostrarLoader() {
    // Mostrar el loader
    document.getElementById("loader").style.display = "flex";
}

// Esperar a que el DOM esté listo
document.addEventListener("DOMContentLoaded", function () {
    // Verificar si hay mensajes o errores en el formulario y ocultar el loader si es necesario
    if (document.querySelector('.alert')) {
        document.getElementById("loader").style.display = "none";
    }
});


//VENTANA EMERGENTE CATEGORIAS MENSAJE
function mostrarModal(titulo, imgUrl) {
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalImg = document.getElementById('modal-img');

    modalTitle.textContent = titulo;
    modalImg.src = imgUrl;
    modal.style.display = 'flex';
}

function cerrarModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}

//CENTRO DE AYUDA
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contact-form"); // Formulario
    const modal = document.getElementById("thank-you-modal"); // Modal de agradecimiento
    const closeModalButton = document.getElementById("close-modal"); // Botón de cerrar el modal

    // Evento de envío del formulario
    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // Previene el comportamiento por defecto de recargar la página

        // Datos del formulario
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            // Envío de los datos al servidor usando fetch (AJAX)
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                // Si el mensaje fue enviado correctamente, muestra el modal
                modal.classList.add("active");

                // Limpia los campos del formulario
                form.reset();
            } else {
                console.error("Error al enviar el mensaje:", response.statusText);
                alert("Hubo un problema al enviar tu mensaje. Por favor, intenta nuevamente.");
            }
        } catch (error) {
            console.error("Error en la solicitud:", error);
            alert("Hubo un error inesperado. Por favor, intenta más tarde.");
        }
    });

    // Cierra el modal al hacer clic en el botón "OK"
    closeModalButton.addEventListener("click", () => {
        modal.classList.remove("active");
    });

    // Cierra el modal si el usuario hace clic fuera de la tarjeta del modal
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("active");
        }
    });
});





//ESTO ERA DE script.js
function confirmaAlert(pregunta, ruta) {
    jCustomConfirm(pregunta, 'Turbodiaz', 'Aceptar', 'Cancelar', function(r) {
        if (r) {
            window.location = ruta;
        }
    });
}

function alertAlert(mensaje) {
    jAlert(mensaje);
}
function validaCorreo(valor) {
 if (/^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i.test(valor)){
  return true;
 } else {
  return false;
 }
}
function agregarAlCarro()
{
   var form=document.agregar_al_carro;
   form.cantidad.value=document.getElementById('cantidad').value;
   form.submit();
}
function sendLogin()
{
   var form=document.form_login;
   if(form.correo.value==0)
   {
       alertAlert('El campo E-Mail es obligatorio');
       form.correo.value='';
       return false;
   }
   if(validaCorreo(form.correo.value)==false)
   {
       alertAlert('El E-Mail no es válido');
       form.correo.value='';
       return false;
   }
   if(form.password.value==0)
   {
       alertAlert('El campo Contraseña es obligatorio');
       form.password.value='';
       return false;
   }
   form.submit();
}

//REGISTRO LOGIN MENSAJES

// Función para validar si la contraseña cumple con los requisitos

function sendRegistro() {
    form = document.form_registro;
    if (form.nombre.value == 0) {
        alertAlert('El campo Nombre es obligatorio');
        form.nombre.value = '';
        return false;
    }
  
    if (form.apellido.value == 0) {
        alertAlert('El campo Apellido es obligatorio');
        form.apellido.value = '';
        return false;
    }

    if (form.telefono.value == 0) {
        alertAlert('El campo Teléfono es obligatorio');
        form.telefono.value = '';
        return false;
    }

    if (isNaN(form.telefono.value)) {
        alertAlert('El campo Teléfono solo debe contener números');
        form.telefono.value = '';
        return false;
    }

    if (form.correo.value == 0) {
        alertAlert('El campo E-Mail es obligatorio');
        form.correo.value = '';
        return false;
    }

    if (validaCorreo(form.correo.value) == false) {
        alertAlert('El E-Mail no es válido');
        form.correo.value = '';
        return false;
    }

    if (form.password.value == 0) {
        alertAlert('El campo Contraseña es obligatorio');
        form.password.value = '';
        return false;
    }

    if (form.password2.value == 0) {
        alertAlert('El campo Repetir Contraseña es obligatorio');
        form.password2.value = '';
        return false;
    }

    if (form.password.value != form.password2.value) {
        alertAlert('Las contraseñas ingresadas no coinciden');
        form.password.value = '';
        form.password2.value = '';
        return false;
    }
    form.submit();
}

document.addEventListener('DOMContentLoaded', function () {
    const passwordField = document.querySelector('[name="password"]');
    const passwordHelp = document.getElementById('password-help');

    // Expresión regular para validar la contraseña
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#*])[A-Za-z\d@$#*]{8,16}$/;

    passwordField.addEventListener('input', function () {
        if (passwordRegex.test(passwordField.value)) {
            passwordHelp.classList.add('valid');
            passwordHelp.classList.remove('invalid');
        } else {
            passwordHelp.classList.add('invalid');
            passwordHelp.classList.remove('valid');
        }
    });
});

function sendRestore()
{
   var form=document.form_restore;
   
   
   
   if(form.password1.value==0)
   {
       alertAlert('El campo Contraseña es obligatorio');
       form.password1.value='';
       return false;
   }
   if(form.password2.value==0)
   {
       alertAlert('El campo Repetir Contraseña es obligatorio');
       form.password2.value='';
       return false;
   }
   if(form.password1.value!=form.password2.value)
   {
       alertAlert('Las contraseñas ingresadas no coinciden');
       form.password1.value='';
       form.password2.value='';
       return false;
   }
   form.submit();
}
function sendReset()
{
   var form=document.form_reset;
   
   
   if(form.correo.value==0)
   {
       alertAlert('El campo E-Mail es obligatorio');
       form.correo.value='';
       return false;
   }
  
   form.submit();
}
function salir(ruta)
{
   jCustomConfirm('¿Realmente desea cerrar sesión?', 'Turbodiaz', 'Aceptar', 'Cancelar', function(r) {
        if (r) {
            window.location = ruta;
        }
    });
}
function modificarCantidadProductoCarro(id, cantidad)
{
   let ruta="/carro/modificar-cantidad-carro/"+id+"/"+cantidad;
   window.location=ruta;
}
function sendPago()
{
   let form=document.form_pagar;
   if(form.direccion.value==0)
   {
       alertAlert("Debes indicar la dirección del envío");
       return false;
   }
   if(form.indicaciones.value==0)
   {
       form.indicaciones.value="";
   }
   form.submit();
}



// Función para alternar el tipo de campo de contraseña y el ícono del ojo
function togglePassword(id, iconId) {
    var passwordField = document.getElementById(id);
    var icon = document.getElementById(iconId);
    if (passwordField.type === "password") {
        passwordField.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}

// Agregar los event listeners para los botones
document.getElementById('eye-password-actual').addEventListener('click', function() {
    togglePassword('id_password_actual', 'eye-icon-actual');
});

document.getElementById('eye-password1').addEventListener('click', function() {
    togglePassword('id_password1', 'eye-icon1');
});

document.getElementById('eye-password2').addEventListener('click', function() {
    togglePassword('id_password2', 'eye-icon2');
});


// DATOS usuario. ANIMACÍON
// Agregar animación al botón
document.addEventListener('DOMContentLoaded', () => {
    const btnActualizar = document.querySelector('.btn-actualizar');

    if (btnActualizar) {
        btnActualizar.addEventListener('mouseover', () => {
            btnActualizar.style.transform = 'scale(1.05)';
        });

        btnActualizar.addEventListener('mouseout', () => {
            btnActualizar.style.transform = 'scale(1)';
        });

        btnActualizar.addEventListener('click', () => {
            btnActualizar.classList.add('loading');
            setTimeout(() => {
                btnActualizar.classList.remove('loading');
            }, 1000);
        });
    }
});

