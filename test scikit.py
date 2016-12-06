import numpy
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import svm
from sklearn.datasets import samples_generator
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import make_pipeline
import math

def p(l):
	for row in l:
		print(row)

tags = ['Action','Adventure','Comedy', 'empty','Drama','Historical','temp',
	'Mecha','Mystery','Parody','Romance','School','Sci-fi', 'misc',
	'Shonen','Slice Of Life','Sports','Supernatural']

organize = MultiLabelBinarizer(classes=tags)

Baccano = ['Action','Comedy','Historical','Mystery','Supernatural'] # Works w/
Bakemonogatari = ['Comedy','Mystery','Romance','School','Supernatural'] # sets
Barakamon = ['Comedy','Slice Of Life']								# as well
FLCL = ['Action','Comedy','Mecha','Parody','Sci-fi']
Haikyuu = ['Comedy','Drama','School','Shonen','Sports']
Noragami = ['Action','Adventure','Shonen','Supernatural']

mylist = [Baccano,Bakemonogatari,Barakamon,FLCL,Haikyuu,Noragami]

prefrences = organize.fit_transform(mylist)

print(prefrences)
'''
Imagine the 'tags' being the columns and 'shows' being row,
and a '1' indicating that yes, this show has this tag, or no, this show doesn't
have this tag
[[1 0 1 0 0 1 0 0 1 0 0 0 0 0 0 0 0 1]
 [0 0 1 0 0 0 0 0 1 0 1 1 0 0 0 0 0 1]
 [0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0]
 [1 0 1 0 0 0 1 0 0 1 0 0 1 0 0 0 0 0]
 [0 0 1 1 0 0 0 0 0 0 0 1 0 0 1 0 1 0]
 [1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1]]
 '''

# Ultimately predicts probability user will like show
# Adaptation on the Tf-IDF technique

ranking = [1,1,0,1,-1,0] # 1=like, -1=dislike. Can be adapted later

# Normalizes feilds to create vector
normalize = []
for features in prefrences:
	val = sum(features)
	weight = 1/(val)**.5
	altered = []
	for i in features:
		if i == 0:
			altered += [0]
		else:
			altered += [weight]

	normalize += [altered]

# Acccounts for what tags the user likes
userPref = []
for i in range(len(normalize[0])):
	attribute = 0
	for j in range(len(normalize)):
		attribute += normalize[j][i]*ranking[j]
	userPref += [attribute]

# Counts total instance of all tags
totalFreq = []
for i in range(len(prefrences[0])):
	tagTotal = 0
	for j in range(len(prefrences)):
		tagTotal += prefrences[j][i]
	totalFreq += [tagTotal]

# Calculates IDF statistic for each tag
IDF = []
for val in totalFreq:
	if val == 0:
		IDF += [0]
	else:
		IDF += [math.log10(6/val)]

p(normalize)
print()
print(userPref)
print()
print(totalFreq)
print()
print(IDF)
print()

# Multiplies user prefrence, IDF, and the particular show's weight
prediction = []
for show in normalize:
	pref = 0
	for i in range(len(show)):
		val = show[i] * userPref[i] * IDF[i]
		pref +=val
	prediction += [pref]

print(prediction)
