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

import _basic
class Screen(_basic.Screen):
	
	def OnInit(self):
		image = Image.new("1", (self.width, self.height), BLACK)
		draw = ImageDraw.Draw(image)
		font1 = ImageFont.truetype(FONT_PATH+"verdana.ttf", 12)
		draw.text((0, 0),self.conf['text'],WHITE,font=font1)
		self.ImageBuffer=list(image.getdata())
		self.forceUpdate=True
