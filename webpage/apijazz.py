from backend.models import*
import socket, sys, zlib
import threading
import time
import constants
import random

CLIENT = 'saccfft'
SERVER = 'api.anidb.net'
PORT = 9000
MYPORT = 9334
CLIENTVER = 1
PROTOVER = 3

target = (SERVER, PORT)

def getAnime(sid, aid, amask='b0a880800e0000', MYPORT=9334):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	getAnime = 'ANIME aid='+str(aid)+'&amask='+amask+'&s='+str(sid)
	sock.sendto(getAnime, target)
	message = sock.recv(1400)
	return message

def getAnimeWTitle(sid, title, amask='b0a880800e0000', MYPORT=9334):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	getAnime = 'ANIME atitle='+title+'&amask='+amask+'&s='+str(sid)
	sock.sendto(getAnime, target)
	message = sock.recv(1400)
	return message

def login( user, password):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	print 'Login Requested'
	login = ('AUTH user='+ user + '&pass=' + password + '&protover=3&client=saccfft&clientver=1')
	sock.sendto(login, target)
	message = sock.recv(1400)
	print message
	print "T2 Login request sent"
	return message

def getRand(sid, prefrence, IDF, tolerance, amask='b0a880800e0000', MYPORT=9334):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	allAnime = open('foo.txt').read().splitlines()
	affinity = -1
	while affinity < tolerance:
		time.sleep(2)
		aid = random.choice(allAnime).split('|')[0]
		print aid
		getAnime = 'ANIME aid='+str(aid)+'&amask='+amask+'&s='+str(sid)
		sock.sendto(getAnime, target)
		anime = sock.recv(1400)
		code = anime[:3]
		if code != '230':
			return (anime, -1)
		alltags = anime.split('|')[8]
		alltags = alltags.split(',')
		tags = constants.filterTags(alltags)
		tags = constants.preprocessing(tags)[0]
		tagVector = constants.getVector(tags)
		affinity = constants.evaluate(tagVector, prefrence, IDF)
	# aid = 6564
	# getAnime = 'ANIME aid='+str(aid)+'&amask='+amask+'&s='+str(sid)
	# sock.sendto(getAnime, target)
	# anime = sock.recv(1400)
	# code = anime[:3]
	# if code != '230':
	# 	return (anime, -1)
	# alltags = anime.split('|')[8]
	# alltags = alltags.split(',')
	# tags = constants.filterTags(alltags)
	# tags = constants.preprocessing(tags)[0]
	# tagVector = constants.getVector(tags)
	# affinity = constants.evaluate(tagVector, prefrence, IDF)
	return (anime, affinity)

class AniDBLink(threading.Thread):

	def __init__(self):
		print "Testing AniDBLink"

		self.CLIENT = 'saccfft'
		self.SERVER = 'api.anidb.net'
		self.PORT = 9000
		self.MYPORT = 9334
		self.CLIENTVER = 1
		self.PROTOVER = 3
		self.target = (self.SERVER, self.PORT)

		super(AniDBLink, self).__init__()
		# Sets up internet and listening socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('', self.MYPORT))
		self.runListener = True
		self.message = ""
		self.flag = None
		self.sid = -1



		threading.Thread.__init__(self)
		print "setup complete"

	def run(self): # TODO: Know issue: listener does not recieve data?
		print "starting listener"
		while self.runListener:
			print "T2 listening"
			data = self.sock.recv(1400)
		print 'T2 quitting'

	def handleData(self, data):
		code = data[0:3]
		print "data recieved. Code: " + code
		self.message = data
		if self.flag != None:
			self.flag.set()	# Triggers flag and then destroys it
			self.flag = None

		# if code == '200' or code == '201':
		# 	self.sid = data.split()[1]
		# 	# TODO: Login Successful

	def setFlag(self, event): 	# In the case the sender is waiting on data,
		self.flag = event		# enables them to be notified when it is recieved

	def getData(self):
		return self.message

	def alreadyLogged(self,sid):
		self.sid = sid

	def logout(self):
		logout = 'LOGOUT s='+self.sid
		self.sock.sendto(logout, self.target)
		self.runListener = False
		self.sid = -1


	def getsid(self):
		return self.sid

	def __str__(self):
		return
