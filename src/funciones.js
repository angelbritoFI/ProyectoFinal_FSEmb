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
//Función para controlar el envío de acciones del sistema de irrigacion
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
		imagen = '<center><img src="Images/aspersor2.png" width = "150" height = "150" /></center>'
			document.getElementById('imagenIrrigacion').innerHTML = imagen;
		
	} else {
		notificacion.innerText = "Sistema de irrigación apagándose";
		imagen = '<center><img src="Images/aspersor1.png" width = "150" height = "150" /></center>'
			document.getElementById('imagenIrrigacion').innerHTML = imagen;
	}
}


//Función para validar el envío de números al programa de Python y mostra
function validaEnvio(funcion, etiqueta) {
	valor = document.getElementById(funcion).value;
	notifica = document.getElementById(etiqueta);
    if (valor < 0 && funcion != 'temperatura') {
    	alert("Debes de introducir un número positivo");
    } else {
    	if (isNaN(valor) || valor === "") {
  			alert("Debes de introducir un número");
		} else {
			if (valor > 100){
				valor = 100
			}
			else{
				valor  = valor
			}
			submit(funcion, valor);
			muestraImagenes(funcion, valor);
			notifica.innerText = valor
		}        
    }
}

//Muestra las imagenes correspondientes a la potencia del radiador
function muestraImagenes(funcion, valor){
	if (funcion == 'radiador'){
		if (valor<= 20){
			imagen = '<center><img src="Images/foco1.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenFoco').innerHTML = imagen;
		}
		else if (valor> 20 && valor<= 40){
			imagen = '<center><img src="Images/foco2.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenFoco').innerHTML = imagen;
		}
		else if (valor> 40 && valor<= 60){
			imagen = '<center><img src="Images/foco3.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenFoco').innerHTML = imagen;
		}
		else if (valor> 60 && valor<= 80){
			imagen = '<center><img src="Images/foco4.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenFoco').innerHTML = imagen;
		}
		else{
			imagen = '<center><img src="Images/foco5.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenFoco').innerHTML = imagen;
		}
	}
	
	else if (funcion == 'ventilador'){
		if (valor<= 33){
			imagen = '<center><img src="Images/ventilador1.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenVentilador').innerHTML = imagen;
		}
		else if (valor> 33 && valor<= 66){
			imagen = '<center><img src="Images/ventilador2.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenVentilador').innerHTML = imagen;
		}
		else{
			imagen = '<center><img src="Images/ventilador3.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenVentilador').innerHTML = imagen;
		}
	}
	else{
		imagen = '<center><img src="Images/foco1.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenFoco').innerHTML = imagen;
		imagen = '<center><img src="Images/ventilador1.png" width = "130" height = "130" /></center>'
	document.getElementById('imagenVentilador').innerHTML = imagen;

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
