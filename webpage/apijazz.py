from backend.models import*
import socket, sys, zlib
import threading
import time
import functions
import random
from decimal import *

CLIENT = 'saccfft'
SERVER = 'api.anidb.net'
PORT = 9000
MYPORT = 9334
CLIENTVER = 1
PROTOVER = 3

target = (SERVER, PORT)

# Retrieves an anime based on its anime ID
def getAnime(sid, aid, amask='b0a880800e0000', MYPORT=9334):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	getAnime = 'ANIME aid='+str(aid)+'&amask='+amask+'&s='+str(sid)
	sock.sendto(getAnime, target)
	message = sock.recv(1400)
	return message

# Retrieves an anime based on it's title
def getAnimeWTitle(sid, title, amask='b0a880800e0000', MYPORT=9334):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	getAnime = 'ANIME aname='+title+'&amask='+amask+'&s='+str(sid)
	sock.sendto(getAnime, target)
	message = sock.recv(1400)
	return message

# Logs a user in to AniDB via the api
def login( user, password):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	print 'Login Requested'
	login = ('AUTH user='+ user + '&pass=' + password + '&protover=3&client=saccfft&clientver=1')
	sock.sendto(login, target)
	message = sock.recv(1400)
	print message
	print "Login request sent"
	return message

# Keeps getting random anime from AniDB's database until it returns one in which
# the affinity exceeds the tolerance level
def getRand(sid, prefrence, IDF, tolerance, cache=[], amask='b0a880800e0000', MYPORT=9334):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	allAnime = open('foo.txt').read().splitlines()
	affinity = -1
	while affinity < tolerance:
		time.sleep(2)
		get = random.choice(allAnime).split('|')
		aid = get[0]
		title = get[3]
		# print aid, title
		getAnime = 'ANIME aid='+str(aid)+'&amask='+amask+'&s='+str(sid)
		sock.sendto(getAnime, target)
		anime = sock.recv(1400)
		code = anime[:3]
		if code != '230':
			return (anime, -1)

		alltags = anime.split('|')[8]
		alltags = alltags.split(',')
		tags = functions.filterTags(alltags)
		tags = functions.preprocessing(tags)[0]
		tagVector = functions.getVector(tags)
		affinity = functions.evaluate(tagVector, prefrence, IDF)
		# print affinity
		# print cache

		for pref in cache:
			# print pref
			if len(pref) < 2:
				continue
			tag = pref[1:]
			add = False
			if '+'in pref:
				if tag in alltags:
					add = True
			else: # If minus
				if tag not in alltags:
					add = True

			if add:
				affinity *= Decimal(1.1)
			else:
				affinity *= Decimal(.9)
			# print affinity
	return (anime, affinity)

# Gets the description of a specified anime
def getDescription(sid, aid, MYPORT=9334):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	part = 0
	description = ""
	getDes = 'ANIMEDESC aid='+str(aid)+'&part='+str(part)+'&s='+str(sid)
	sock.sendto(getDes, target)
	anime = sock.recv(1400)
	code = anime[:3]
	if code != "233":
		return anime

	data = anime.split('|')
	description += data[2]
	maxPart = int(data[1])
	while part < maxPart:
		part += 1
		getDes = 'ANIMEDESC aid='+str(aid)+'&part='+str(part)+'&s='+str(sid)
		sock.sendto(getDes, target)
		anime = sock.recv(1400)
		data = anime.split('|')
		description += data[2]
	return functions.filterDescription(description)

# Logs a user out of AniDB
def logout(sid, MYPORT=9334):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', MYPORT))
	logout = "LOGOUT s="+str(sid)
	sock.sendto(logout, target)
	data = sock.recv(1400)
	return data

# An attempt to create an API link class and use multithreading for efficiency
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
