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
	Conf=None
	Info=None
	Duration=None

	ImageBuffer=None
	Width=None
	Height=None
	
	active=False
	
	def __init__(self,conf,info,duration):
		self.Conf=conf
		self.Info=info
		self.Duration=duration
		
		self.ImageBuffer=[]
		
		self.Width=info['width']
		self.Height=info['height']
		
		self.OnInit()
		

	def activate(self):
		self.active=True
		
	def deactivate(self):
		self.active=False
		
		
	def OnInit(self):
		pass

	def OnDisplay(self):
		pass
	
	def OnClose(self):
		pass
	
	def getImageBuffer(self):
		return self.ImageBuffer

	def Update(self):
		pass
	
	def UpdateRegion(self):
		pass
