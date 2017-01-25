from Globals2 import *
import time
import json
import BaseHTTPServer
import requests
import random
import threading
import socket
from dicttoxml import dicttoxml
from SocketServer import ThreadingMixIn
import xmltodict

HOST_NAME = '127.0.0.7'
UDP_IP = HOST_NAME

class Socket_listener(threading.Thread):

	def __init__(self, new_httpd):
		threading.Thread.__init__(self)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		self.httpd = new_httpd
		self.event = threading.Event()

	def run(self):
		self.socket.bind((UDP_IP, UDP_PORT))

		while True:
			data, addr = self.socket.recvfrom(1024) 
			print data
			self.httpd.address_list.add(data)

			if self.event.is_set():
				break

		self.socket.close()
		print "event called"
		

class MyServerClass(ThreadingMixIn, BaseHTTPServer.HTTPServer):
	"""Handle requests in a separate thread."""
	address_list = set()

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_HEAD(self):
		"""Respond to a HEAD request."""
		path_elements = self.path.split('/')

		if len(path_elements) == 4 and path_elements[-1] == '' and path_elements[1] == 'worker': # /worker/@id/
			for add in self.server.address_list:
				r = requests.head( 'http://' + add + self.path)
				if r.status_code == 200:
					break

			self.send_response(r.status_code)
			self.end_headers()
			
		else: # Bad request
			self.send_response(400)
			self.end_headers()

	def do_GET(self):
		"""Respond to a GET request."""
		path_elements = self.path.split('/')

		if len(path_elements) == 3 and path_elements[-1] == '' and path_elements[1] == 'worker': # /worker/
			# Return Json
			# self.wfile.write('[')

			# for add in self.server.address_list:
			# 	r = requests.get( 'http://' + add + self.path)
			# 	self.wfile.write(r.text[1:-2])

			# self.wfile.write(']')

			# Return Xml
			count = 1
			nr_nodes = len(self.server.address_list)
			temp_json =  '['

			for add in self.server.address_list:
				r = requests.get( 'http://' + add + self.path)
				temp_json = temp_json + r.text[1:-2]
				if count < nr_nodes:
					temp_json = temp_json + ','
					count += 1

			temp_json = temp_json + ']'

			temp_dict = json.loads(temp_json)
			temp_xml = dicttoxml(temp_dict, attr_type=False)

			self.send_response(r.status_code)
			self.send_header("Content-type", r.headers['Content-type'])
			self.end_headers()

			self.wfile.write(temp_xml)

		elif len(path_elements) == 4 and path_elements[-1] == '' and path_elements[1] == 'worker': # /worker/@id/
			for add in self.server.address_list:
				r = requests.get( 'http://' + add + self.path)
				if r.status_code == 200:
					break

			
			if r.status_code == 200:
				temp_json = '[' + r.text + ']'
				temp_dict = json.loads(temp_json)
				temp_xml = dicttoxml(temp_dict, attr_type=False)

				self.send_response(r.status_code)
				self.send_header("Content-type", "text/xml")
				self.end_headers()

				self.wfile.write(temp_xml)
			else:
				self.send_response(r.status_code)
				self.send_header("Content-type", "text")
				self.end_headers()

				self.wfile.write(r.text)



		else: # Bad request
			self.send_response(400)
			self.end_headers()

	def do_PUT(self):
		"""Respond to a PUT request."""

		if self.path == '/worker/' or self.path == '/worker/asis/': # /worker/ /worker/asis/
			length = int(self.headers['Content-Length'])
			content_xml = self.rfile.read(length)
			content_dict = xmltodict.parse(content_xml)
			content_json = json.dumps(content_dict['root']['item'],sort_keys=True, indent=4, separators=(',', ': '))

			r = requests.put( 'http://' + random.sample(self.server.address_list, 1)[0] + self.path, data = content_json )

			self.send_response(r.status_code)
			self.send_header("Content-type", r.headers['Content-type'])
			self.end_headers()
			
			self.wfile.write(r.text)

		else: # Bad request
			self.send_response(400)
			self.end_headers()


	# def do_DELETE(self):

if __name__ == '__main__':
	server_class = MyServerClass
	handler_class = MyHandler

	httpd = server_class((HOST_NAME, PORT_NUMBER), handler_class)

	socket_listener_thread = Socket_listener(httpd)
	socket_listener_thread.start()

	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()
	socket_listener_thread.event.set()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

## Detection here
## UDP broadcast as node start
## thread
## send the addlist to the thread
## time.sleep() on database requests
## Periodic broadcast, print in maven when new node comes
## Threaded basehttpserver for maven proxy but not for simple servers

#  SUBNETTING!!! /no/ different ports for broadcasting
# Proxy

# copy code to simple servers 2-4