from Server import *

host_name = HOST_NAME[0]
message = host_name
file = FILE[0]

if __name__ == '__main__':
	run_server(host_name, PORT_NUMBER, file, message)
