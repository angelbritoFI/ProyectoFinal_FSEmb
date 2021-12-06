#!/usr/bin/env python3
# Authors:
# 	Brito Segura Angel
# 	Tovar Herrera Carlos Eduardo
#	Zazueta Barajas Sebastián Pedro
# License: MIT
# Version 1.0
# Date: 21/11/2021
# Description: Simulador de Invernadero

#Parte gráfica del simulador
from tkinter import *
from PIL import ImageTk, Image

#Para manejar animaciones (Tal vez cambien a gifs)
from threading import Thread

from time import sleep

"""

"""

#Cuadros a utilizar (Que requieren activarse o cambiar por funciones)
etiqueta = None #Ejemplo
img = None
panel = None
raiz = None

#Imagenes para animar

imgAsp = None

imgTerm = None

#imagenes temporal
img1 = "yellow.png"
img2 = "white.png"
img3 = "red.png"
img4 = "blue.png"

#Ventilador 
activa_Vent = False
imgActual_Vent = 0
imgVent = None
lblVent_Img = None
lblPot_Vent = None 
lblOnOff_Vent = None
####IMAGENES VENTILADOR x3

#Aspersor
imgAsp = None 
lblAsp_Img = None 
lblOnOff_Asp = None
#Termometro
temperatura = "25"
lblTemp = None

#Foco 
imgFoco = None 
lblFoco_Img = None 
lblPot_Foco = None 
lblOnOff_Foco = None 
imgActual_Foco = 0
imgFoco = None

#Función para iniciar el simulador
def simularInvernadero():
    global etiqueta, raiz #Quitar etiqueta
    #Ventilador
    global imgVent, lblVent_Img, lblPot_Vent, lblOnOff_Vent
    #Aspersor
    global imgAsp, lblAsp_Img, lblOnOff_Asp
    #Termometro
    global lblTemp, temperatura, lblTerm_Img, imgTerm
    #Foco
    global imgFoco, lblFoco_Img, lblPot_Foco, lblOnOff_Foco
    global img, panel #ejemplos
    fondo = 'light sky blue'
    raiz = Tk() #Ventana principal
    raiz.geometry('600x700') #Dimensiones
    raiz.configure(bg = fondo) #Color de fondo
    raiz.title('Invernadero Simulado') #Título
	# Al presionar sobre el botón Cerrar 'X', el programa llegará a su fin

    #Espacios vacíos
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

    #Ejemplo
    #img = ImageTk.PhotoImage(Image.open(img1))
    #panel = Label(raiz, image = img)
    #panel.grid(row = 2, column = 2)
    #hilo1 = Thread(target=fingeMoverte) #, args=(x,y)
    #hilo1.start()

    etiqueta = Label(raiz)
    etiqueta.configure(bg = 'dodger blue')
    #etiqueta.grid(row = 0, column = 4)
    etiqueta["text"] = "Etiqueta"

    #Ventilador
    #Variables: imgVent, lblVent_Img, lblPot_Vent, lblOnOff_Vent
    #Imagen
    imgVent = ImageTk.PhotoImage(Image.open("Images/ventilador1.png"))
    lblVent_Img = Label(raiz, image = imgVent)
    lblVent_Img.grid(row = 1, column = 1)
    #hiloVent = Thread(target = ventila, args=(False))
    #hiloVent.start()

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
    lblFoco_Img.grid(row = 1, column = 3)
    #hiloFoco = Thread(target = calienta, args=(False))
    
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
    lblAsp_Img.grid(row = 5, column = 1)
    #hiloFoco = Thread(target = calienta, args=(False))

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
    lblTerm_Img.grid(row = 5, column = 3)
    #hiloFoco = Thread(target = calienta, args=(False))
    
    #Temperatura
    lblTemp = Label(raiz)
    lblTemp.grid(row = 6, column = 3)
    lblTemp["text"] = "0°C"

    #Slider (Cambiar la temperatura medida)
    sliderTemp = Scale(raiz, from_=-20, to=50, orient='horizontal', command = slider_changed)
    sliderTemp.grid(row = 7, column = 3)
    ##########################

    raiz.mainloop()

#Permite actualizar el valor "medido" por el termometro
#Realmente se coloca el valor directamente de ahí
def slider_changed(value):
    global lblTemp, temperatura, imgTerm, lblTerm_Img, raiz
    temperatura = value
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
    lblTerm_Img.grid(row = 5, column = 3)

    lblTemp["text"] = text


