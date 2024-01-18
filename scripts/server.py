import socket
from _thread import *
import sys
import pickle

from player import Player
from enemy import Enemy


server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)


s.listen(3)
print("Waiting for connection, Server Started")


enemy = Enemy()
players = [Player([50, 10], '1'), Player([100, 10], '2'), Player([100, 10], '3')]

class Data:
	def __init__(self):
		self.player_id = 0
		self.connections = []

d = Data()

def threaded_client(conn, player_id):
	if player_id != 0:
		players[player_id].enemy = players[player_id].enemy
	conn.send(pickle.dumps(players[player_id]))
	#print('sent play obj')
	reply = []
	while 1:
		try:
			data = pickle.loads(conn.recv(2048))
			players[player_id] = data
			players[1].enemy = players[0].enemy
			players[2].enemy = players[0].enemy

			if not data:
				#print("Disconnected")
				break
			else:
				# update the enemies in the other player classes
				if player_id == 0:
					reply = [players[1], players[2]]
				elif player_id == 1:
					reply = [players[0], players[2]]
				elif player_id == 2:
					reply = [players[0], players[1]]

			conn.sendall(pickle.dumps(reply))
		except Exception as e:
			print(e)
			break

	#print("Lost connection")
	conn.close()

	del d.connections[player_id]


def run(s, d):
	while 1:
		conn, addr = s.accept()
		#print("Connected to:", addr)

		d.connections.append(0)
		start_new_thread(threaded_client, (conn, len(d.connections)-1))
		#print(f'Players connected: {len(d.connections)}')

start_new_thread(run, (s, d))