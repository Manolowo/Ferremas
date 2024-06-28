fetch('https://mindicador.cl/api').then(function(response) {
    return response.json();
}).then(function(dailyIndicators) {
    document.getElementById("UF").innerHTML = 'UF  : $' + dailyIndicators.uf.valor;
    document.getElementById("DolarO").innerHTML = 'DOLAR : $' + dailyIndicators.dolar.valor;
    document.getElementById("Euro").innerHTML = 'EURO  : $' + dailyIndicators.euro.valor;
    document.getElementById("IPC").innerHTML = ' IPC  : ' + dailyIndicators.ipc.valor;
    document.getElementById("UTM").innerHTML = ' UTM : $' + dailyIndicators.utm.valor;
    document.getElementById("IVP").innerHTML = ' IVP  : $' + dailyIndicators.ivp.valor;
    document.getElementById("Imacec").innerHTML = ' Imacec  : ' + dailyIndicators.imacec.valor;
}).catch(function(error) {
    console.log('Requestfailed', error);
});
