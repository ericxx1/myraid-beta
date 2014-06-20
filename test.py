from threading import Thread
class Memory(Thread):
	def __init__(self):
		self.Collector = {}
	def Add(self, x, y):
		self.Collector[x] = y
	def Select(self, x):
		return self.Collector[x]
mem = Memory()
x = "hi"
y = "dong"
mem.Add(x, y)
print mem.Select(x)
