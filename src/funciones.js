/*
	Authors:
	 	Brito Segura Angel
	 	Tovar Herrera Carlos Eduardo
		Zazueta Barájas Sebastián Pedro
	License: MIT
	Version 1.0
	Date: 20/11/2021
	Description: Funciones para controlar el envío de datos
*/
function handle(sender, action, value){
	submit(action, value);
	if (value == 'on')
		alert("Sistema de irrigación encendiendo");
	else
		alert("Sistema de irrigación apagándose");
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
