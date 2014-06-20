from rpython.rlib import rsocket
from rpython.rlib.rsocket import *
from ..memory import memory
#Sockets = memory.Sockets();
def create_socket(self, name):
	myraid_socket = RSocket(AF_INET, SOCK_STREAM);
	memory.Sockets.Add(self, name, myraid_socket);
	print "Socket created " + str(memory.Sockets.Select(name));
	
def connect_socket(self, name, host, port):
	print "Name:" + name + "," + host + "," + port
	myraid_socket = memory.Sockets.Select(self, name);
	try:
		addr = INETAddress(host, int(port))
		myraid_socket.connect(addr)
		print "Connected to " + host;
	except(rsocket.SocketError):
		print "Could not connect to " + host;
		pass
		
def create_socket_server(self, name, port):
	try:
		myraid_socket = memory.Sockets.Select(self, name);
		myraid_socket.bind(INETAddress('localhost', int(port)));
		print "Socket binded on port " + port
	except(rsocket.SocketError):
		return "Could not bind to port " + port;
		pass
		
def send_to_socket(self, name, data):
	myraid_socket = memory.Sockets.Select(self, name);
	myraid_socket.send(data);
	return None;
	
def socket_recv(name, bytes_per_chunk):
	myraid_socket = memory.Sockets.Select(self, name);
	data = myraid_socket.recv(int(bytes_per_chunk));
	return data;
