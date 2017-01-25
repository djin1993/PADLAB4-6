from Server2 import *

host_name ='127.0.0.4'
message = host_name
file = FILE[2]

if __name__ == '__main__':
	run_server(host_name, PORT_NUMBER, file, message)
