from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = settings.AUTH_USER_MODEL
import datetime

# Create your models here.

class Tag(models.Model):
    tid = models.IntegerField()
    tagName = models.CharField(max_length=200, default="")

class Anime(models.Model):
    aid = models.IntegerField(default=0)
    title = models.CharField(max_length=200, default="")
    type = models.CharField(max_length=200, default="")
    episodes = models.IntegerField(default=0)
    # startDate = models.DateField()
    # endDate = models.DateField()
    seen = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=200, default="")
    tags = models.ManyToManyField(Tag)
    normalizedVector = models.CharField(max_length=500, default="")
    allTags = models.CharField(max_length=1000, default="")

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    average = models.DecimalField(max_digits=15, decimal_places=10, default=7.5)
    sid = models.CharField(max_length=10, default="")
    prefrenceVector = models.CharField(max_length=500, default="")
    tagTotal = models.CharField(max_length=500, default="")
    IDFvector =  models.CharField(max_length=500, default="")
