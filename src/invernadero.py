#!/usr/bin/env python3
# Authors:
# 	Brito Segura Angel
# 	Tovar Herrera Carlos Eduardo
#	Zazueta Barajas Sebastián Pedro
# License: MIT
# Version 1.0
# Date: 21/11/2021
# Description: Control de Invernadero

# Importación de la librería de control del GPIO de la Raspberry Pi
#import RPi.GPIO as GPIO #Descomentar para una implementación física

#Importación del simulador
from simula_Invernadero import *

from threading import Thread

import smbus2 #Lectura del puerto serial I2C
import struct #Conversión de datos binarios a objetos que puede leer Python

#Configuraciones de la librería RPi.GPIO (descomentar para implementación física)
#GPIO.setwarnings(False) # Desactiviar advertencias
#GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin
#GPIO.setup(29,GPIO.IN) #Sensor de humedad
#GPIO.setup(37,GPIO.OUT) #Válvula de solenoide para riego

# Dirección del dispositivo I2C
SLAVE_ADDR = 0x0A # Dirección I2C del Arduino

# Inicializar el bus I2C instanciando al objeto SMBus
# Como parámetro se indica el número de dispositivo a controlar
i2c = smbus2.SMBus(1)

temp = 25 #Temperatura de inicio del invernadero
humedo = False #Humedad del huerto

#Sistema de Irrigación
def irrigacion(estado):
	#apagaEtiqueta()
	quitaRiega()
	riega(estado)
	print("Sistema de irrigación", estado.upper())
	"""Descomentar para implementación física
	if estado == 'on':		
		GPIO.output(37, True) #Prender válvula con agua
	else:
		GPIO.output(37, False) #Apagar válvula con agua
	"""

def temperatura(num):
	print("Temperatura cambiada a: ", num, "°C", sep="")
	print("Devuelta del invernadero:", temperaturaActual())

def radiador(potencia):
	print("Potencia del radiador: ",potencia, "%", sep="")
	quitaFoco()
	calienta(potencia)

def ventilador(potencia):
	print("Potencia del ventilador: ",potencia, "%", sep="")
	quitaVentilaAnt()
	hiloVent = Thread(target = ventila, args=(potencia,))
	hiloVent.start()

def mostrarGrafica(valor):
	print("Imprimiendo gráfica")

def iniciaControl():
	simularInvernadero()

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
