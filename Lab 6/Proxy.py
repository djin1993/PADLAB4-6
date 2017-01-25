from Globals import *
from SocketServer import ThreadingMixIn
import BaseHTTPServer
import requests
import threading
import time
import json
import xmltodict
from dicttoxml import dicttoxml


MAVEN1 = '127.0.0.6'
MAVEN2 = '127.0.0.7'
HOST_NAME = '127.0.0.8'

class MyServerClass(ThreadingMixIn, BaseHTTPServer.HTTPServer):
	"""Handle requests in a separate thread."""
	address_list = [MAVEN1, MAVEN2]
	thread_count = [[], []]
	cache_one = {}

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_HEAD(self):
		"""Respond to a HEAD request."""
		path_elements = self.path.split('/')
		thread_name = threading.currentThread().getName()

		if len(path_elements) == 4 and path_elements[-1] == '' and path_elements[1] == 'worker': # /worker/@id/
			if len(self.server.thread_count[0]) <= len(self.server.thread_count[1]):
				self.server.thread_count[0].append(thread_name)
				r = requests.head( 'http://' + self.server.address_list[0] + self.path)
				self.server.thread_count[0].remove(thread_name)
			else:
				self.server.thread_count[1].append(thread_name)
				r = requests.head( 'http://' + self.server.address_list[1] + self.path)
				self.server.thread_count[1].remove(thread_name)

			self.send_response(r.status_code)
			self.end_headers()
			
		else: # Bad request
			self.send_response(400)
			self.end_headers()

	def do_GET(self):
		"""Respond to a GET request."""
		path_elements = self.path.split('/')
		thread_name = threading.currentThread().getName()

		if self.path == '/worker/': # /worker/ 
			
			if len(self.server.thread_count[0]) <= len(self.server.thread_count[1]):
				self.server.thread_count[0].append(thread_name)
				r = requests.get( 'http://' + self.server.address_list[0] + self.path)
				self.server.thread_count[0].remove(thread_name)
			else:
				self.server.thread_count[1].append(thread_name)
				r = requests.get( 'http://' + self.server.address_list[1] + self.path)
				self.server.thread_count[1].remove(thread_name)

			self.send_response(r.status_code)
			self.send_header("Content-type", r.headers['Content-type'])
			self.end_headers()

			self.wfile.write(r.text)

		elif len(path_elements) == 4 and path_elements[-1] == '' and path_elements[1] == 'worker': # /worker/@id/

			if self.path in self.server.cache_one:
				self.send_response(200)
				self.send_header("Content-type", "text/xml")
				self.end_headers()
				self.wfile.write(self.server.cache_one[self.path])
				return

			if len(self.server.thread_count[0]) <= len(self.server.thread_count[1]):
				self.server.thread_count[0].append(thread_name)
				r = requests.get( 'http://' + self.server.address_list[0] + self.path)
				self.server.thread_count[0].remove(thread_name)
			else:
				self.server.thread_count[1].append(thread_name)
				r = requests.get( 'http://' + self.server.address_list[1] + self.path)
				self.server.thread_count[1].remove(thread_name)

			self.send_response(r.status_code)
			self.send_header("Content-type", r.headers['Content-type'])
			self.end_headers()

			self.wfile.write(r.text)

			if r.status_code == 200:
				self.server.cache_one[self.path] = r.text

		else: # Bad request
			self.send_response(400)
			self.end_headers()

	def do_PUT(self):
		"""Respond to a PUT request."""
		thread_name = threading.currentThread().getName()

		if self.path == '/worker/': # /worker/
			length = int(self.headers['Content-Length'])
			content_xml = self.rfile.read(length)

			if len(self.server.thread_count[0]) <= len(self.server.thread_count[1]):
				self.server.thread_count[0].append(thread_name)
				r = requests.put( 'http://' + self.server.address_list[0] + self.path, data = content_xml)
				self.server.thread_count[0].remove(thread_name)

				content_dict = xmltodict.parse(content_xml)
				content_dict['root']['item']['id'] = r.text
				content_xml = dicttoxml(content_dict['root'], attr_type=False)

				self.server.thread_count[1].append(thread_name)
				r = requests.put( 'http://' + self.server.address_list[1] + self.path + 'asis/', data = content_xml)
				self.server.thread_count[1].remove(thread_name)
				# add new id
				# /asis/ to the second

			else:
				self.server.thread_count[1].append(thread_name)
				r = requests.put( 'http://' + self.server.address_list[1] + self.path, data = content_xml)
				self.server.thread_count[1].remove(thread_name)

				content_dict = xmltodict.parse(content_xml)
				content_dict['root']['item']['id'] = r.text
				content_xml = dicttoxml(content_dict['root'], attr_type=False)

				self.server.thread_count[0].append(thread_name)
				r = requests.put( 'http://' + self.server.address_list[0] + self.path + 'asis/', data = content_xml)
				self.server.thread_count[0].remove(thread_name)								

			

			self.send_response(r.status_code)
			self.send_header("Content-type", r.headers["Content-type"])
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

	print time.asctime(), "Proxy Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()
	print time.asctime(), "Proxy Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
