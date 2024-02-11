from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def all_words(request):
    return HttpResponse("All words")


def word_detail(request, word_id):
    return HttpResponse(f"Word {word_id}")
