#!/usr/bin/env python3
# Authors:
# 	Brito Segura Angel
# 	Tovar Herrera Carlos Eduardo
#	Zazueta Barájas Sebastián Pedro
# License: MIT
# Version 1.0
# Date: 21/11/2021
# Description: Control de Invernadero

import sys
import math
import struct

from os import _exit
from threading import Thread, Timer, Lock
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

from smbus2 import Vi2cSlave
from __common import _get_sprites, _set_kill_handler, _img


class Invernadero(Vi2cSlave):
	def __init__(self, address=10, temperatura=20, ventilador=60, irrigacion = 0 ):
		super().__init__(address)
		self.temperatura = temperatura
		self.ventilador = ventilador
		self.irrigacion = irrigacion
		self._phaselock = Lock()
		self._data = [0, 0, 0, 0]

		# GUI
		self.gui = Tk(className=" Control de invernadero")
		self.gui.bind("<<UpdateGUI>>", self._update_gui)
		self._io_pins = {}
		self.controls = {}
		for i in range(1, 28):
			self._io_pins[i] = None
		self._sprites = _get_sprites(_img("lightbulb.png"), 680, scale=0.17)
		self._initialize_components()
		_set_kill_handler(self.close)
		self.running = True
		self.phase = 1000
	# end def

	def __del__(self):
		_exit(1)
	# end def

	


	def _initialize_components(self):
		# set window size
		# self.gui.geometry("510x270")
		self.gui.geometry("1000x500")
		#set window color
		self.gui.configure(bg='beige')
		self.gui.protocol("WM_DELETE_WINDOW", self._on_closing)

		# Control instantiation
		self.strIrrigacion = StringVar(self.gui)
		self.strTemperatura = StringVar(self.gui)
		self.strVentilador = StringVar(self.gui)

		# Validators

		self.lblIrrigacion = Label(self.gui, anchor="w",
			bg="beige", fg="black",
			text="Sistema de Irrigacion:")
		
		self.txtData = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable="Hola")

		self.lblTemperatura = Label(self.gui, anchor="w",
			bg="beige", fg="black",
			text="Temperatura:")
		

		self.lblVentilador = Label(self.gui, anchor="w",
			bg="beige", fg="black",
			text="Ventilador:")
		

		# Control initialization
		self.lblIrrigacion.grid(row=0, column=0, sticky="w", padx=2, pady=40)
		#self.txtLineV.grid(row=0, column=1, sticky="w", padx=2, pady=2)
		self.lblTemperatura.grid(row=1, column=0, sticky="w", padx=2, pady=50)
		#self.txtLineF.grid(row=1, column=1, sticky="w", padx=2, pady=2)
		self.lblVentilador.grid(row=2, column=0, sticky="w", padx=2, pady=50)
		self.txtData.grid(row=2, column=1, sticky="w", padx=2, pady=2)
		
		#self.lblPhase.grid(row=3, column=0, sticky="w", padx=2, pady=2)
		#self.txtPhase.grid(row=3, column=1, sticky="w", padx=2, pady=2)
		#self.lblPower.grid(row=4, column=0, sticky="w", padx=2, pady=2)
		#self.txtPower.grid(row=4, column=1, sticky="w", padx=2, pady=2)

		# self.lblLampI.grid(row=0, column=2, sticky="w", padx=50, pady=2,
		#                    columnspan=2, rowspan=5)

		# self.strLineV.set("V")
		# self.strLineF.set("{:0.0fHz")
		# self.strPhase.set("{:0.2fms")
		# self.strPower.set("{:0.3f%")

		#self._update_gui()
	# end def

	def _on_closing(self):
		self.running = False
		self.disconnect()
		self.gui.destroy()
		self.gui.quit()
		sys.exit()
	# end def

	def _get_phase_image(self):
		ix = max(0, min(10, int(self.power/10)))
		if ix < 4:
			return ImageTk.PhotoImage(self._sprites[ix])
		img = Image.blend(
			self._sprites[4],
			self._sprites[8],
			alpha=min(1, 0.25 * ix -1))
		if ix > 8 :
			img = Image.alpha_composite(img, self._sprites[ix])
		return ImageTk.PhotoImage(img)
	# end def

	def _update_gui(self, e=None):
		self.strPhase.set("{:0.1f}ms".format(self.phase*1000))
		self.strPower.set("{:0.3f}%".format(self.power))
		sdata = "0x" + "".join("{:02x}".format(x) for x in self._data)
		self.strDataR.set(sdata)
		img = self._get_phase_image()
		self.lblLampI.configure(image=img)
		self.lblLampI.image = img
	#end def

	def close(self, *args):
		print("Shutting down GUI")
		self._on_closing()
	#end def

	def read(self):
		"""Master reads a byte stream from the slave"""
		self._data = struct.pack("<f", self.phase)
		return self._data
	#end def

	def write(self, value):
		"""Master writes byte stream to the slave"""
		self._data = value
		self.phase = struct.unpack("<f", value)[0]
		try:
			self.gui.event_generate("<<UpdateGUI>>", when="tail")
		except:
			pass
	#end def


