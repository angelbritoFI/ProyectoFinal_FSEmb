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

#Parte gráfica del simulador
from tkinter import *

#Clase para crear ventana del simulador
class InterfazGrafica:
    def __init__(self):
        raiz = Tk() #Llamada a la ventana principal
        #Dimensiones de la ventana que se ubicará en el centro de la pantalla
        raiz.geometry('1000x500') # anchura x altura
        raiz.configure(bg = 'beige') #Color para el fondo de la ventana
        raiz.title('Simulador de Invernadero') #Título de la ventana
        # Construir y mostrar la ventana
        raiz.mainloop() #Queda a la espera de que alguna persona interactúe con la UI

#Configuraciones de la librería RPi.GPIO
GPIO.setwarnings(False) # Desactiviar advertencias
GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin

#Sistema de Irrigación
def irrigacion(estado):
	print("Sistema de irrigación", estado.upper())
	# salida = 'document.getElementById("prueba").innerHTML=%s;' % json_obj['action']

#Función para iniciar el simulador
def simulador():
	UI = InterfazGrafica()
	# Al presionar sobre el botón Cerrar 'X', el programa llegará a su fin
