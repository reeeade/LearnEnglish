from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from words.models import UserDict


# Create your views here.

class Words(View):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return render(request, 'login.html', {'error_message': 'You must be logged in to access this page.'})
        user = User.objects.get(username=request.user.username)
        all_words = UserDict.objects.filter(user=user)
        return render(request, 'words.html', {'all_words': all_words})

    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return render(request, 'login.html', {'error_message': 'You must be logged in to access this page.'})
        word = request.POST.get('word')
        translation = request.POST.get('translation')
        transcription = request.POST.get('transcription')
        transliteration = request.POST.get('transliteration')
        user = User.objects.get(username=request.user.username)
        if UserDict.objects.filter(word=word, user=user).exists():
            all_words = UserDict.objects.filter(user=user)
            messages.error(request, 'Word already exists.')
            return redirect('all_words')
        db_word = UserDict(word=word, user=user, translation=translation,
                           transcription=transcription, transliteration=transliteration)
        db_word.save()
        all_words = UserDict.objects.filter(user=user)
        messages.success(request, 'Word added successfully.')
        return redirect('all_words')


def word_detail(request, word_id):
    return HttpResponse(f"Word {word_id}")


def word_delete(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'error_message': 'You must be logged in to access this page.'})
    word = request.POST.get('word')
    user = User.objects.get(username=request.user.username)
    try:
        db_word = UserDict.objects.get(word=word, user=user)
        db_word.delete()
        messages.success(request, 'Word deleted successfully.')
    except UserDict.DoesNotExist:
        messages.error(request, 'Word does not exist.')

    all_words = UserDict.objects.filter(user=user)
    return redirect('all_words')
