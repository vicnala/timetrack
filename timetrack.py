#!/usr/bin/env python

from subprocess import check_output, CalledProcessError
import threading 
import time
from datetime import datetime
import os
import sqlite3


class CheckActiveWindow (threading.Thread):
		def __init__(self):
				self.cur = None
				self.conn = None
				self.stopped = False
				self.screensaver = False
				self.new = dict()
				self.last = dict()
				threading.Thread.__init__(self)

		def initdb(self):
				# data
				home = os.path.expanduser("~")
				database = home + "/timetrack.sqlite"

				if not os.path.exists(database):
						open(database, 'w').close()
				self.conn = sqlite3.connect(database)
				self.cur = self.conn.cursor()
				sql = """
						CREATE TABLE IF NOT EXISTS records ( \
								date TEXT, \
								host TEXT, \
								class TEXT, \
								title TEXT\
						)"""
				self.cur.execute(sql)

		def check(self):
				# take care about screensaver
				self.screensaver = False
				try:
						self.screensaver = check_output("nice -n 19 gnome-screensaver-command -q", shell=True).find(" acti") == -1
				except CalledProcessError, e:
						print('"Error","CalledProcessError","' + e.output + '"')
						return

				# get active window
				try:
						xprop_active_window_info = check_output("nice -n 19 xprop -root _NET_ACTIVE_WINDOW", shell=True)
				except CalledProcessError, e:
						print('"Error","CalledProcessError","' + e.output + '"')
						return
				
				window = xprop_active_window_info.split()[-1]		
				
				# get window properties
				try:
					xprop_window_info = check_output("nice -n 19 xprop -id " + window, shell=True)
				except CalledProcessError, e:
						print('"Error","CalledProcessError","' + e.output + '"')
						return
				
				keyvalues = {}
				for line in xprop_window_info.split('\n'):
						name, var = line.partition("=")[::2]
						keyvalues[name.strip()] = var

				try:
						self.new['hostname'] = keyvalues['WM_CLIENT_MACHINE(STRING)'].split('"')[1::2][0].decode('utf-8')
						self.new['appclass'] =  keyvalues['WM_CLASS(STRING)'].split(',')[1].split('"')[1::2][0].decode('utf-8')
						self.new['title'] = keyvalues['_NET_WM_NAME(UTF8_STRING)'].split('"')[1::2][0].decode('utf-8')
				except KeyError, e:
						print('"Error"' + ',"KeyError:","' + str(e) + '"')
						self.new['hostname'] = ""
						self.new['appclass'] = ""
						self.new['appclass'] = ""
						return

				if not self.screensaver:
						self.new['appclass'] = "screensaver"
						self.new['title'] = "screensaver"

				if not set(self.new.values()).issubset(self.last.values()):
						self.last['hostname'] = self.new['hostname']
						self.last['appclass'] = self.new['appclass']
						self.last['title'] = self.new['title']


						self.cur.execute("""INSERT INTO records VALUES (?,?,?,?)""", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.last['hostname'], self.last['appclass'], self.last['title']))
						self.conn.commit()

		def run(self):
				self.initdb()
				while not self.stopped:
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