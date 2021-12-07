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
//Función para controlar el envío de acciones al programa de Python
function handle(sender, action, value){
	if (sender.id == 'irrigacionON' || sender.id == 'irrigacionOFF')	
		irrigacion(action, value);
	else {
		validaEnvio(action, value);
	}
}

//Control del sistema de Irrigación
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

//Función para validar el envío de números al programa de Python
function validaEnvio(funcion, etiqueta) {
	valor = document.getElementById(funcion).value;
	notifica = document.getElementById(etiqueta);
    if (valor < 0 && funcion != 'temperatura') {
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

//Función para programar ciclos de temperatura e irrigado
function ciclosTempIrr(funcion) {
	temperatura = document.getElementById('tempProg').value;
	fecha = document.getElementById('fecha').value;
	iniciar = document.getElementById('t_inicio').value;
	terminar = document.getElementById('t_fin').value;
	notifica = document.getElementById('programado');
	if (isNaN(temperatura) || temperatura === "") {
  		alert("Debes de introducir un número");
	} else if (fecha === "" || iniciar === "" || terminar === "") {
		alert("Introduce todos los campos solicitados");
	} else {
		var valor = temperatura + "," + fecha + "," + iniciar + "," + terminar
		notifica.innerText = "Ciclo de temperatura e irrigado programado para " + fecha 
			+ " desde " + iniciar + " hasta " + terminar
		submit(funcion, valor);
	}
}

//Enviar los datos con el método POST al programa de Python
function submit(action, value){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", window.location.href, true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify({
		'action' : action,
		'value' :  value,
	}));
}
