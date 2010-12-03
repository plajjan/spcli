#!/usr/bin/python

import xmlrpclib

# Create an object to represent our server.
server_url = 'http://127.0.0.1:29999/XMLRPC'
server = xmlrpclib.Server(server_url);

# Call the server and get our result.
result = server.cancel_shutdown('TEST')
print "Sum:", result
