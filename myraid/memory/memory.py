import re, socket, os, sys, time
from threading import Thread

class i(object):
	pass
i = i()
i.i = 0;

class Memory_Stack(Thread):
	global stack
	stack = {};	
	def __init__(self):
		Thread.__init__(self)
	def Add(function):
		i.i+=1
		stack[i.i] = function;
	def Select(self, name):
		return stack[name];
	def Empty(self):
		del stack[:]
		
class Sockets():
	def __init__(self):
		self.Socket_list = {}
		Socket_list = self.Socket_list
	def Add(self, name ,socket_data):
		self.Socket_list[name] = socket_data
	def Select(self, name):
		#for value in self.Socket_list:
		#	print value
		return self.Socket_list[name]
	def Empty(self):
		del self.Socket_list[:]
		
class Memory(Thread):
	global Collector
	Collector = {};
	def Add(name, value):
		Collector[name] = value;	
	def Select(name):
		return Collector[name];
	def Empty():
		del Collector[:]
		
