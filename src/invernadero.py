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
import RPi.GPIO as GPIO

#Importación del simulador
from simula_Invernadero import *

from threading import Thread

#Configuraciones de la librería RPi.GPIO
#GPIO.setwarnings(False) # Desactiviar advertencias
#GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin

#Sistema de Irrigación
def irrigacion(estado):
	print("Sistema de irrigación", estado.upper())
	# salida = 'document.getElementById("prueba").innerHTML=%s;' % json_obj['action']
	#apagaEtiqueta()
	quitaRiega()
	riega(estado)
	print("El estado de irrigacion: ")
	print(estado)

def temperatura(num):
	print("Temperatura cambiada a: ", num, "°C", sep="")
	print("Devuelta:")
	print(temperaturaActual())


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