import socket, sys, zlib
import threading
import time

CLIENT = 'saccfft'
SERVER = 'api.anidb.net'
PORT = 9000
MYPORT = 9334
CLIENTVER = 1
PROTOVER = 3

target = (SERVER, PORT)
print 'Initialized...',
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', MYPORT))
print 'Listening!'
while True:
	data = sock.recv(1400)
	print (data)