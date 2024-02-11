from django.db import models


# Create your models here.

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()


class Question(models.Model):
    question = models.TextField()
    correct_answer = models.TextField()
    wrong_answers = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
