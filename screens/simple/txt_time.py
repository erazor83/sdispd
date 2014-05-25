#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	a simple example screen which draws time, regulary
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-05-23"
__version__	= "0.0.1"
__license__ = "GPL"

from PIL import Image, ImageDraw, ImageFont

BLACK=0
WHITE=1

import time
import _basic
class Screen(_basic.Screen):
	forceUpdate=None
	
	def OnInit(self):
		self.image = Image.new("1", (self.width, self.height), BLACK)
		self.draw = ImageDraw.Draw(self.image)
		self.font1 = ImageFont.truetype(FONT_PATH+"verdana.ttf", 12)
		self.time_str=''
		
	def OnDisplay(self):
		time_str=time.strftime("%H:%M:%S")
		if (time_str!=self.time_str):
			#TODO: draw black rect below text
			self.OnInit()
			
			self.time_str=time_str
			self.draw.text((0, 0),time_str,WHITE,font=self.font1)
			self.ImageBuffer=list(self.image.getdata())
			self.forceUpdate=True
			
		if self.forceUpdate:
			self.UpdateDisplay()
			self.forceUpdate=False


