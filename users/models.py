from django.contrib.auth.models import User
from django.db import models

from lessons.models import Lesson


# Create your models here.

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
