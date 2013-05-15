#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import logging
from subprocess import check_output, CalledProcessError
import threading 
import time

logfile = 'timetrack.csv'


class CheckActiveWindow (threading.Thread):
    def __init__(self):
				self.stopped = False
				self.new = dict()
				self.last = dict()
				logging.basicConfig(filename=logfile, format='%(asctime)s, %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)
				threading.Thread.__init__(self)

    def check(self):
				# get active window
				try:
						xprop_active_window_info = check_output("nice -n 19 xprop -root _NET_ACTIVE_WINDOW", shell=True)
				except CalledProcessError, e:
						logging.info('"Error","CalledProcessError","' + e.output + '"')
						return
				
				window = xprop_active_window_info.split()[-1]				
				
				# get window properties
				try:
					xprop_window_info = check_output("nice -n 19 xprop -id " + window, shell=True)
				except CalledProcessError, e:
						logging.info('"Error","CalledProcessError","' + e.output + '"')
						return
				
				keyvalues = {}
				for line in xprop_window_info.split('\n'):
						name, var = line.partition("=")[::2]
						keyvalues[name.strip()] = var

				try:
						self.new['hostname'] = keyvalues['WM_CLIENT_MACHINE(STRING)'].split('"')[1::2][0]
						self.new['appclass'] =  keyvalues['WM_CLASS(STRING)'].split(',')[1].split('"')[1::2][0]
						self.new['title'] = keyvalues['_NET_WM_NAME(UTF8_STRING)'].split('"')[1::2][0]
				except KeyError, e:
						#logging.info('"Error"' + ',"KeyError:","' + str(e) + '"')
						self.new['hostname'] = ""
						self.new['appclass'] = ""
						self.new['appclass'] = ""
						return

				if not set(self.new.values()).issubset(self.last.values()):
						self.last['hostname'] = self.new['hostname']
						self.last['appclass'] = self.new['appclass']
						self.last['title'] = self.new['title']
						# TODO: take care about screensaver
						logging.info('"' + self.last['hostname'] + '","' + self.last['appclass'] + '","' + self.last['title'] + '"')

    def run(self):
        while not self.stopped:
            # call a function
            self.check()
            time.sleep(5)


if __name__ == "__main__":
		try:
				check = CheckActiveWindow()
				check.daemon = True
				check.start()
				while True:
						time.sleep(100)
		except KeyboardInterrupt:
				print "\nbye!"