#Prende o apaga el ventilador (activa-bool)
def ventila(potencia):
    cuenta = 10 #Detendra la animacion pasado un tiempo
    #Variables: imgVent, lblVent_Img, lblPot_Vent, lblOnOff_Vent
    global activa_Vent #Variable que hace que se active o desactive (Para evitar 2 activaciones)
    global imgActual_Vent #Saber en que imagen vamos
    cambio = True
    global img1, img2, img3 #Imagenes del ventilador
    global raiz, imgVent, lblVent_Img #Imagen y ventana
    pot = int(potencia)
    lblPot_Vent = Label(raiz)
    lblPot_Vent.grid(row = 2, column = 1)
    lblOnOff_Vent = Label(raiz)
    lblOnOff_Vent.grid(row = 3, column = 1)
    if potencia != '0':
        lblPot_Vent["text"] = str(potencia) + "%"
        lblOnOff_Vent["text"] = "On"
        activa_Vent = True
    else:
        lblPot_Vent["text"] = "0%"
        lblOnOff_Vent["text"] = "Off"
        activa_Vent = False
    while(activa_Vent): #Si se apago simplemente no reproducirá lo siguiente
        if cuenta == 0:
            break
        try:
            lblVent_Img.grid_remove()
            if imgActual_Vent == 0:
                imgVent = ImageTk.PhotoImage(Image.open("Images/ventilador1.png"))
                imgActual_Vent = imgActual_Vent + 1
            elif imgActual_Vent == 1:
                imgVent = ImageTk.PhotoImage(Image.open("Images/ventilador2.png"))
                imgActual_Vent = imgActual_Vent + 1
            elif imgActual_Vent == 2:
                imgVent = ImageTk.PhotoImage(Image.open("Images/ventilador3.png"))
                imgActual_Vent = 0
            lblVent_Img = Label(raiz, image = imgVent)
            lblVent_Img.grid(row = 1, column = 1)
            sleep(0.15 + (1 - (pot/100)) )
            cuenta = cuenta - 1
        except:
            break

def quitaVentilaAnt():
    global lblPot_Vent, lblOnOff_Vent
    lblPot_Vent.grid_remove()
    lblOnOff_Vent.grid_remove()

def calienta(potencia):
    global imgFoco, lblFoco_Img, lblPot_Foco, lblOnOff_Foco, raiz
    global img1, img2, img3, img4

    pot = int(potencia)
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
    lblFoco_Img.grid(row = 1, column = 3)
    
    #La potencia se puede poner siempre igual
    lblPot_Foco["text"] = potencia + "%"

def quitaFoco():
    global lblFoco_Img, lblPot_Foco, lblOnOff_Foco
    lblFoco_Img.grid_remove()
    lblPot_Foco.grid_remove()
    lblOnOff_Foco.grid_remove()

def riega(estado):
    global imgAsp, lblAsp_Img, lblOnOff_Asp, raiz
    lblOnOff_Asp = Label(raiz)
    lblOnOff_Asp.grid(row = 6, column = 1)
    if estado == "on":
        lblOnOff_Asp["text"] = "On"
        imgAsp = ImageTk.PhotoImage(Image.open("Images/aspersor2.png"))
    else:
        lblOnOff_Asp["text"] = "Off"
        imgAsp = ImageTk.PhotoImage(Image.open("Images/aspersor1.png"))
    lblAsp_Img = Label(raiz, image = imgAsp)
    lblAsp_Img.grid(row = 5, column = 1)

def quitaRiega():
    global lblAsp_Img, lblOnOff_Asp
    lblAsp_Img.grid_remove()
    lblOnOff_Asp.grid_remove()

#Funcion de prueba (apagado remoto)
def apagaEtiqueta(): 
    etiqueta.grid_remove()

#Devuelve temperatura actual
def temperaturaActual(temp):
    slider_changed(str(temp))
    return int(temperatura)

#Prueba para crear animacion en tkinter
def fingeMoverte():
    x = True
    global img,panel,raiz
    while(True):
        try:
            if x:
                print("Plantaaaaaa")
                img = ImageTk.PhotoImage(Image.open("planta.png"))
                panel = Label(raiz, image = img)
                panel.grid(row = 2, column = 2)
                x = False
            else:
                print("Perraaaa")
                img = ImageTk.PhotoImage(Image.open("ventilador.gif"))
                panel = Label(raiz, image = img)
                panel.grid(row = 2, column = 2)
                x = True
        except:
            break
        print("llega?")
        sleep(1)

