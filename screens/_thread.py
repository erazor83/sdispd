#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	threaded screen - a screen with background thread
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-05-23"
__version__	= "0.0.1"
__license__ = "GPL"

import _basic
import threading
import time
class Screen(_basic.Screen,threading.Thread):
	_alive=False
	
	def __init__(self,conf,info,duration):
		threading.Thread(self)
		_basic.Screen.__init__(self,conf,info,duration)
	
	def run(self):
		while self._alive:
			time.sleep(1)
			
	def OnInit(self):
		self.run()
		
	def OnClose(self):
		self._alive=False

