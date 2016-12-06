# Gets anime list from an XML file
import os
# This must be executed before the import below
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django
django.setup()
from lxml import etree
from backend.models import *
from decimal import *
from django.apps import apps
import threading
import time
from AniDBLink import *
from django.db import models
from django.contrib.auth.models import User


import constants

#settings.configure()

listName = "/Users/ryan/Documents/Fresh Sem1/CS/Term Project/webpage/animelist_1479685660_-_3715245.xml"
mylist = etree.parse(listName)
listedAnime = mylist.findall('anime')
# print mylist
# print listedAnime

CLIENT = 'saccfft'
SERVER = 'api.anidb.net'
PORT = 9000
MYPORT = 9334
CLIENTVER = 1
PROTOVER = 3
target = (SERVER, PORT)

username = 'SACCFFT'
password = 'CheeseCakeSteak'
tagamask = '800000000e0000'

avg = 0
count = 0
dbtags = []
dblikes = []
totalFreq = []


print "Starting..."
listSetup = AniDBLink() #Set up Anidb Link
#listSetup.start()

# logStatus = threading.Event() #Tries to login
# listSetup.setFlag(logStatus)
# data = listSetup.login(username, password)
# logStatus.wait()

# #If already logged in, can hardcode SID to avoid logging in again
sid = "qe5yC"
listSetup.alreadyLogged(sid)
code = 200

status = listSetup.getData()
print status
code = status[:3]



if code == 500:
	print "failed"
else:

	# sid = listSetup.getsid()
	# print sid

	failedAnime = []

	for anime in listedAnime:
		title = anime.findtext('series_title')
		type = anime.findtext('series_type')
		episodes = anime.findtext('series_episodes')
		seen = anime.findtext('my_watched_episodes')
		score = Decimal(anime.findtext('my_score'))
		status = anime.findtext('my_status')
		print title

		data= listSetup.getAnime(title,amask=tagamask)
		data = data.split('|')
		print data[0]
		if data[0][:3] != "230":
			print "does not exist"
			failedAnime += anime
			time.sleep(2)
			continue
		aid = int(data[0].split()[2])
		print aid
		alltags = data[1].split(',')
		tags = constants.filterTags(alltags)
		temp = constants.preprocessing(tags)
		vector = constants.getVector(temp[0])
		exportVector = constants.tagToString(vector)
		totalFreq += [temp]
		dbtags += [vector]
		dblikes += [score-6] #TODO: Refine like/dislike weighting


		if score > 0:
			avg += score
			count += 1
			dblikes += [score-6]
		else:
			dblikes += [0]

		temp = Anime(aid=aid,title=title,type=type,episodes=episodes,seen=seen,
			score=score,status=status,normalizedVector=exportVector,allTags=alltags)
		temp.save()
		for tagObject in tags:
			temp.tags.add(Tag.objects.get(tagName=tagObject))

		time.sleep(2)

	avg /= Decimal(count * 1.0)
	u = User.objects.get(username='SACCFFT')
	print avg
	u.member.average = avg
	prefrences = constants.userVector(dbtags, dblikes)
	print prefrences
	u.member.prefrenceVector = constants.tagToString(prefrences)
	print
	tagFrequency = constants.tagFreq(totalFreq)
	print tagFrequency
	u.member.tagTotal = constants.tagToString(tagFrequency)
	IDFvector = constants.IDFvector(tagFrequency)
	print IDFvector
	u.member.IDFvector = constants.tagToString(IDFvector, len(listedAnime)-len(failedAnime))

	u.member.save()

	print "Please manually enter the following:"
	for anime in failedAnime:
		print anime.findtext('series_title')

	# animeTagStatus = threading.Event()
	# listSetup.setFlag(animeTagStatus)
	# animeTagStatus.wait()
	#
	# alltags = listSetup.getData()
