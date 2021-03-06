from backend.models import*
import socket, sys, zlib
import threading
import time
import functions

CLIENT = 'saccfft'
SERVER = 'api.anidb.net'
PORT = 9000
MYPORT = 9334
CLIENTVER = 1
PROTOVER = 3

target = (SERVER, PORT)

# A class that connects to the AniDB database and retrieves information
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

	def run(self): # Sets up listener
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

	# Logs user into AniDB
	def login(self, user, password):
		print 'T2 Login Requested'
		if not self.runListener: #If listener is not running, restarts it
			self.runListener = True
			self.run()

		login = ('AUTH user='+user+'&pass='+password+'&protover=3&client=saccfft&clientver=1')
		login += user
		self.sock.sendto(login, self.target)
		self.message = self.sock.recv(1400)
		print "T2 Login request sent"
		return self.message

	# If the user is already logged, can hardcode session key here
	def alreadyLogged(self,sid):
		self.sid = sid

	# Logs user out of AniDB
	def logout(self):
		logout = 'LOGOUT s='+self.sid
		self.sock.sendto(logout, self.target)
		self.runListener = False
		self.sid = -1

	# Gets an anime from AniDB
	def getAnime(self, title, amask='b0a880800e0000'):
		try:
			getAnime = 'ANIME aname='+title+'&amask='+amask+'&s='+str(self.sid)
			self.sock.sendto(getAnime, self.target)
			self.message = self.sock.recv(1400)
			return self.message
		except:
			print "Can not send"
			return "330 NO SUCH ANIME"

	# Gets a random unwatched anime
	def getRand(self):
		random = 'RANDOMANIME type=2&s='+self.sid
		self.sock.sendto(random, self.target)

	# Returns session ID
	def getsid(self):
		return self.sid

	def __str__(self):
		return
