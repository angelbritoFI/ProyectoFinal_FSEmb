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
#import RPi.GPIO as GPIO


#Parte gráfica del simulador
from tkinter import *

#Clase para crear ventana del simulador
class InterfazGrafica():
    def __init__(self, irrigacion = 0, temperatura = 20, ventilador = 50):
        self._irrigacion = irrigacion
        self._temperatura = temperatura
        self._ventilador = ventilador

        self.gui = Tk() #Llamada a la ventana principal
        #Dimensiones de la ventana que se ubicará en el centro de la pantalla
        self.gui.geometry('1000x500') # anchura x altura
        self.gui.configure(bg = 'beige') #Color para el fondo de la ventana
        self.gui.title('Simulador de Invernadero') #Título de la ventana
        # Construir y mostrar la ventana
        self._inicializar()

        self.gui.mainloop() #Queda a la espera de que alguna persona interactúe con la UI


    def _inicializar(self):

        self.strLineV = StringVar(self.gui)
        self.strLineF = StringVar(self.gui)
        self.strDataR = StringVar(self.gui)
        self.strPhase = StringVar(self.gui)
        self.strPower = StringVar(self.gui)

        # Validators
        self.lblLineV = Label(self.gui, anchor="w",
            bg="blue", fg="white",
            text="Sistema de Irrigacion:")

        self.lblLineF = Label(self.gui, anchor="w",
            bg="blue", fg="white",
            text="Temperatura:")

        self.lblDataR = Label(self.gui, anchor="w",
            bg="blue", fg="white",
            text="Ventilacion:")


       
        self.lblLineV.grid(row=0, column=0, sticky="w", padx=20, pady=40)
        
        self.lblLineF.grid(row=1, column=0, sticky="w", padx=20, pady=80)
        
        self.lblDataR.grid(row=2, column=0, sticky="w", padx=20, pady=80)
        

        # self.lblLampI.grid(row=0, column=2, sticky="w", padx=75, pady=2,
        #                     columnspan=2, rowspan=5)



        

#Configuraciones de la librería RPi.GPIO
#GPIO.setwarnings(False) # Desactiviar advertencias
#GPIO.setmode(GPIO.BOARD) # Usar el número físico de pin

#Sistema de Irrigación
def irrigacion(estado):
	print("Sistema de irrigación", estado.upper())
	# salida = 'document.getElementById("prueba").innerHTML=%s;' % json_obj['action']

#Función para iniciar el simulador
def simulador():
	UI = InterfazGrafica()
	# Al presionar sobre el botón Cerrar 'X', el programa llegará a su fin

InterfazGrafica()