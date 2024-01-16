import socket
import select
import sys
from _thread import *
import pickle
import ipaddress
import subprocess

results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
signal_strength = int(''.join([i for i in (''.join([i for i in list((results.decode('ascii')).split('\n')) if 'Signal' in i]).strip()) if i.isnumeric()]))
#the above line is super unreadable, but it just retrieves the singal strength from a long list of strings of random stuff


def find_search_speed():
	results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
	signal_strength = int(''.join([i for i in (''.join([i for i in list((results.decode('ascii')).split('\n')) if 'Signal' in i]).strip()) if i.isnumeric()]))
	return .085 / (signal_strength / 100)

def get_end_ip_id(ip_address):
	n = 0
	for char in str(ipaddress):
		n += 1
		if char == '.':
			n = 0

	return n

class Network:
	def __init__(self, skip, server='N/A'):
		if not skip:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server = socket.gethostbyname(socket.gethostname())
			print(self.server)
			self.found_server = False
			self.p = None
			self.ip_found = None
			network = ipaddress.ip_network(self.server[:-get_end_ip_id(self.server)] + '0/24')

			self.search_speed = find_search_speed()
			network = ipaddress.ip_network(self.server[:-3] + '0/24')

			for ip in network:
				addr = (str(ip), 5555)
				#print('checking ', addr)
				#print(addr[0])
				ping = self.search_servers(addr)
				if ping != None:
					#print(f'!-> Connected to server {addr[0]} <-!')
					#print(f'--Connected to server {addr[0]}--')
					self.server = addr[0]
					self.found_server = True
					self.ip_found = addr[0]
					break
		else:
			print(server)
			if server == 'N/A':
				self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.server = socket.gethostbyname(socket.gethostname())
				print(self.server)
				self.port = 5555
				self.addr = (self.server, self.port)
				self.p = self.connect()
				#print(self.p)
			else:
				self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.server = server
				self.port = 5555
				self.addr = (self.server, self.port)
				self.p = self.connect()
				#print(self.p)

	def get_p(self):
		return self.p

	def search_servers(self, addr):
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #gotta make new socket else we get \/
			self.client.settimeout(0.1)									#[WinError 10022] An invalid argument was supplied
			self.client.settimeout(self.search_speed)						#[WinError 10022] An invalid argument was supplied
			self.p = self.client.connect(addr)
			#print(self.p)
			data = pickle.loads(self.client.recv(2048))
			return data
		except Exception as e:
			pass

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

	def str_send(self, data):
		try:
			self.client.send(str.encode(data))
		except socket.error as e:
			print(e)

	def recieve(self):
		try:
			return self.client.recv(2048)
		except:
			pass