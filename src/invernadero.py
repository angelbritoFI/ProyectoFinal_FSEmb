#!/usr/bin/env python3
# Authors:
# 	Brito Segura Angel
# 	Tovar Herrera Carlos Eduardo
#	Zazueta Barájas Sebastián Pedro
# License: MIT
# Version 1.0
# Date: 21/11/2021
# Description: Control de Invernadero

# Importación de la librería de control del GPIO de la Raspberry Pi
import RPi.GPIO as GPIO

#Configuraciones de la librería RPi.GPIO
GPIO.setwarnings(False) # Desactiviar advertencias
GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin

#Sistema de Irrigación
def irrigacion(estado):
	print("Sistema de irrigación", estado.upper())
	# salida = 'document.getElementById("prueba").innerHTML=%s;' % json_obj['action']

