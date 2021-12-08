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
	graficaIrrigacion(estado)
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
			if (funcion == "temperatura"){
				graficaTemperatura(valor);
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
		graficaRadiador(valor);
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
		graficaVentilacion(valor)
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
	imagen = '<center><img src="Images/aspersor1.png" width = "150" height = "150" /></center>'
			document.getElementById('imagenIrrigacion').innerHTML = imagen;

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

etiquetasTemperatura = ["Inicial"]
datosTemperatura = [25]
//Funcion para crear grafica de temperatura
function graficaTemperatura(valor){
	var hoy = new Date();
	const $grafica = document.querySelector("#temp_grafica");
	// Las etiquetas son las que van en el eje X. 
	notifica = document.getElementById('estado_temperatura');
	notifica.innerText = valor 

	var horas = hoy.getHours() + ':' + hoy.getMinutes() + ':' + hoy.getSeconds();
	var dias = hoy.getDate() + '-' + ( hoy.getMonth() + 1 ) + '-' + hoy.getYear();
	horaCambio = horas + "  " +dias
	
	etiquetasTemperatura.push(horaCambio)
	datosTemperatura.push(valor)
	//Podemos tener varios conjuntos de datos. Comencemos con uno
	const datosTemp = {
		label: "Temperatura",
		data: datosTemperatura, // La data es un arreglo que debe tener la misma cantidad de valores que la cantidad de etiquetas
		backgroundColor: 'rgba(54, 162, 235, 0.2)', // Color de fondo
		borderColor: 'rgba(54, 162, 235, 1)', // Color del borde
		borderWidth: 1,// Ancho del borde
	};
	new Chart($grafica, {
		type: 'line',// Tipo de gráfica
		data: {
			labels: etiquetasTemperatura,
			datasets: [
				datosTemp,
				// Aquí más datos...
			]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero: true
					}
				}],
			},
		}
	});
}

etiquetasRadiador = ["Inicial"]
datosRadiador = [0]
//Funcion para crear grafica de radiador
function graficaRadiador(valor){
	var hoy = new Date();
	const $grafica = document.querySelector("#foco_grafica");

	var horas = hoy.getHours() + ':' + hoy.getMinutes() + ':' + hoy.getSeconds();
	var dias = hoy.getDate() + '-' + ( hoy.getMonth() + 1 ) + '-' + hoy.getYear();
	horaCambio = horas + "  " +dias
	
	etiquetasRadiador.push(horaCambio)
	datosRadiador.push(valor)

	const datosRad = {
		label: "Potencia Radiador",
		data: datosRadiador, // La data es un arreglo debe tener la misma cantidad de valores que la cantidad de etiquetas
		backgroundColor: 'rgba(154, 162, 235, 0.2)', // Color de fondo
		borderColor: 'rgba(154, 162, 235, 1)', // Color del borde
		borderWidth: 1,// Ancho del borde
	};
	new Chart($grafica, {
		type: 'line',// Tipo de gráfica
		data: {
			labels: etiquetasRadiador,
			datasets: [
				datosRad,
			]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero: true
					}
				}],
			},
		}
	});
}

//**GRAFICA PARA IRRIGACIÓN */
etiquetasIrrigacion = ["Inicial"]
datosIrrigacion  = [0]
//Funcion para crear grafica de irrigación
function graficaIrrigacion(valor){
	var hoy = new Date();
	const $grafica = document.querySelector("#irrig_grafica");
	if (valor == 'on'){
		datosIrrigacion.push(100);
	}
	else{
		datosIrrigacion.push(0);
	}
	
	var horas = hoy.getHours() + ':' + hoy.getMinutes() + ':' + hoy.getSeconds();
	var dias = hoy.getDate() + '-' + ( hoy.getMonth() + 1 ) + '-' + hoy.getYear();
	horaCambio = horas + "  " +dias
	
	etiquetasIrrigacion.push(horaCambio)

	const datosIrrg = {
		label: "Activacion de Irrigado",
		data: datosIrrigacion, // La data es un arreglo debe tener la misma cantidad de valores que la cantidad de etiquetas
		backgroundColor: 'rgba(100, 62, 135, 0.2)', // Color de fondo
		borderColor: 'rgba(100, 62, 135, 1)', // Color del borde
		borderWidth: 1,// Ancho del borde
	};
	new Chart($grafica, {
		type: 'bar',// Tipo de gráfica
		data: {
			labels: etiquetasIrrigacion,
			datasets: [
				datosIrrg,
			]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero: true
					}
				}],
			},
		}
	});
}

//**GRAFICA PARA ventilación */
etiquetasVentilacion = ["Inicial"]
datosVentilacion  = [0]
//Funcion para crear grafica de ventilación
function graficaVentilacion(valor){
	var hoy = new Date();
	const $grafica = document.querySelector("#vent_grafica");
	
	var horas = hoy.getHours() + ':' + hoy.getMinutes() + ':' + hoy.getSeconds();
	var dias = hoy.getDate() + '-' + ( hoy.getMonth() + 1 ) + '-' + hoy.getYear();
	horaCambio = horas + "  " +dias
	
	etiquetasVentilacion.push(horaCambio)
	datosVentilacion.push(valor)

	const datosVent = {
		label: "Potencia de ventilador",
		data: datosVentilacion, // La data es un arreglo debe tener la misma cantidad de valores que la cantidad de etiquetas
		backgroundColor: 'rgba(184, 12, 35, 0.2)', // Color de fondo
		borderColor: 'rgba(184, 12, 35, 1)', // Color del borde
		borderWidth: 1,// Ancho del borde
	};
	new Chart($grafica, {
		type: 'line',// Tipo de gráfica
		data: {
			labels: etiquetasVentilacion,
			datasets: [
				datosVent,
			]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero: true
					}
				}],
			},
		}
	});
}
