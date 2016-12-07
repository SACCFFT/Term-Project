import numpy
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import svm
from sklearn.datasets import samples_generator
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import make_pipeline
from backend.models import*
from decimal import *
import random

import socket, sys, zlib
import threading
import time
import math
import constant


def filterTags(alltags):
	storedTags = constant.getAllTags()
	tags = filter( lambda s: s.lower() in storedTags, alltags)
	return tags

def preprocessing(tags):
	storedTags = constant.getAllTags()
	organize = MultiLabelBinarizer(classes=storedTags)
	prefrences = organize.fit_transform([tags])
	return prefrences

def getVector(prefrences):
	getcontext().prec = 10

	val = sum(prefrences)
	if (val == 0):
		weight = 0
	else:
		weight = Decimal(1/(val)**.5).normalize()
	normalize = map(lambda x: x * weight, prefrences)
	return normalize

def userVector(animeList, likes):
	userPref = []
	for i in range(len(animeList[0])):
		attribute = 0
		for j in range(len(animeList)):
			attribute += animeList[j][i]*likes[j]
		userPref += [attribute]
	return userPref

def tagFreq(totalFreq):
	counts = []
	for i in range(len(totalFreq[0])):
		tagTotal = 0
		for j in range(len(totalFreq)):
			tagTotal += totalFreq[j][i]
		counts += [tagTotal]
	return counts

def IDFvector(counts, listSize):
	IDF = []
	for val in counts:
		print val
		if val <= 0:
			IDF += [0]
		else:
			IDF += [math.log10(Decimal(listSize)/val)] # TODO: Fix for colums of 0s
	return IDF

def evaluate(animeVector, userVector, IDFVector):
	prefrence = 0
	for i in range(len(userVector)):
		val = animeVector[i] * userVector[i] * IDFVector[i]
		prefrence +=val
	return prefrence

def tagToString(tags):
	temp = ''
	for tag in tags:
		temp += '|' + str(tag)

	return temp[1:]


def stringToTag(stringForm):
	tags = stringForm.split('|')
	for i in range(len(tags)):
		tags[i] = Decimal(tags[i])
	return tags

def sortAnime(animeList):
	return sorted(animeList, key=lambda anime: anime.title)

def sortType(animeList):
	tv = []
	movie = []
	ovaona = []
	special = []
	other = []
	for anime in animeList:
		type = anime.type
		if type == 'TV' or type == 'TV Series':
			tv += [anime]
		elif type == 'Movie':
			movie += [anime]
		elif type == 'OVA' or type == 'ONA':
			ovaona += [anime]
		elif type == 'Special':
			special += [anime]
		else:
			other += [anime]

	tv = sortAnime(tv)
	movie = sortAnime(movie)
	ovaona = sortAnime(ovaona)
	special = sortAnime(special)
	other = sortAnime(other)
	return tv + movie + ovaona + special + other

def sortSeen(animeList):
	animeList = sortAnime(animeList)
	return sorted(animeList, key=lambda anime: anime.seen / (anime.episodes+0.01))

def sortStatus(animeList):
	watching = []
	onhold = []
	ptw = []
	completed = []
	dropped = []
	animeList = sortAnime(animeList)
	for anime in animeList:
		status = anime.status
		if status == 'Watching':
			watching += [anime]
		elif status == 'On-Hold':
			onhold += [anime]
		elif status == 'Plan to Watch':
			ptw += [anime]
		elif status == 'Completed':
			completed += [anime]
		else:
			dropped += [anime]

	return watching + onhold + ptw + completed + dropped

def sortScore(animeList):
	animeList = sortAnime(animeList)[::-1]
	animeList.sort(key=lambda anime: anime.score)
	return animeList[::-1]


# def addTag(tag):
# 	name = tag.tagName
# 	storedTags = constant.getAllTags()
# 	index = 0
# 	while index < len(storedTags) and  name < storedTags[index]:
# 		index += 1
#
# 	lineNo = index + 3
# 	tagFile = open('constant.py')
# 	temp = tagFile.readlines()
# 	temp.insert(lineNo, '\t\t"'+name+'",')
#
# 	s.insert(index, name)
#
# 	animeList = Anime.objects.all()
# 	for anime in animeList:
# 		if name in anime.allTags:
# 			anime.tags.add(tag)
#
# 	updatevectors.updateList()


def testFilterTags():
	alltags = ['action','adventure','shonen','supernatural']
	testo = filterTags(alltags)
	print testo

# testFilterTags()
