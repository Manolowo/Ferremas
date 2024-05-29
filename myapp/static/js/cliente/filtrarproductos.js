// static/js/filtrarProductos.js

function filtrarProductos() {
    // Obtener el valor del input de búsqueda
    var input = document.getElementById('searchInput');
    var filter = input.value.toLowerCase();
    
    // Obtener el contenedor de productos
    var productosContainer = document.getElementById('productos-section');
    
    // Obtener todas las tarjetas de productos
    var productos = productosContainer.getElementsByClassName('productos-card');
    
    // Recorrer todas las tarjetas y ocultar las que no coincidan con la búsqueda
    for (var i = 0; i < productos.length; i++) {
        var nombre = productos[i].getElementsByClassName('card-header')[0].getElementsByTagName('h5')[0];
        if (nombre.innerHTML.toLowerCase().indexOf(filter) > -1) {
            productos[i].style.display = '';
        } else {
            productos[i].style.display = 'none';
        }
    }
}
