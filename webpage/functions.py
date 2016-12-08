import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django
django.setup()
import numpy
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import svm
from sklearn.datasets import samples_generator
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import make_pipeline
from backend.models import*
from decimal import *
import copy
import random
import string

import socket, sys, zlib
import threading
import time
import math
import constant

# Takes a list of tags and of those only returns the ones the system uses
def filterTags(alltags):
	storedTags = constant.getAllTags()
	tags = filter( lambda s: s.lower() in storedTags, alltags)
	return tags

# Takes a list of tags and turns them into a list of 0s and 1s representing the
# presence or lackthereof a tag
def preprocessing(tags):
	storedTags = constant.getAllTags()
	organize = MultiLabelBinarizer(classes=storedTags)
	prefrences = organize.fit_transform([tags])
	return prefrences

# Takes a list of 0s and 1s and weights the tag based on how many there are
def getVector(prefrences):
	getcontext().prec = 10

	val = sum(prefrences)
	if (val == 0):
		weight = 0
	else:
		weight = Decimal(1/(val)**.5).normalize()
	normalize = map(lambda x: x * weight, prefrences)
	return normalize

# Takes a 2D list of all anime watched and multiplies them by how much the user
# liked that anime and sums them to obtain a vector ow what the user likes
def userVector(animeList, likes):
	userPref = []
	for i in range(len(animeList[0])):
		attribute = 0
		for j in range(len(animeList)):
			attribute += animeList[j][i]*likes[j]
		userPref += [attribute]
	return userPref

# Takes a 2D list of anime and returns the counts of each tag
def tagFreq(totalFreq):
	counts = []
	for i in range(len(totalFreq[0])):
		tagTotal = 0
		for j in range(len(totalFreq)):
			tagTotal += totalFreq[j][i]
		counts += [tagTotal]
	return counts

# Takes counts of all anime and the size of the db and calculates a vector that
# represents the frequency of all tags
def IDFvector(counts, listSize):
	IDF = []
	for val in counts:
		print val
		if val <= 0:
			IDF += [0]
		else:
			IDF += [math.log10(Decimal(listSize)/val)]
	return IDF

# Multiplies anime, prefrence, and IDF vector to predict how much a user will
# like an anime
def evaluate(animeVector, userVector, IDFVector):
	prefrence = 0
	for i in range(len(userVector)):
		val = animeVector[i] * userVector[i] * IDFVector[i]
		prefrence +=val
	return prefrence

# Converts vector to string format to store in database
def tagToString(tags):
	temp = ''
	for tag in tags:
		temp += '|' + str(tag)

	return temp[1:]

# Converts a vector's string representation to the original vector
def stringToTag(stringForm):
	tags = stringForm.split('|')
	for i in range(len(tags)):
		tags[i] = Decimal(tags[i])
	return tags

# Sorts list of anime based on title
def sortAnime(animeList):
	return sorted(animeList, key=lambda anime: anime.title)

# Sorts anime based on release format
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

# Sorts anime based on percentage of episodes seen
def sortSeen(animeList):
	animeList = sortAnime(animeList)
	return sorted(animeList, key=lambda anime: anime.seen / (anime.episodes+0.01))

# Sorts anime based on their watch status
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

# Sorts anime based on their score
def sortScore(animeList):
	animeList = sortAnime(animeList)[::-1]
	animeList.sort(key=lambda anime: anime.score)
	return animeList[::-1]

# Takes a list of tags from an anime and weights each tag based on how much
# the user likes that tag
def filterRelevant(tags, prefrenceVector, context):
	storedTags = constant.getAllTags()
	preWeight = copy.copy(prefrenceVector)
	vector = preprocessing(tags)[0]
	index = 0
	pos = 0
	while index < len(vector):
		if (vector[index] == 0):
			preWeight.pop(pos)
		else:
			pos += 1
		index += 1

	# print tags
	# print vector
	# print preWeight
	# print tags

	index = 0
	for i in range(len(tags)):
		if tags[i] in context:
			preWeight.pop(index)
		else:
			index += 1

	tags = filter(lambda tag: tag not in context, tags)

	total = sum(preWeight)
	if total > 0:
		weight = map(lambda mass: mass/total, preWeight)
	else:
		weight = [0]
	print preWeight
	print weight
	return [tags,weight]

# Takes a list of tags and chooses ones based on their respective probabilities
def randSelection(tags, probabilities):
	return numpy.random.choice(tags, 1, p=probabilities)

# Takes out any [***] and <*****> bits from the anime description
def filterDescription(des):
	print des
	print "testo"
	place = des.find('[')
	print place
	while place != -1:
		print place
		end = des.find(']')
		des = des[:place] + des[end+1:]
		print des
		place = des.find('[')

	place = des.find('<')
	print place
	while place != -1:
		place
		end = des.find('>')
		des = des[:place] + des[end+1:]
		place = des.find('<')

	return des



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

def testFilterRelevant():
	nise = Anime.objects.get(aid=8658)
	tags = filterTags(nise.allTags.split('|'))
	pref = "48.86830064|15.82623284|0E-10|6.187125661|0.9113576738|2.449489743|72.84816161|3.572350929|17.24065943|1.060660172|4.938870563|43.94697121|0E-10|32.39488195|2.572425527|20.71556840|5.355611231|2.702805431|0.5875606843|0.8164965810|3.788854382|2.309401077|0.7071067812|0E-10|1.353553391|2.632993162|70.35851902|28.90860039|5.191597590|15.73481944|1.760045373|0E-10"
	vector = stringToTag(pref)
	context = ""
	print tags
	print vector
	result = filterRelevant(tags,vector,context)
	print result

	selection = randSelection(result[0],result[1])
	print selection

	context = "+contemporary fantasy|+u'action|-fantasy|-harem|+comedy|-ecchi|+romance"
	result = filterRelevant(tags,vector,context)
	print result

# testFilterTags()
# testFilterRelevant()
