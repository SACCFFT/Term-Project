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


global Taglist
Taglist = [
		"action",
		"adventure",
		"agnst",
		"anthropomorphism",
		"blackmail",
		"brainwashing",
		"comedy",
		"competition",
		"contemporary fantasy",
		"deconstruction",
		"detective",
		"ecchi",
		"educational",
		"fantasy",
		"gender bender",
		"harem",
		"henshin",
		"horror",
		"magical girl",
		"magical realism",
		"melodrama",
		"mono no aware",
		"mystery",
		"neo-noir",
		"parasite",
		"reverse harem",
		"romance",
		"science fiction",
		"social commentary",
		"super power",
		"thriller",
		"torture,"
		"tragedy",
		]

def filterTags(alltags):
	tags = filter( lambda s: s.lower() in Taglist, alltags)
	return tags

def preprocessing(tags):
	organize = MultiLabelBinarizer(classes=Taglist)
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


def testFilterTags():
	alltags = ['Action','Adventure','Shonen','Supernatural']
	testo = filterTags(alltags)
	print testo

# testFilterTags()
