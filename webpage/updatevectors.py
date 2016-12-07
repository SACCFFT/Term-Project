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


import functions

def updateList():
	animeList = Anime.objects.all()

	avg = 0
	count = 0
	dbtags = []
	dblikes = []
	totalFreq = []

	for anime in animeList:
		print anime.title
		tags = []
		alltags = anime.tags.all()
		for tag in alltags:
			tags += [str(tag.tagName)]
		print tags
		tags = functions.preprocessing(tags)
		print tags
		totalFreq += [tags]

		vector = functions.stringToTag(anime.normalizedVector)
		dbtags += [vector]
		score = anime.score
		if score > 0:
			avg += score
			count += 1
			dblikes += [anime.score-6]
		else:
			dblikes += [0]

	avg /= Decimal(count * 1.0)
	u = User.objects.get(username='SACCFFT')
	print avg
	u.member.average = avg
	prefrences = functions.userVector(dbtags, dblikes)
	print prefrences
	u.member.prefrenceVector = functions.tagToString(prefrences)
	print
	tagFreq = functions.tagFreq(totalFreq)
	print tagFreq
	tagFrequency = functions.tagFreq(tagFreq)
	print tagFrequency
	u.member.tagTotal = functions.tagToString(tagFrequency)
	IDFvector = functions.IDFvector(tagFrequency, len(animeList))
	print IDFvector
	u.member.IDFvector = functions.tagToString(IDFvector)

	u.member.save()

#updateList()
