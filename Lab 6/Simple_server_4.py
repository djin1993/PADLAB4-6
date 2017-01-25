from Server2 import *

host_name = HOST_NAME[3]
message = host_name
file = FILE[3]

if __name__ == '__main__':
	run_server(host_name, PORT_NUMBER, file, message)
