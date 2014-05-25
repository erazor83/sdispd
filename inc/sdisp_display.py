# -*- coding: utf-8 -*-
"""
	class for libdisp
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-05-25"
__version__	= "0.0.2"
__license__ = "GPL"


import logging

import sdisp

class Display():
	conf=None
	info=None
	
	_sdisp_ctx=None
	
	def __init__(self,conf):
		self.conf=conf
		
	def open(self):
		dsp_type=self.conf['type']
		if 		dsp_type=='crius':
			self._sdisp_ctx=sdisp.sdisp_new_crius(
				int(self.conf['bus'])
			)
		elif	dsp_type=='ssd1306':
			self._sdisp_ctx=sdisp.sdisp_new_ssd1306(
				int(self.conf['bus'])
			)
		elif	dsp_type=='ssd1327':
			self._sdisp_ctx=sdisp.sdisp_new_ssd1327(
				int(self.conf['bus'])
			)
		else:
			logging.error("Display type not supported!")
			return False
		
		logging.info("Created display %s"%dsp_type)
	

		if 'debug' in self.conf and self.conf['debug']:
			sdisp.sdisp_set_debug(self._sdisp_ctx,True)
		else:
			sdisp.sdisp_set_debug(self._sdisp_ctx,False)

		sdisp.sdisp_display__init(self._sdisp_ctx)
		return True

	def getInfo(self):
		#get display info
		self.info={
			'width':			sdisp.sdisp_display__getWidth(self._sdisp_ctx),
			'height':			sdisp.sdisp_display__getHeight(self._sdisp_ctx),
			'features':		sdisp.sdisp_display__getFeatures(self._sdisp_ctx)
		}
		return self.info

	def displayBuffer(self,buff):
		sdisp.sdisp_display__buffer_set_pixels(
			self._sdisp_ctx,
			0,
			buff
		)
		sdisp.sdisp_display__buffer_draw(self._sdisp_ctx)

	def close(self):
		sdisp.sdisp_close(self._sdisp_ctx)

