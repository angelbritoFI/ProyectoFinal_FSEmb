#!/usr/bin/env python3
# Authors:
# 	Brito Segura Angel
# 	Tovar Herrera Carlos Eduardo
#	Zazueta Barajas Sebastián Pedro
# License: MIT
# Version 1.2
# Date: 06/12/2021
# Description: Simulador de Invernadero

#Parte gráfica del simulador
from tkinter import *
from PIL import ImageTk, Image

#Para manejar animaciones 
from threading import Thread
#Para el apoyo de las animaciones
from time import sleep

""" Simulador de un invernadero, este simulador nos mostrará los componentes que se activan desactivan, dependiendo de 
las acciones realizadas por el servidor web/invernadero, el cual puede ser reemplazado por la implementación física
siendo este simulador, solamente eso, un simulador visual de dicha implementación

"""

#Ventana principal
raiz = None
fondo = 'light sky blue'

#Ventilador 
activa_Vent = False  #Variable para control de animación
imgActual_Vent = 0   #Variable para reanudar animación
imgVent = None       #Para asignar imagen
lblVent_Img = None   #A esta etiqueta se le asignará la imagen
lblPot_Vent = None   #Etiqueta que muestra la potencia actual del ventilador
lblOnOff_Vent = None #Etiqueta que muestra si el ventilador esta prendido o apagado

#Aspersor
imgAsp = None       #Para asignar imagen
lblAsp_Img = None   #A esta etiqueta se le asignará la imagen
lblOnOff_Asp = None #Etiqueta que muestra si se está regando o no

#Termometro
temperatura = "25"  #Variable para obtener/mostrar la temperatura actual
lblTemp = None      #Etiqueta que muestra la temperatura actual (Se puede ver el valor en el slider también)
imgTerm = None      #Para asignar imagen
lblTerm_Img = None  #Etiqueta a la que se le asignará la imagen

#Foco 
imgFoco = None         #Para asignar imagen
lblFoco_Img = None     #Etiqueta a la que se le asignará la imagen
lblPot_Foco = None     #Etiqueta que muestra la potencia actual del foco
lblOnOff_Foco = None   #Etiqueta que muestra si está encendido o apagado
imgActual_Foco = 0     #Variable para cambios de la imagen       

#Función para iniciar el simulador
def simularInvernadero():
    #Estas variables se definen como globales para evitar crear "múltiples" elementos
    global raiz, fondo
    #Ventilador
    global imgVent, lblVent_Img, lblPot_Vent, lblOnOff_Vent
    #Aspersor
    global imgAsp, lblAsp_Img, lblOnOff_Asp
    #Termometro
    global lblTemp, temperatura, lblTerm_Img, imgTerm
    #Foco
    global imgFoco, lblFoco_Img, lblPot_Foco, lblOnOff_Foco

    #Definición de la ventana principal
    raiz = Tk() #Ventana principal
    raiz.geometry('600x700') #Dimensiones
    raiz.configure(bg = fondo) #Color de fondo
    raiz.title('Invernadero Simulado') #Título
	# Al presionar sobre el botón Cerrar 'X', el programa llegará a su fin (Hilo del simulador)

    #Espacios vacíos para ordenar la ventana
    vacio1 = Label(raiz)
    vacio1.configure(bg = fondo)
    vacio1.grid(row = 0, column = 0)
    vacio1["text"]="      "

    vacio2 = Label(raiz)
    vacio2.configure(bg = fondo)
    vacio2.grid(row = 0, column = 2)
    vacio2["text"]="      "

    vacio3 = Label(raiz)
    vacio3.configure(bg = fondo)
    vacio3.grid(row = 0, column = 4)
    vacio3["text"]="      "

    vacio4 = Label(raiz)
    vacio4.configure(bg = fondo)
    vacio4.grid(row = 4, column = 0)
    vacio4["text"]="      "

    vacio5 = Label(raiz)
    vacio5.configure(bg = fondo)
    vacio5.grid(row = 8, column = 0)
    vacio5["text"]="      "

    #Ventilador
    #Variables: imgVent, lblVent_Img, lblPot_Vent, lblOnOff_Vent
    #Imagen
    imgVent = ImageTk.PhotoImage(Image.open("Images/ventilador1.png"))
    lblVent_Img = Label(raiz, image = imgVent)
    lblVent_Img.configure(bg=fondo)
    lblVent_Img.grid(row = 1, column = 1)

    #Potencia
    lblPot_Vent = Label(raiz)
    lblPot_Vent.grid(row = 2, column = 1)
    lblPot_Vent["text"] = "0%"

    #On/Off
    lblOnOff_Vent = Label(raiz)
    lblOnOff_Vent.grid(row = 3, column = 1)
    lblOnOff_Vent["text"] = "Off"

    ############
    #Foco
    #Variables: imgFoco, lblFoco_Img, lblPot_Foco, lblOnOff_Foco
    #Imagen
    imgFoco = ImageTk.PhotoImage(Image.open("Images/foco1.png"))
    lblFoco_Img = Label(raiz, image = imgFoco)
    lblFoco_Img.configure(bg=fondo)
    lblFoco_Img.grid(row = 1, column = 3)
    
    #Potencia
    lblPot_Foco = Label(raiz)
    lblPot_Foco.grid(row = 2, column = 3)
    lblPot_Foco["text"] = "0 %"

    #ON/OFF
    lblOnOff_Foco = Label(raiz)
    lblOnOff_Foco.grid(row = 3, column = 3)
    lblOnOff_Foco["text"] = "Off"

    ##########################
    #Aspersor
    #Variables: imgAsp, lblAsp_Img, lblOnOff_Asp
    #Imagen
    imgAsp = ImageTk.PhotoImage(Image.open("Images/aspersor1.png"))
    lblAsp_Img = Label(raiz, image = imgAsp)
    lblAsp_Img.configure(bg = fondo)
    lblAsp_Img.grid(row = 5, column = 1)

    #ON/OFF
    lblOnOff_Asp = Label(raiz)
    lblOnOff_Asp.grid(row = 6, column = 1)
    lblOnOff_Asp["text"] = "Off"

    ##########################
    #Termometro
    #Variables: imgTerm, lblTerm_Img, lblTemp
    #Imagen
    imgTerm = ImageTk.PhotoImage(Image.open("Images/term1.png"))
    lblTerm_Img = Label(raiz, image = imgTerm)
    lblTerm_Img.configure(bg = fondo)
    lblTerm_Img.grid(row = 5, column = 3)
    
    #Temperatura
    lblTemp = Label(raiz)
    lblTemp.grid(row = 6, column = 3)
    lblTemp["text"] = "0°C"

    #Slider (Cambiar la temperatura medida)
    sliderTemp = Scale(raiz, from_=-10, to=50, orient='horizontal', command = slider_changed)
    sliderTemp.set(25)
    sliderTemp.grid(row = 7, column = 3)
    ##########################

    raiz.mainloop()

