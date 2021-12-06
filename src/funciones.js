/*
	Authors:
	 	Brito Segura Angel
	 	Tovar Herrera Carlos Eduardo
		Zazueta Barajas Sebastián Pedro
	License: MIT
	Version 1.0
	Date: 20/11/2021
	Description: Funciones para controlar el envío de datos
*/
function handle(sender, action, value){
	if (sender.id == 'irrigacionON' || sender.id == 'irrigacionOFF')	
		irrigacion(action, value);
	else {
		validaEnvio(action, value);
	}
}

function irrigacion(funcion, estado) {
	submit(funcion, estado);
	notificacion = document.getElementById("sistema_irr");
	if (estado == 'on') {
		notificacion.innerText = "Sistema de irrigación enciendose";
		imagen = '<img src="Images/aspersor2.png" alt="cargando..." />'
			document.getElementById('imagenIrrigacion').innerHTML = imagen;
		
	} else {
		notificacion.innerText = "Sistema de irrigación apagándose";
		imagen = '<img src="Images/aspersor1.png" alt="cargando..." />'
			document.getElementById('imagenIrrigacion').innerHTML = imagen;
	}
}

function validaEnvio(funcion, etiqueta) {
	valor = document.getElementById(funcion).value;
	notifica = document.getElementById(etiqueta);
    if (valor < 0) {
    	alert("Debes de introducir un número positivo");
    } else {
    	if (isNaN(valor) || valor === "") {
  			alert("Debes de introducir un número");
		} else {
			submit(funcion, valor);
			notifica.innerText = valor
		}        
    }
}

function submit(action, value){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", window.location.href, true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify({
		'action' : action,
		'value' :  value,
	}));
}
