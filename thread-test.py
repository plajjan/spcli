#!/usr/bin/python

import threading
import datetime

class ThreadClass(threading.Thread):
	def run(self):
		now = datetime.datetime.now()
		print "%s says Hello World at time: %s" % (self.getName(), now)
		import time
		time.sleep(1)
		now = datetime.datetime.now()
		print "%s says Hello World at time: %s" % (self.getName(), now)


for i in range(2):
	t = ThreadClass()
	t.start()
