#!/usr/bin/env python3
# Authors:
# 	Brito Segura Angel
# 	Tovar Herrera Carlos Eduardo
#	Zazueta Barajas Sebastián Pedro
# License: MIT
# Version 1.7
# Date: 07/12/2021
# Description: Funciones para el control de Invernadero

# Importación de la librería de control del GPIO de la Raspberry Pi
#import RPi.GPIO as GPIO #Descomentar para una implementación física

#Importación del simulador (comentar para una implementación física)
from simula_Invernadero import *

import smbus2 	#Lectura del puerto serial I2C
import struct 	#Conversión de datos binarios a objetos que puede leer Python
from datetime import datetime	#Obtener fecha y hora actual del sistema

#Configuraciones de la librería RPi.GPIO (descomentar para implementación física)
#GPIO.setwarnings(False) # Desactiviar advertencias
#GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin
#GPIO.setup(29,GPIO.IN) #Sensor de humedad
#GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW) # Ventilador apagado
#GPIO.setup(37,GPIO.OUT, initial=GPIO.LOW) #Válvula de solenoide para riego apagada

#Configuraciones para control de potencia del ventilador
#pwm = GPIO.PWM(32, 1) #Inicializar pin 32 como PWM a una frecuencia de 1 Hz
#pwm.start(0) # Establecer ciclo de trabajo al 0% (apagado)

# Dirección del dispositivo I2C
SLAVE_ADDR = 0x0A #Dirección I2C del Arduino

# Inicializar el bus I2C instanciando al objeto SMBus
i2c = smbus2.SMBus(1) # Como parámetro se indica el número de dispositivo a controlar

#Declaración de variables globales
temp = 25 #Temperatura de inicio del invernadero
humedo = False #Humedad en el suelo del invernadero
tempA = 0
error_previo = 0
suma_errores = 0
tempC = 0

#Arreglos para almacenar las variables para el programado de ciclos
fecha_programada = []
horaInicio = []
horaTermino = []

#Constantes para controlador PID
KP = 0.02 	#Constante para control proporcional
KD = 0.01 	#Constante para control derivativo
KI = 0.005	#Constante para control integral

#Sistema de Irrigación
def irrigacion(estado):
	#Comentar las siguientes dos líneas para una implementación física
	quitaRiega()
	riega(estado)
	print("Sistema de irrigación", estado.upper())
	"""Descomentar para implementación física
	if estado == 'on':		
		GPIO.output(37, True) #Prender válvula con agua
	else:
		GPIO.output(37, False) #Apagar válvula con agua
	"""

#Controlador PID
def controlPID(tempObj):
	global temp, error_previo, suma_errores
	error = tempObj - temp #Cálculo del error (control proporcional)
	#Control proporcional, derivado e integral
	temp += (error * KP) + (error_previo * KD) + (suma_errores * KI)
	temp = max(min(150, temp), -55) #Valores mínimos y máximos del sensor LM35
	error_previo = error #Cálculo del error previo (control derivado)
	suma_errores += error #Sumatoria de errores (control integral)
	return int(temp)

#Control de temperatura por PID
def temperatura(num):
	global tempA
	tempA = temp
	print("Temperatura deseada por el usuario: ", num, "°C", sep="")
	#Repetir control PID hasta conseguir temperatura deseada
	while int(num) != tempA:
		tempA = temperaturaActual(controlPID(int(num)))
		print("Devuelta del invernadero por PID: ", tempA, "°C", sep="")

#Leer potencia en el esclavo (Arduino)
def leePotencia():
	try:
		#Generación del mensaje I2C de tipo lectura
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4) #Número de bytes que se leerán del esclavo
		i2c.i2c_rdwr(msg) #En este caso lectura en I2C
		data = list(msg) #Convertir el flujo de datos a una lista de Python
		""" Función unpack:
		Recibe un bytearray y un especificador de formato (interpreta los bytes en el arreglo
			para generar tupla de n elementos)
		Hace la codificación por defecto en I2C (<):
			little endian: codifica los bytes con el LSB a la izquierda
		"""
		potencia = struct.unpack('<f', ''.join([chr(c) for c in data]))		
	except:
		potencia = 0

	return potencia

#Escribir la potencia recibida al esclavo (Arduino)
def escribePotencia(potencia):
	try:
		""" Función pack:
		Recibe un bytearray y un especificador de formato para poder generar su tupla
		Se empaqueta la potencia recibida como un valor flotante (f)
		Hace la codificación por defecto en I2C (<):
			little endian: codifica los bytes con el LSB a la izquierda
		"""
		data = struct.pack('<f', potencia) 
		#Generación del mensaje I2C de tipo escritura
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
		i2c.i2c_rdwr(msg) #Escritura en el canal SDA
	except:
		#print("Sucedió un error en la escritura de potencia") #Descomentar para implementación física
		pass #Comentar para implementación física

