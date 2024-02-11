from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserDict(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=50)
    translation = models.CharField(max_length=50)
    transcription = models.CharField(max_length=50)
    transliteration = models.CharField(max_length=50)
    audio = models.CharField(max_length=255)


