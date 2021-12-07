#!/usr/bin/env python3
# Authors:
# 	Brito Segura Angel
# 	Tovar Herrera Carlos Eduardo
#	Zazueta Barajas Sebastián Pedro
# License: MIT
# Version 1.6
# Date: 06/12/2021
# Description: Control de Invernadero

# Importación de la librería de control del GPIO de la Raspberry Pi
#import RPi.GPIO as GPIO #Descomentar para una implementación física

#Importación del simulador (comentar para una implementación física)
from simula_Invernadero import *

#Control de hilos para el simulador (comentar para una implementación física)
from threading import Thread

import smbus2 	#Lectura del puerto serial I2C
import struct 	#Conversión de datos binarios a objetos que puede leer Python
import time 	#Medición de tiempos

#Configuraciones de la librería RPi.GPIO (descomentar para implementación física)
#GPIO.setwarnings(False) # Desactiviar advertencias
#GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin
#GPIO.setup(29,GPIO.IN) #Sensor de humedad
#GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW) # Ventilador
#GPIO.setup(37,GPIO.OUT, initial=GPIO.LOW) #Válvula de solenoide para riego apagada

#Configuraciones para control de potencia del ventilador
#pwm = GPIO.PWM(32, 1) #Inicializar pin 32 como PWM a una frecuencia de 1 Hz
#pwm.start(0) # Establecer ciclo de trabajo al 0% (apagado)

# Dirección del dispositivo I2C
SLAVE_ADDR = 0x0A # Dirección I2C del Arduino

# Inicializar el bus I2C instanciando al objeto SMBus
# Como parámetro se indica el número de dispositivo a controlar
i2c = smbus2.SMBus(1)

temp = 25 #Temperatura de inicio del invernadero
humedo = False #Humedad del huerto
tempA = 0

automatico = False #Inicia sin programación de ciclos de temperatura e irrigado el programa

#Constantes para controlador PID
KP = 0.02 	#Constante para control proporcional
KD = 0.01 	#Constante para control derivativo
KI = 0.005	#Constante para control integral

error_previo = 0
suma_errores = 0

#Sistema de Irrigación
def irrigacion(estado):
	#apagaEtiqueta()
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
	error = tempObj - temp
	#Control proporcional, derivado e integral
	temp += (error * KP) + (error_previo * KD) + (suma_errores * KI)
	temp = max(min(150, temp), -55) #Valores mínimos y máximos del sensor LM35
	error_previo = error
	suma_errores += error
	return int(temp)

#Control de temperatura
def temperatura(num):
	global tempA
	print("Temperatura deseada por el usuario: ", num, "°C", sep="")
	while int(num) != tempA:
		tempA = temperaturaActual(controlPID(int(num)))
		print("Devuelta del invernadero por PID: ", tempA, "°C", sep="")

#Leer potencia en el esclavo (Arduino)
def leePotencia():
	try:
		#Generación del mensaje I2C de tipo lectura
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4) #Número de bytes que se leerán del esclavo
		i2c.i2c_rdwr(msg) #En este caso lectura en I2C (escritura en el canal SDA)		
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
		#Generación del mensaje I2C de tipo lectura
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data) #Número de bytes que se leerán del esclavo
		i2c.i2c_rdwr(msg) #En este caso lectura en I2C (escritura en el canal SDA)
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
	hiloVent = Thread(target = ventila, args=(potencia,))
	hiloVent.start()

def mostrarGrafica(valor):
	print("Imprimiendo gráfica")

def iniciaControl():
	simularInvernadero()

#Programado de ciclos de temperatura e irrigado
def programaInvernadero(entrada):
	automatico = True
	#0,2021-12-08,00:03,12:00

#Resolución de 10 bits para el convertidor A/D
def leerTemperatura():
	global temp
	while True:
		try:
			#Generación del mensaje I2C de tipo lectura
			msg = smbus2.i2c_msg.read(SLAVE_ADDR, 2) #Número de bytes que se leerán del esclavo
			i2c.i2c_rdwr(msg) #En este caso lectura en I2C (escritura en el canal SDA)		
			data = list(msg)
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
			print("Temperatura leida del sensor: ", temp, "°C", sep="")
		except:
			print("Sucedió un error con el sensor de temperatura")

#Sensor de humedad sencillo
def registrarHumedad():
	global humedo
	while True:
		if (GPIO.input(29)) == 0:
			humedo = True
		else:
			humedo = False
