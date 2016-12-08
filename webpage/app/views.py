from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
import threading
from backend.models import *
import functions
import time
import apijazz
import updatevectors
from decimal import *

# Home page
class HomePage(View):
    def get(self, request):
		animeList = Anime.objects.all()
		playerList = []
		context = {}
		context["animeList"] = animeList
		context["user"] = request.user.username
		return render(request, 'home.html', context)

# Recommendation Page
class RecPage(View):
    def get(self, request, url=""):
		u = request.user.member
		tol = u.tolerance
		cache = u.context.split('|')
		print "Context:"
		print cache
		if len(url) > 0:
			print url
			if "same" in url:
				if url[0].equals('+'):
					tol *= Decimal(1.1)
				else:
					tol *= Decimal(.9)
				u.tolerance = tol
				u.save()
			else:
				cache += [url]
				print cache
				update = reduce(lambda a,b: a+'|'+b, cache[-5:])
				print update
				u.context = update
				u.save()

		context = {}
		prefrence = functions.stringToTag(u.prefrenceVector)
		IDF = functions.stringToTag(u.IDFvector)
		data = apijazz.getRand(u.sid, prefrence, IDF, tol, cache=cache)
		context["full"] = data[0]
		anime = data[0].split('|')
		code = anime[0][:3]
		if code != '230':
			return HttpResponseRedirect('/error/'+ code)

		context["anime"] = anime[3]
		context["type"] = anime[2]
		context["aired"] = anime[1]
		context["episodes"] = anime[6]
		context["affinity"] = data[1]
		alltags = anime[8]
		alltags = alltags.split(',')
		tags = functions.filterTags(alltags)
		context["tags"] = tags
		aid = anime[0].split()[2]
		context["description"] = apijazz.getDescription(u.sid, aid)
		context["aid"] = aid

		cache = u.context
		possibilities = functions.filterRelevant(tags, prefrence, cache)
		select = possibilities[0]
		prob = possibilities[1]
		if prob[0] == 0:
			context["learn"] = "same"
		else:
			context["learn"] = functions.randSelection(select, prob)[0]

		return render(request, 'rec.html', context)

# User's anime list
class ProfilePage(View):
	def get(self, request, url=""):
		animeList = Anime.objects.all()
		if url == "type":
			listOrder = functions.sortType(animeList)
		elif url == "seen":
			listOrder = functions.sortSeen(animeList)
		elif url == "status":
			listOrder = functions.sortStatus(animeList)
		elif url == "score":
			listOrder = functions.sortScore(animeList)
		else:
			listOrder = functions.sortAnime(animeList)



		context = {}
		context["animeList"] = listOrder
		context["user"] = request.user.username
		return render(request, 'index.html', context)

# Displays information on anime
class ViewAnime(View):
	def get(self, request, url=""):
		anime = Anime.objects.get(aid=int(url))
		context = {}
		context["anime"] = anime.title
		context["type"] = anime.type
		#context["aired"] = anime.
		context["episodes"] = anime.episodes
		allT = anime.allTags.split('|')
		#print allT
		tags = functions.filterTags(allT)
		#print tags
		context["tags"] = tags
		description = apijazz.getDescription(request.user.member.sid, anime.aid)
		context["description"] = description
		context["aid"] = anime.aid
		context["score"] = anime.score
		context["status"] = anime.status
		return render(request, 'anime.html', context)

# Login to API page
class LoginPage(View): #TODO: debug login later
	def get(self, request):
		context = {}
		context["sid"] = "Please Log In to Continue"
		return render(request, "login.html", context)

	def post(self, request):
		username = request.POST['userid']
		password = request.POST['pass']

		data = apijazz.login(username,password)
		command = data.split()
		if command[0] != '200' and command[0] != '201':
			return HttpResponseRedirect('/error/'+ command[0])
		print(command)
		sid = command[1]
		request.user.member.sid = sid
		request.user.member.context = ""
		request.user.member.save()
		user = authenticate(username=username, password=password)
		context = {}
		print(sid)
		context["sid"] = sid
		return render(request, "login.html", context)

# Add an anime to your DB page
class AddAnime(View):
	def get(self, request):
		return render(request, "addanime.html")

	def post(self, request):
		aid = request.POST['aid']
		title = request.POST['title']
		status = request.POST['status']
		seen = request.POST['seen']
		score = request.POST['score']
		print aid, title, status, seen, score
		if len(aid) == 0:
			anime = apijazz.getAnimeWTitle(request.user.member.sid, title)
		else:
			anime = apijazz.getAnime(request.user.member.sid, aid)
		command = anime[:3]
		if command != '230':
			return HttpResponseRedirect('/error/'+ command)

		if len(status) == 0: status = "Plan to Watch"
		if len(seen) == 0: seen = 0
		if len(score) == 0: score = 0

		anime = anime.split('|')
		aid = anime[0].split()[2]
		title = anime[3]
		type = anime[2]
		episodes = anime[6]
		alltags = anime[8]
		tags = functions.filterTags(alltags.split(','))
		setup = functions.preprocessing(tags)
		vector = functions.getVector(setup[0])
		exportVector = functions.tagToString(vector)
		temp = Anime(aid=aid,title=title,type=type,episodes=episodes,seen=seen,
			score=score,status=status,normalizedVector=exportVector,allTags=alltags)
		temp.save()
		for tagObject in tags:
			temp.tags.add(Tag.objects.get(tagName=tagObject))

		updatevectors.updateList()
		return HttpResponseRedirect('/anime/aid')

# Select an anime to edit
class SelectEdit(View):
	def get(self, request):
		return render(request, "selectanime.html")

	def post(self, request):
		aid = request.POST['aid']
		title = request.POST['title']
		if len(aid) == 0:
			aid = Anime.objects.get(title=title)
		return HttpResponseRedirect('/edit/anime/'+aid)

# Edit an anime
class EditAnime(View):
	def get(self, request, url=""):
		try:
			anime = Anime.objects.get(aid=int(url))
		except:
			return HttpResponseRedirect('/error/330')
		context = {}
		context["anime"] = anime.title
		context["aid"] = anime.aid
		return render(request, "editanime.html", context)

	def post(self, request, url=""):
		anime = Anime.objects.get(aid=int(url))
		status = request.POST['status']
		seen = request.POST['seen']
		score = request.POST['score']
		if len(status) != 0: anime.status = status
		if len(seen) != 0: anime.seen = int(seen)
		if len(score) != 0: anime.score = Decimal(score)
		anime.save()
		return HttpResponseRedirect('/anime/'+url)

class AddTags(View):
	def get(self, request):
		return render(request, "addtags.html")

	def post(self, request):
		tid = request.POST['tid']
		name = request.POST['title']
		if len(tid) == 0 or len(name) == 0:
			return HttpResponseRedirect('/error/237')
		tag = Tag(tid=tid,tagName=name)
		tag.save()
		#functions.addTag(tag)
		return HttpResponseRedirect('/profile')

# Not a page, but logs the user out
class Logout(View):
	def get(self, request):
		session = request.user.member.sid
		request.user.member.sid = -1

		data = apijazz.logout(session)
		code = data[:3]
		if code != '203':
			return HttpResponseRedirect('/error/'+ code)
		return HttpResponseRedirect('/login')

# Occurs AniDB returns an error
class ErrorPage(View):
	def get(self, request, url=""):
		context = {}
		context["error"] = url
		return render(request, "error.html", context)
