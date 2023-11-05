// JavaScript para mostrar y ocultar el modal
document.getElementById('save-outfit-button').addEventListener('click', function() {
   document.getElementById('save-outfit-modal').style.display = 'block';
});

document.querySelector('.close').addEventListener('click', function() {
   document.getElementById('save-outfit-modal').style.display = 'none';
});


// JavaScript para redirigir después de guardar el outfit
document.getElementById('save-outfit-form').addEventListener('submit', function(event) {
   event.preventDefault();

   // Envía el formulario a tu servidor para guardar el outfit en la base de datos.
   
   // Después de guardar el outfit, redirige al usuario a la página /closet_outfits/.
   window.location.href = '/closet_outfits/';
});
