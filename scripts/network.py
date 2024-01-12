import socket
import sys
from _thread import *
import pickle


class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = socket.gethostbyname(socket.gethostname())
		self.port = 5555
		self.addr = (self.server, self.port)
		self.p = self.connect()
		print(self.p)

	def get_p(self):
		return self.p

	def connect(self):
		try:
			self.client.connect(self.addr)
			return pickle.loads(self.client.recv(2048))
		except:
			pass

	def send(self, data):
		try:
			self.client.send(pickle.dumps(data))
			return pickle.loads(self.client.recv(2048))
		except socket.error as e:
			print(e, 'goo goo gah gah')

	def recieve(self):
		try:
			return self.client.recv(2048)
		except:
			pass