#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# virtualboards.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# Configures multiple boards to be run in a separate thread.
#
# ## #############################################################

import sys
import signal
from atexit import register
from threading import Barrier, Event, Thread
from threading import current_thread, main_thread
from interfaz import Invernadero
from tkinter import Tk, mainloop


_board = None
_board_type = None
_async_board_thread = None
_barrier = Event()# Barrier(2)


def _async_board_worker(*args, **kwargs):
	global _async_board_thread
	global _board

	if _board_type == 'dimm':
		_board = Invernadero(*args, **kwargs)
	else:
		return

	_barrier.set()

	try:
		print("Running GUI")
		mainloop()
	except:
		pass
	_async_board_thread = None
# end def



def _setup(*args, **kwargs):
	global _async_board_thread
	_async_board_thread = Thread(
		target = _async_board_worker,
		args = args,
		kwargs = kwargs)
	_async_board_thread.daemon = True
# end def



def _wait_board():
	_barrier.wait()
	# if current_thread() is main_thread():
	# 	signal.signal(signal.SIGINT, _board.close)
	# 	signal.signal(signal.SIGTERM, _board.close)
# end def



def _check_board():
	if (_board is not None) or (_async_board_thread is not None):
		raise RuntimeError("A board is already running")
# end def


def run_invernadero_board(address=10, temperatura=20, ventilador=60, irrigacion = 0):
	_check_board()
	_setup(address=address,temperatura=temperatura, ventilador=ventilador, irrigacion =irrigacion)

	global _board_type
	_board_type = "dimm"
	_async_board_thread.start()
	_wait_board()
# end def