#Permite actualizar el valor "medido" por el termometro
#Realmente se coloca el valor directamente de ahí
def slider_changed(value):
    global lblTemp, temperatura, imgTerm, lblTerm_Img, raiz, fondo
    temperatura = value
    #La imagen se ajusta para una retroalimentación visual pequeña (No exacta visualmente)
    if int(temperatura) <= 0:
        imgTerm = ImageTk.PhotoImage(Image.open("Images/term1.png"))
    elif int(temperatura) <= 17:
        imgTerm = ImageTk.PhotoImage(Image.open("Images/term2.png"))
    elif int(temperatura) <= 30:
        imgTerm = ImageTk.PhotoImage(Image.open("Images/term3.png"))
    else:
        imgTerm = ImageTk.PhotoImage(Image.open("Images/term4.png"))
    text = str(value) + " °C"
    lblTerm_Img = Label(raiz, image = imgTerm)
    lblTerm_Img.configure(bg=fondo)
    lblTerm_Img.grid(row = 5, column = 3)
    lblTemp["text"] = text


#Prende o apaga el ventilador, maneja la potencia mostrada
def ventila(potencia):
    #Variables: imgVent, lblVent_Img, lblPot_Vent, lblOnOff_Vent
    global activa_Vent #Variable que hace que se active o desactive (Para evitar 2 animaciones)
    global raiz, lblPot_Vent, lblOnOff_Vent 
    pot = float(potencia)
    #Preparamos las nuevas etiquetas
    lblPot_Vent = Label(raiz)
    lblPot_Vent.grid(row = 2, column = 1)
    lblOnOff_Vent = Label(raiz)
    lblOnOff_Vent.grid(row = 3, column = 1)
    if potencia != '0':
        #Cambiamos a la potencia actual
        lblPot_Vent["text"] = str(potencia) + "%"
        lblOnOff_Vent["text"] = "On"
        #Matando la anterior animación
        activa_Vent = False #Para que mate a otra animación, si la hay
        sleep(0.2) #Máximo tiempo para que la anterior animación termine
        #Iniciando la nueva animación
        activa_Vent = True
        hiloAnimacion = Thread(target = animacionVentilador, args=(pot,))
        hiloAnimacion.start()
    else:
        #Si se apaga
        lblPot_Vent["text"] = "0%"
        lblOnOff_Vent["text"] = "Off"
        activa_Vent = False

