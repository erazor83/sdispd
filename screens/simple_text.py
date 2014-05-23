#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	a simple example screen which draws text
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-05-23"
__version__	= "0.0.1"
__license__ = "GPL"

from PIL import Image, ImageDraw, ImageFont

BLACK=0
WHITE=1

import _common
class Screen(_common.Screen):
	def OnInit(self):
		image = Image.new("1", (self.Width, self.Height), BLACK)
		draw = ImageDraw.Draw(image)
		font1 = ImageFont.truetype(FONT_PATH+"verdana.ttf", 12)
		draw.text((0, 0),self.Conf['text'],WHITE,font=font1)
		self.ImageBuffer=list(image.getdata())
		
	def OnDisplay(self):
		pass
	def OnClose(self):
		pass
	def getImage(self):
		pass

