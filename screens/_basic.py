#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	common Screen base class
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-05-24"
__version__	= "0.0.2"
__license__ = "GPL"

import time

class Screen():
	conf=None
	duration=None
	display=None
	
	ImageBuffer=None
	width=None
	height=None
	
	active=False
	forceUpdate=None

	def __init__(self,display,conf,duration):
		self.display=display
		self.conf=conf
		self.duration=duration
		
		self.ImageBuffer=[]
		
		self.width=display.info['width']
		self.height=display.info['height']
		
		self.OnInit()
		

	def activate(self):
		self.active=True
		
	def deactivate(self):
		self.active=False
		
		
	def OnInit(self):
		pass

		
	def OnDisplay(self):
		if self.forceUpdate and self.ImageBuffer:
			self.UpdateDisplay()
			self.forceUpdate=False
	
	def OnClose(self):
		pass

	def UpdateDisplay(self):
		self.display.displayBuffer(self.ImageBuffer)
	
	def UpdateRegion(self):
		#TODO: add region update
		self.display.displayBuffer(self.ImageBuffer)
