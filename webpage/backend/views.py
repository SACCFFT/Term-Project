from django.shortcuts import render
from backend.models import*
from apijazz import *


# Create your views here.
class HomePage(View):
    def get(self, request):

		animeList = Anime.objects.all()
		playerList = []
		context = {}
		context["animeList"] = animeList
		context["user"] = request.user.username
		print animeList
		return render(request, 'index.html', context)

class RecPage(View):
    def get(self, request):
		context = {}
		return render(request, 'index.html', context)



class LoginPage(View):
	def get(self, request):
		context = {}
		session = request.user.member.sid
		if ( session == -1):
			context["sid"] = "Please Log In to Continue"
		else:
			context["sid"] = "Currently logged in under sID "+ str(session)
		return render(request, "login.html", context)

	def post(self, request):
		username = request.POST['userid']
		password = request.POST['pass']
		sid = apijazz.login(username,password)
		user = authenticate(username=username, password=password)
		context = {}
		context["sid"] = sid
		return render(request, "login.html", context)

class Logout(View):
	def get(self, request):
		session = request.user.member.sid
		request.user.member.sid = -1

		apijazz.logout(session)
		context = {}
		context["animeList"] = []
		context["user"] = "Please log in to continue"
