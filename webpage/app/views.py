from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
import threading
from backend.models import *
import constants
import time
import apijazz

class HomePage(View):
    def get(self, request):
		animeList = Anime.objects.all()
		playerList = []
		context = {}
		context["animeList"] = animeList
		context["user"] = request.user.username
		return render(request, 'home.html', context)

class RecPage(View):
    def get(self, request):
		tolerance = 0.01
		context = {}
		prefrence = constants.stringToTag(request.user.member.prefrenceVector)
		IDF = constants.stringToTag(request.user.member.IDFvector)
		data = apijazz.getRand(request.user.member.sid, prefrence, IDF, tolerance )
		#anime = apijazz.getAnime(request.user.member.sid, 6564,('api.anidb.net',9000) )
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
		tags = constants.filterTags(alltags)
		context["tags"] = tags


		return render(request, 'rec.html', context)

class ProfilePage(View):
	def get(self, request):
		animeList = Anime.objects.all()
		playerList = []
		context = {}
		context["animeList"] = animeList
		context["user"] = request.user.username
		return render(request, 'index.html', context)

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
		request.user.member.save()
		user = authenticate(username=username, password=password)
		context = {}
		print(sid)
		context["sid"] = sid
		return render(request, "login.html", context)

class AddAnime(View):
	def get(self, request):
		return render(request, "addanime.html")

	def post(self, request):
		aid = request.POST['aid']
		title = request.POST['title']

		if len(aid) > 0:
			anime = apijazz.getAnime(request.user.member.sid, aid)
		else:
			anime = apijazz.getAnimeWTitle(request.user.member.sid, title)
		command = anime[:3]
		if command != '230':
			return HttpResponseRedirect('/error/'+ command)
		context = {}
		print(sid)
		context["sid"] = sid
		return HttpResponseRedirect('/profile')

class Logout(View):
	def get(self, request):
		session = request.user.member.sid
		request.user.member.sid = -1

		apijazz.logout(session)
		context = {}
		context["animeList"] = []
		context["user"] = "Please log in to continue"

class ErrorPage(View):
	def get(self, request, url=""):
		context = {}
		context["error"] = url
		return render(request, "error.html", context)
