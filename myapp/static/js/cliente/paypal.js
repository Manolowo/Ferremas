document.addEventListener('DOMContentLoaded', function () {
    // Realizar solicitud a la API de divisas
    fetch('https://mindicador.cl/api')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Obtener el valor del dólar
            var valorDolar = data.dolar.valor;

            // Calcular el total del carrito en dólares
            var totalCarritoCLP = parseFloat(document.getElementById('totalCarrito').getAttribute('data-total'));
            var totalCarritoUSD = totalCarritoCLP / valorDolar;

            // Renderizar el botón de PayPal con el total del carrito en dólares
            renderPayPalButton(totalCarritoUSD);
        })
        .catch(function(error) {
            console.log('Error al obtener el valor del dólar:', error);
        });
});

function renderPayPalButton(totalCarritoUSD) {
    paypal.Buttons({
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: totalCarritoUSD.toFixed(2),
                        currency_code: 'USD'
                    }
                }]
            });
        },
        onApprove: function(data, actions) {
            return actions.order.capture().then(function(details) {
                alert('Transaction completed by ' + details.payer.name.given_name);
                // Redirigir a la vista para registrar el pedido después de la compra exitosa
                window.location.href = "/registrarPedido/";
            });
        }
    }).render('#paypal-button-container');
}

function limpiarCarrito() {
    console.log("Limpiando el carrito...");
    location.href = clearCartUrl;
}