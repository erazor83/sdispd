#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	deamon for libsdisp
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-05-25"
__version__	= "0.0.3"
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

parser.add_argument(
	'-s','--screen', type=str, default=None,
	help='force screen'
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
import sys
sys.path.append(BASE_DIR+'inc/')
import sdisp_display

currentDisplay=sdisp_display.Display(config['display'])
currentDisplay.open()
currentDisplay.getInfo()

#try to create screens

sys.path.append(BASE_DIR+'screens/')

SCREENS={}
if args.screen != None:
	USED_SCREENS=[args.screen]
else:
	USED_SCREENS=config['screens']
	
for screenInstanceName in USED_SCREENS:
	cConfig=config['screens'][screenInstanceName]
	if len(cConfig)==1:
		cConfig.append(10)
	if len(cConfig)==2:
		cConfig.append({})
		
	screen_package=			cConfig[0]
	screen_duration=		cConfig[1]
	screen_config=			cConfig[2]
	if os.path.isfile(BASE_DIR+'screens/'+screen_package.replace('.','/')+'.py'):
		package_name='screens.'+screen_package
		if not sys.modules.has_key(package_name):
			__import__(package_name, globals(), locals(), [])
			sys.modules[package_name].FONT_PATH=BASE_DIR+'fonts/'
		SCREENS[screenInstanceName]=sys.modules[package_name].Screen(
			currentDisplay,
			screen_config,
			screen_duration
		)
		logging.info("Screen %s [%s] created"%(screenInstanceName,screen_package))

import time
	
try:
	while True:
		for screen in SCREENS:
			SCREENS[screen].activate()
			t_end=time.time()+SCREENS[screen].duration
			while (time.time()<t_end):
				time.sleep(0.2)
				SCREENS[screen].OnDisplay()
				
			SCREENS[screen].deactivate()
except KeyboardInterrupt:
	pass

for screen in SCREENS:
	SCREENS[screen].OnClose()
	

currentDisplay.close()