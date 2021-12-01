#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Autor: Carlos  Eduardo Tovar Herrera
#  Programa que recibe el factor de potencia y determina el desfase 
#   
# ## #############################################################

import smbus2
import struct
import time

# Initializes virtual board (comment out for hardware deploy)
from sincronizacion import run_invernadero_board

# Arduino's I2C device address
SLAVE_ADDR = 0x0B # I2C Address of Arduino
potencia_actual = 0 					# Almacena la potencia actual, para compararla con la siguiente
# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)

def writePhase(delay):
	"""Writes the delay phase in milliseconds to the Arduino via I2C"""
	try:
		data = struct.pack('<f', delay/1000.0)
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
		i2c.i2c_rdwr(msg)
		print('Written phase delay: {:0.5f} ({:0.1f}ms)'.format(delay/1000.0, delay))
	except Exception as ex:
		raise ex
#end def

def powerf2ms(parametros, frecu):
	if int(parametros) <= 100 and int(parametros) >=0:					# Válida que la potencia se encuentre en el rango permitido
		diccionario60 ={												# Valores de la tabla 1: Relacion potencia-disparo a 60 Hz
			'100': 0.00, '95' : 2.060, '90' : 2.696, '85' : 3.157,
			'80' : 3.538, '75' : 3.874, '70' : 4.179, '65' : 4.464,
			'60' : 4.734, '55' : 4.993, '50' : 5.245, '45' : 5.493,
			'40' : 5.738, '35' : 5.984, '30' : 6.232, '25' : 6.487,
			'20' : 6.750, '15' : 6.487, '10' : 7.334, '5' : 7.688,
			'0' : 8.203
		}
		diccionario50 ={											# Valores de la tabla : Relacion potencia-disparo a 50 Hz
			'100': 0.00, '95' : 2.500, '90' : 3.277, '85' : 3.833,
			'80' : 4.277, '75' : 4.666, '70' : 4.047, '65' : 5.388,
			'60' : 5.711, '55' : 6.021, '50' : 6.323, '45' : 6.620,
			'40' : 6.914, '35' : 7.209, '30' : 7.508, '25' : 7.813,
			'20' : 8.111, '15' : 8.469, '10' : 8.832, '5' : 9.272,
			'0' : 10.00
		}
		if frecu == 60:											# Dependiendo del valor de la frecuencia se usa el diccionario adecuado
			diccionario = diccionario60
		else:
			diccionario = diccionario50

		pf = diccionario.get(parametros, 'No')					# Si el valor no se encuentra en el diccionario, se realizara una interpolación
														
		param = int(parametros)
		if pf != 'No':
			return float(pf)								# Si se encuentra en el diccionario regresa el valor de desfase
		else:												# En caso contrario realizara la interpolación lineal
															# tomando el punto más cercano, superior o inferior al ingresado
			delta = 5-(param % 5)	
			x2 = param + delta								# Potencia superior a la ingresada
			x1 = x2-5										# Potencia inferior a la ingresada
			y1 = diccionario.get(str(x1))					# Desfase superior de la potencia ingresada
			y2 = diccionario.get(str(x2))					# Desfase inferior de la potencia ingresada
			valor = y1 + (y2 - y1)/(x2 - x1)*(param - x1)	# Calculo del retraso del disparo correspondiente al factor de potencia
			return valor
	else:
		print("\tFactor de potencia incorrecto, valores permitidos 0-100")
		return 0
#end def

def valida_frecuencia():						# Función para ingresar la frecuencia 
	while True:									# Solo permite valores de 50 o 60 Hz
		try:
			frecuencia = int(input("Frecuencia: "))
		except ValueError:
			print("Debes escribir un número.")
			continue
		
		if (frecuencia != 60) and (frecuencia != 50):
			print("La frecuencia permitida es de 50[Hz] o 60[Hz].")
			print("\tEl valor recomendado es: frecuencia = 60")
			continue
		else:
			return frecuencia



def main():
	# Runs virtual board (comment out for hardware deploy)
	run_invernadero_board(address = 11,temperatura=20, ventilador=60, irrigacion = 0)
	# Shutdown lamp
	time.sleep(1)
	#writePhase(1000/60)


	while True:
		try:
			parametros = input("Ingrese parametros de configuracion: ") 	# Solicita  los parámetros 
			writePhase(float(parametros))
			
		except KeyboardInterrupt:
			return 0
#end def

if __name__ == '__main__':
	main()
