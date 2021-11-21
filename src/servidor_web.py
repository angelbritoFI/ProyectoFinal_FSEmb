#!/usr/bin/env python3
# Authors:
# 	Brito Segura Angel
# 	Tovar Herrera Carlos Eduardo
#	Zazueta Barájas Sebastián Pedro
# License: MIT
# Version 1.1
# Date: 21/11/2021
# Description: Servidor web para control de invernadero
import os
import sys
import json
import magic
from http.server import BaseHTTPRequestHandler, HTTPServer

from invernadero import *

# Nombre o direccion IP del sistema anfitrion del servidor web
address = "localhost"
# address = "192.168.1.254"
# Puerto en el cual el servidor estara atendiendo solicitudes HTTP
# El default de un servidor web en produción debe ser 80
port = 8080

archivoHTML = "inicio.html"

#Heredando la clase para habilitar un servidor web sencillo
class WebServer(BaseHTTPRequestHandler):
	#Función para servir cualquier archivo encontrado en el servidor
	def _serve_file(self, rel_path):
		if not os.path.isfile(rel_path):
			self.send_error(404) #Si el archivo que se desea acceder no se encuentra
			return
		self.send_response(200)
		mime = magic.Magic(mime=True)
		#Para cada archivo se dene especificar su tipo en la cabecera
		if rel_path.find(".css"):
			self.send_header("Content-type", "text/css")
			self.end_headers()
		else:
			#Se proporciona el tipo mime del archivo en la cabecera
			self.send_header("Content-type", mime.from_file(rel_path))
			self.end_headers()
		with open(rel_path, 'rb') as file:
			self.wfile.write(file.read()) #Imprimir código HTML al socket

	#Función para controlar el JSON enviado por el usuario y hacer las acciones respectivas
	def _parse_post(self, json_obj):
		if not 'action' in json_obj or not 'value' in json_obj:
			print("Datos JSON incorrectos")
			return
		funciones = {
			'irrigacion' : irrigacion, 		#Sistema de Irrigación
			#'temperatura': temperatura,	#Control de temperatura
			#'radiador'	 : radiador, 		#Control de potencia del radiador
			#'ventilador' : ventilador		#Control de potencia del ventilador
		}
		accion = funciones.get(json_obj['action'], None)
		if accion:
			accion(json_obj['value'])

	#Función para desplegar el archivo de interfaz de usuario (página principal)
	def _serve_ui_file(self):
		if not os.path.isfile(archivoHTML):
			err = archivoHTML + " no encontrado"
			self.wfile.write(bytes(err, "utf-8"))
			print(err)
			return
		try:
			with open(archivoHTML, "r") as f:
				content = "\n".join(f.readlines())
		except:
			content = "Error leyendo "+ archivoHTML
		self.wfile.write(bytes(content, "utf-8")) #Devolver el código HTML como cadena binaria

	""" Función do_GET:
	Controla todas las solicitudes recibidas via GET, es decir, páginas HTML
	Por seguridad, no se analizan variables que lleguen por esta vía """
	def do_GET(self):
		# Si se accede a la raiz, se responde con la interfaz por defecto (incio.html)
		if self.path == '/': #variable con el directorio de trabajo
			self.send_response(200) #Código de respuesta satisfactorio (OK) de una solicitud
			""" La cabecera HTTP siempre debe contener el tipo de datos mime del contenido
				con el que responde el servidor """
			self.send_header("Content-type", "text/html")
			self.end_headers() # Fin de cabecera
			self._serve_ui_file() #Desplegar lo contenido en el HTML de la página principal
		else:
			# En caso contrario, se verifica que el archivo exista y se sirve
			self._serve_file(self.path[1:])

	""" Función do_POST:
	Controla todas las solicitudes recibidas via POST, es decir, envíos de formulario
	Recibe y procesa los datos para evitar inyección de código
	Gestiona los comandos para la Raspberry Pi a través de datos JSON 
	JSON para hacer llamadas asíncronas del cliente y sin respuesta por parte del servidor """
	def do_POST(self):
		# Primero se obtiene la longitud de la cadena de datos recibida
		content_length = int(self.headers.get('Content-Length'))
		if content_length < 1:
			#Si es menor a 1, no se recibió ninguna cadena
			return
		# Después se lee toda la cadena de datos
		post_data = self.rfile.read(content_length)
		# Finalmente, se decodifica el objeto JSON y se procesan los datos
		try:			
			#Interpretar los datos recibidos como cadenas de texto utf-8
			jobj = json.loads(post_data.decode("utf-8")) #Crear diccionario de Python
			self._parse_post(jobj)
		except:
			# Se descartan cadenas de datos mal formados
			print(sys.exc_info())
			print("Datos POST no recnocidos")
		
def main():
	# Inicializa una nueva instancia de HTTPServer con el HTTPRequestHandler definido
	webServer = HTTPServer((address, port), WebServer)
	print("Servidor iniciado")
	print ("\tAtendiendo solicitudes en http://{}:{}".format(address, port))
	try:
		# Mantiene al servidor web ejecutándose en segundo plano
		webServer.serve_forever()
	except KeyboardInterrupt:
		# Maneja la interrupción de cierre con CTRL+C
		pass
	except:
		print(sys.exc_info())
	# Detiene el servidor web cerrando todas las conexiones
	webServer.server_close()
	# Reporta parada del servidor web en consola
	print("\nServidor detenido.")

# Punto de anclaje de la función main
if __name__ == "__main__":
	main()
