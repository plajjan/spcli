#!/usr/bin/python

from twisted.web.xmlrpc import Proxy
from twisted.internet import reactor, threads, defer
import sys

def handleResponse(response):
	if response['answer_type'] == 'question':
		print response['message']
		input = sys.stdin.readline()
	proxy.callRemote('reboot', '23:00', 'Because I can!', input).addCallbacks(handleResponse, printError)
	reactor.stop()

def printError(value):
	print 'error:', value
	reactor.stop()

proxy = Proxy('http://127.0.0.1:29999/XMLRPC')
#proxy.callRemote('cancel_shutdown', 'Because I can!').addCallbacks(printValue, printError)
proxy.callRemote('reboot', '23:00', 'Because I can!').addCallbacks(handleResponse, printError)
reactor.run(installSignalHandlers=0)
