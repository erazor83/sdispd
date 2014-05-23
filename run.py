#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	deamon for libsdisp
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-05-23"
__version__	= "0.0.1"
__license__ = "GPL"

import os
import getopt
import sys
import pwd
import grp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'/'

import yaml

"""parse arguments"""
import argparse
parser = argparse.ArgumentParser(
	description='sdispd - daemon for libsdisp'
)
parser.add_argument(
	'-c','--config', type=str, 
	help='configuration file if not given it tries to find files in this order: '+
	'~/.sdispd.conf /etc/sdispd.conf'
)
parser.add_argument(
	'-v','--version', action='version', version='%(prog)s '+__version__
)
parser.add_argument(
	'-l','--logger', type=str,default='default',
	help='use a specific logger (has to be configured in config)'
)
parser.add_argument(
	'-u','--user', type=str, default=None,
	help='setuid to user'
)
parser.add_argument(
	'-g','--group', type=str, default=None,
	help='setgid to group'
)

args = parser.parse_args()
	
"""read config"""
cfg_file_list=['./sdispd.conf','/etc/sdispd.conf']
for cConfig in cfg_file_list:
	if os.path.isfile(cConfig):
		try:
			config=yaml.load(open(cConfig))
		except Exception as e:
			print("Error while loading config!")
			sys.exit(-1)

"""setup logger"""
import logging
import logging.config

#import pprint
#pp=pprint.PrettyPrinter()
#pp.pprint(config['logging'])

if 'logging' in config:
	logging.config.dictConfig(config['logging'])

	if args.logger in config['logging']['loggers']:
		logging.getLogger(args.logger)
	else:
		logging.warning('Logger "%s" not configured' % args.logger)


if args.group != None:
	logging.info("Changing to group %s:%i"%(args.group,grp.getgrnam(args.group).gr_gid))
	os.setgid(grp.getgrnam(args.group).gr_gid)

if args.user != None:
	logging.info("Changing to user %s:%i"%(args.user,pwd.getpwnam(args.user).pw_uid))
	os.setuid(pwd.getpwnam(args.user).pw_uid)


#init display
import sdisp
dsp_type=config['display']['type']
if 		dsp_type=='crius':
	sdisp_ctx=sdisp.sdisp_new_crius(
		int(config['display']['bus'])
	)
elif	dsp_type=='ssd1306':
	sdisp_ctx=sdisp.sdisp_new_ssd1306(
		int(config['display']['bus'])
	)
elif	dsp_type=='ssd1327':
	sdisp_ctx=sdisp.sdisp_new_ssd1327(
		int(config['display']['bus'])
	)
else:
	logging.error("Display type not supported!")
	sys.exit(-1)
logging.info("Created display %s"%dsp_type)

if 'debug' in config['display'] and config['display']['debug']:
	sdisp.sdisp_set_debug(sdisp_ctx,True)
else:
	sdisp.sdisp_set_debug(sdisp_ctx,False)

sdisp.sdisp_display__init(sdisp_ctx)
	
#get display info
displayInfo={
	'width':			sdisp.sdisp_display__getWidth(sdisp_ctx),
	'height':			sdisp.sdisp_display__getHeight(sdisp_ctx),
	'features':		sdisp.sdisp_display__getFeatures(sdisp_ctx)
}
#try to create screens
SCREENS={}
for screenInstanceName in config['screens']:
	screen_package=			config['screens'][screenInstanceName][0]
	screen_duration=		config['screens'][screenInstanceName][1]
	screen_config=			config['screens'][screenInstanceName][2]
	if os.path.isfile(BASE_DIR+'screens/'+screen_package+'.py'):
		package_name='screens.'+screen_package
		if not sys.modules.has_key(package_name):
			__import__(package_name, globals(), locals(), [])
			sys.modules[package_name].FONT_PATH=BASE_DIR+'fonts/'
		SCREENS[screenInstanceName]=sys.modules[package_name].Screen(
			screen_config,
			displayInfo,
			screen_duration
		)
		logging.info("Screen %s [%s] created"%(screenInstanceName,screen_package))

import time
try:
	while True:
		for screen in SCREENS:
			if SCREENS[screen].ImageBuffer:
				logging.info("Showing %s..."%screen)
				sdisp.sdisp_display__buffer_set_pixels(
					sdisp_ctx,
					0,
					SCREENS[screen].ImageBuffer
				)
				sdisp.sdisp_display__buffer_draw(sdisp_ctx)
				time.sleep(SCREENS[screen].Duration)
except KeyboardInterrupt:
	pass


sdisp.sdisp_close(sdisp_ctx)


