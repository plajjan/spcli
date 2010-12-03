"""
Manager stuff

What should the manager do?

 - Start daemons, ie routing processes
 - Write out config files for "ternary" processes
	- such as NTPd, ie, it doesn't have a SPCLI compatible XML-RPC interface


The manager is basically an XML RPC mediator with some backend functionality.
It manages starting up worker processes who are needed to complete certain tasks..

All processes that actually perform something are referred to as workers, be it a routing process or a process to write a configuration file..

"""
from twisted.web import xmlrpc, server
import subprocess
import re

class FunctionsSystem:

	def _run(self, args, timeout = None, outerr_exit_condition = [], out_exit_condition = [], err_exit_condition = []):
		process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		retcode = process.poll()
		retout = ''
		reterr = ''
		while true:
			r_ready, w_ready, x_ready = select.select([ process.stdout, process.stderr ], [], [], timeout)

			for fh in r_read:
				line = fh.readline()

				if fh == process.stdout:
					retout += line
					for cond in out_exit_condition:
						if re.match(cond, line):
							return retcode, retout, reterr
					for cond in outerr_exit_condition:
						if re.match(cond, line):
							return retcode, retout, reterr
				elif fh == process.stderr:
					reterr += line
					for cond in err_exit_condition:
						if re.match(cond, line):
							return retcode, retout, reterr
					for cond in outerr_exit_condition:
						if re.match(cond, line):
							return retcode, retout, reterr

		return retcode, retout, reterr

	def cancel_shutdown(self, reason):
		retcode,retout,reterr = self._run(['/sbin/shutdown', '-c', reason])
		ret_message = 'Canceled shutdown.'
		if re.match('shutdown: Cannot find pid of running shutdown', reterr):
			ret_message = 'No shutdown/reboot scheduled.'
		return { 'message': ret_message }

	def reboot(self, time, reason, response = None):
		if response is None:
			return { 'answer_type': 'question', 'message': 'Reboot the system?' }
		retcode,retout,reterr = self._run(['/sbin/shutdown', '-r', time, reason, '&'])
		print "OUT: ", retout
		print "ERR: ", reterr
		ret_message = ''
		if re.match('shutdown: Cannot find pid of running shutdown', reterr):
			ret_message = 'No shutdown/reboot scheduled.'
		return { 'answer_type': '', 'message': ret_message }

	def halt(self):
		time = self._normalize_shutdown_time(time)
		subprocess.call(['/sbin/shutdown', '-h', time, reason])
		return

class Mgr:
	stop = None
	cli_clients = []
	daemons = []
	daemons_needed = {}
	daemons_running = {}


	def __init__(self):
		pass

	def start_worker(self):
		pass

	def stop_worker (self):
		pass

	def run(self):
		from twisted.internet import reactor

		r = CliP()
		r.mgr = self

		reactor.listenTCP(29999, server.Site(r))
		reactor.run()


class CliP(xmlrpc.XMLRPC):
	mgr = None
	FS = FunctionsSystem()

	def cli_register(self, data):
		print "TJOasd"
		pass

	def remote_echo(self, st):
		print "echoing:", st
		return 'ECHOING:' + st

	def xmlrpc_cliRegister(self, data):
		result = "Hello"
		return result

	def xmlrpc_echo(self, val):
		print "TJO"
		return 'SERV:' + val

	def xmlrpc_cancel_shutdown(self, reason):
		return self.FS.cancel_shutdown(reason)

	def xmlrpc_reboot(self, time, reason):
		return self.FS.reboot(time, reason)



