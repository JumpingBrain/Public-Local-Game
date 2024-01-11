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

def threaded_client(conn, player_id):
	print(f'You are player #{player_id}')
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


player_id = 0
while 1:
	conn, addr = s.accept()
	print("Connected to:", addr)

	start_new_thread(threaded_client, (conn, player_id))
	player_id += 1