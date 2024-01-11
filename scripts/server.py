import socket
from _thread import *
import sys
import pickle

from player import Player


server = "192.168.1.144"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)


s.listen(2)
print("Waiting for connection, Server Started")


players = [Player([50, 10]), Player([100, 10])]

class Data:
	def __init__(self):
		self.player_id = 0
		self.connections = []

d = Data()

def threaded_client(conn, player_id):
	conn.send(pickle.dumps(players[player_id]))
	reply = ""
	while 1:
		try:
			data = pickle.loads(conn.recv(2048))
			players[player_id] = data

			if not data:
				print("Disconnected")
				break
			else:
				if player_id == 0:
					reply = players[1]
				else:
					reply = players[0]

			conn.sendall(pickle.dumps(reply))
		except Exception as e:
			print(e)
			break

	print("Lost connection")
	conn.close()

	del d.connections[player_id]


def run(s, d):
	while 1:
		conn, addr = s.accept()
		print("Connected to:", addr)

		d.connections.append(0)
		start_new_thread(threaded_client, (conn, len(d.connections)-1))
		print(d.connections)
		#player_id += 1

start_new_thread(run, (s, d))