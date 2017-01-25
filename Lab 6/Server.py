from Database import * 
from Globals import *
import time
import json
import BaseHTTPServer
import threading
import socket


HOST_NAME = [
	'127.0.0.2', 
	'127.0.0.3', 
	'127.0.0.4', 
	'127.0.0.5'] 
FILE = [
	'D.json', 
	'E.json', 
	'F.json', 
	'G.json']

MESSAGE = ''

class Socket_listener(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.socket = None
		self.event = threading.Event()

	def run(self):
		while not self.event.is_set():
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			self.socket.sendto(MESSAGE, (UDP_IP, UDP_PORT))
			self.socket.close()
			print MESSAGE
			time.sleep(5)

		print "event set"


class MyServerClass(BaseHTTPServer.HTTPServer):
	"""docstring for MyServerClass"""
	db = None


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_HEAD(self):
		"""Respond to a HEAD request."""
		path_elements = self.path.split('/')

		if len(path_elements) == 4 and path_elements[-1] == '' and path_elements[1] == 'worker': # /worker/@id/
			one = self.server.db.get_one(path_elements[2])
			
			if one == DB_ERRCODE:
				self.send_response(404)
				self.end_headers()

			else:
				self.send_response(200)
				self.end_headers()

		else: # Bad request
			self.send_response(400)
			self.end_headers()


	def do_GET(self):
		"""Respond to a GET request."""
		path_elements = self.path.split('/')

		if len(path_elements) == 3 and path_elements[-1] == '' and path_elements[1] == 'worker': # /worker/
			all = self.server.db.get_all()
			all_json = json.dumps(all, sort_keys=True, indent=4, separators=(',', ': '))

			self.send_response(200)
			self.send_header("Content-type", "text/json")
			self.end_headers()

			self.wfile.write(all_json)

		elif len(path_elements) == 4 and path_elements[-1] == '' and path_elements[1] == 'worker': # /worker/@id/
			one = self.server.db.get_one(path_elements[2])

			if one == DB_ERRCODE:
				self.send_response(404)
				self.end_headers()

				
			else:
				one_json = json.dumps(one, sort_keys=True, indent=4, separators=(',', ': '))

				self.send_response(200)
				self.send_header("Content-type", "text/json")
				self.end_headers()

				self.wfile.write(one_json)

		else: # Bad request
			self.send_response(400)
			self.end_headers()


	def do_PUT(self):
		"""Respond to a PUT request."""
		length = int(self.headers['Content-Length'])
		content_json = self.rfile.read(length)
		content = json.loads(content_json)

		if self.path == '/worker/': # /worker/
			identity = self.server.db.add_one(content)

			self.send_response(200)
			self.send_header("Content-type", "text")
			self.end_headers()
			self.wfile.write(identity)

		elif self.path == '/worker/asis/': # /worker/asis/
			identity = self.server.db.add_asis(content)			

			self.send_response(200)
			self.send_header("Content-type", "text")
			self.end_headers()
			self.wfile.write(identity)

		else: # Bad request
			self.send_response(400)
			self.end_headers()

	# def do_DELETE(self):


def run_server(host_name, port_number, file, message, server_class=MyServerClass, handler_class=MyHandler):

	global MESSAGE
	httpd = server_class((host_name, port_number), handler_class)
	httpd.db = Database()
	httpd.db.populate(file)
	MESSAGE = message

	socket_listener_thread = Socket_listener()
	socket_listener_thread.start()

	print time.asctime(), "Server Starts - %s:%s" % (host_name, port_number)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
		
	socket_listener_thread.event.set()
	httpd.db.depopulate(file)
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (host_name, port_number)