#Control de potencia del radiador
def radiador(potencia):
	escribePotencia(potencia)
	#print("Potencia del radiador: ",leePotencia(), "%", sep="") #Descomentar para implementación física
	#Comentar las siguientes líneas para implementación física
	print("Potencia del radiador: ",potencia, "%", sep="")	
	quitaFoco()
	calienta(potencia)

#Control de potencia del ventilador
def ventilador(potencia):
	#pwm.ChangeDutyCycle(potencia) #Descomentar para implementación física
	print("Potencia del ventilador: ",potencia, "%", sep="")
	#Comentar las siguientes líneas para implementación física
	quitaVentilaAnt()
	ventila(potencia)

#Función para llamar al simulador creado (solo aplica para una implementación virtual)
def iniciaControl():
	simularInvernadero()

# Función para obtener los datos del usuario de la página web
def programaInvernadero(entrada):
	global tempC, fecha_programada, horaInicio, horaTermino
	datos = entrada.split(",") #Separar la cadena recibida por JSON
	tempC = float(datos[0]) #Convertir a flotante el número de temperatura

	fecha = datos[1].split("-") #Separar cada número que compone la fecha
	#Acomodar arreglo de cadenas a enteros
	for i in range(2,-1,-1):
		fecha_programada.append(int(fecha[i]))

	#Separación de cada número de las horas de inicio y fin del ciclo
	hora_inicio = datos[2].split(":")
	hora_fin = datos[3].split(":")
	#Acomodar arreglos de cadenas a enteros
	for i in range(2):
		horaInicio.append(int(hora_inicio[i]))
		horaTermino.append(int(hora_fin[i]))
	
#Resolución de 10 bits para el convertidor A/D
def leerTemperatura():
	global temp
	while True:
		try:
			#Generación del mensaje I2C de tipo lectura
			msg = smbus2.i2c_msg.read(SLAVE_ADDR, 2) #Número de bytes que se leerán del esclavo
			i2c.i2c_rdwr(msg) #En este caso lectura en I2C
			""" Función unpack:
			Recibe un bytearray y un especificador de formato (interpreta los bytes en el arreglo
				para generar tupla de n elementos)
			Tiene 2 tipos de lectura:
				- 1 byte (ADC de 8 bits): '<B'
				- 2 bytes (ADC de 10 bits): '<H' -unsigned half int-
			Hace la codificación por defecto en I2C:
				little endian: codifica los bytes con el LSB a la izquierda
			"""
			temp = struct.unpack('<H', msg.buf)[0]
			temp = temp * (5/10.24) #Conversión de valores discretos a °C con Vref = 5 [V]
			print("Temperatura leída del sensor: ", temp, "°C", sep="")
		except:
			print("Sucedió un error con el sensor de temperatura")

#Sensor de humedad sencillo
def registrarHumedad():
	global humedo #Variable para indicar si el suelo del invernadero está húmedo
	while True:
		if (GPIO.input(29)) == 0:
			humedo = True
		else:
			humedo = False

#Programado de ciclos de temperatura e irrigado
def ciclosTempIrr():
	global fecha_programada, horaInicio, horaTermino
	desactivado = True #Bandera para simulación, comentar y solo llamar a las funciones para implementación física
	tempI = 0
	irrigado = False #Bandera para implementación física
	while True:
		Ahora = datetime.now()
		#Programación de ciclos de temperatura e irrigado activado
		if len(fecha_programada) == 3:
			# ¿Es la fecha para hacer el ciclo?
			if (Ahora.day == fecha_programada[0] and Ahora.month == fecha_programada[1] and Ahora.year == fecha_programada[2]):
				#¿Es la hora para iniciarlo?
				if (Ahora.hour == horaInicio[0] and Ahora.minute == horaInicio[1]):
					irrigado = True
					if desactivado:
						print("Iniciando ciclo programado de temperatura e irrigado")
						tempI = temp
						temperatura(tempC)
						irrigacion('on')
						desactivado = False
				#¿Es la hora de terminar el irrigado?
				elif (Ahora.hour == horaTermino[0] and Ahora.minute == horaTermino[1]):
					irrigado = False
					if desactivado == False:
						print("Terminando ciclo programado de temperatura e irrigado")
						irrigacion('off')
						temperatura(tempI) #Regresando a valor de temperatura inicial
						desactivado = True
		"""Descomentar si es una implementación física
		#Comprobando que se mantenga temperatura e irrigado en el ciclo
		if irrigado:
			if tempC != temp:
				temperatura(tempC)
			elif humedo == False:
				#Suelo del invernadero seco
				irrigacion('on') #Activando el sistema de irrigación
		"""