#La velocidad cambia con respecto a la potencia
def animacionVentilador(pot):
    global activa_Vent, imgActual_Vent, raiz, imgVent, lblVent_Img, fondo
    while activa_Vent:
        #Eliminamos la imagen anteriormente mostrada
        lblVent_Img.grid_remove()
        #Dependiendo de donde se haya detenido el ventilador, mostrará la siguiente
        if imgActual_Vent == 0:
            imgVent = ImageTk.PhotoImage(Image.open("Images/ventilador1.png"))
            imgActual_Vent = imgActual_Vent + 1
        elif imgActual_Vent == 1:
            imgVent = ImageTk.PhotoImage(Image.open("Images/ventilador2.png"))
            imgActual_Vent = imgActual_Vent + 1
        elif imgActual_Vent == 2:
            imgVent = ImageTk.PhotoImage(Image.open("Images/ventilador3.png"))
            imgActual_Vent = 0
        else:
            imgVent = ImageTk.PhotoImage(Image.open("Images/ventilador1.png"))
        lblVent_Img = Label(raiz, image = imgVent)
        lblVent_Img.configure(bg = fondo)
        lblVent_Img.grid(row = 1, column = 1)
        #Para simular movimientos diferentes, dependiendo de la potencia
        sleep(0.05 + (0.1 -(pot/1000)))  #Original: 0.05 + (1-(pot/100)) - Animación lenta
        #lblVent_Img.grid_remove()

#Elimina etiquetas anteriores para evitar la creación de muchos elementos
def quitaVentilaAnt():
    global lblPot_Vent, lblOnOff_Vent
    lblPot_Vent.grid_remove()
    lblOnOff_Vent.grid_remove()

#Enciende el foco y maneja la potencia del mismo
def calienta(potencia):
    global imgFoco, lblFoco_Img, lblPot_Foco, lblOnOff_Foco, raiz, fondo
    #Ya que se recibe en cadena, debe cambiarse a un valor legible
    pot = float(potencia)
    #Se modificaran
    lblPot_Foco = Label(raiz)
    lblPot_Foco.grid(row = 2, column = 3)
    lblOnOff_Foco = Label(raiz)
    lblOnOff_Foco.grid(row = 3, column = 3)
    #Caso especial de 0 (Para etiqueta On/Off)
    if pot == 0: 
        imgFoco = ImageTk.PhotoImage(Image.open("Images/foco1.png"))
        lblOnOff_Foco["text"] = "Off"
    else:
        lblOnOff_Foco["text"] = "On"

    #Se asignara una imagen dependiendo de la potencia
    if pot <= 25 and pot != 0:
        imgFoco = ImageTk.PhotoImage(Image.open("Images/foco2.png"))
    elif pot <= 50:
        imgFoco = ImageTk.PhotoImage(Image.open("Images/foco3.png"))
    elif pot <= 75:
        imgFoco = ImageTk.PhotoImage(Image.open("Images/foco4.png"))
    elif pot <= 100:
        imgFoco = ImageTk.PhotoImage(Image.open("Images/foco5.png"))
    else: 
        imgFoco = ImageTk.PhotoImage(Image.open("Images/foco5.png"))

    lblFoco_Img = Label(raiz, image = imgFoco)
    lblFoco_Img.configure(bg = fondo)
    lblFoco_Img.grid(row = 1, column = 3)
    
    #La potencia se puede poner siempre de esta manera
    lblPot_Foco["text"] = potencia + "%"

#Elimina anteriores etiquetas para evitar la creación de múltiples elementos
def quitaFoco():
    global lblFoco_Img, lblPot_Foco, lblOnOff_Foco
    lblFoco_Img.grid_remove()
    lblPot_Foco.grid_remove()
    lblOnOff_Foco.grid_remove()

#Controla el encendido/apagado del aspersor
def riega(estado):
    global imgAsp, lblAsp_Img, lblOnOff_Asp, raiz, fondo
    lblOnOff_Asp = Label(raiz)
    lblOnOff_Asp.grid(row = 6, column = 1)
    #El estado se utiliza "on", pues es lo que nos pasa el servidor
    if estado == "on":
        lblOnOff_Asp["text"] = "On"
        imgAsp = ImageTk.PhotoImage(Image.open("Images/aspersor2.png"))
    else:
        lblOnOff_Asp["text"] = "Off"
        imgAsp = ImageTk.PhotoImage(Image.open("Images/aspersor1.png"))
    lblAsp_Img = Label(raiz, image = imgAsp)
    lblAsp_Img.configure(bg = fondo)
    lblAsp_Img.grid(row = 5, column = 1)

#Eliminea anteriores etiquetas para evitar la creación de múltiples elementos
def quitaRiega():
    global lblAsp_Img, lblOnOff_Asp
    lblAsp_Img.grid_remove()
    lblOnOff_Asp.grid_remove()

#Devuelve temperatura actual (Función para retroalimentación)
def temperaturaActual(temp):
    slider_changed(str(temp))
    return int(temperatura)
