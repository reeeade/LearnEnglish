import random

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from words.forms import PartialArticleForm
from words.models import UserDict


# Create your views here.

class Words(View):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return render(request, 'login.html', {'error_message': 'You must be logged in to access this page.'})
        user = User.objects.get(username=request.user.username)
        all_words = UserDict.objects.filter(user=user)
        form_template = PartialArticleForm()
        return render(request, 'words.html', {'all_words': all_words, 'form_template': form_template})

    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return render(request, 'login.html', {'error_message': 'You must be logged in to access this page.'})
        user = User.objects.get(username=request.user.username)
        new_form = UserDict(user=user)
        word_form = PartialArticleForm(request.POST, instance=new_form)
        word = request.POST.get('word')
        if UserDict.objects.filter(word=word, user=user).exists():
            messages.error(request, 'Word already exists.')
            return redirect('all_words')

        if word_form.is_valid():
            word_form.save()
        messages.success(request, 'Word added successfully.')
        return redirect('all_words')


def word_detail(request, word_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'error_message': 'You must be logged in to access this page.'})
    user = User.objects.get(username=request.user.username)
    message = ''
    if request.method == 'POST':
        test_word_id = request.POST.get('word_id')
        test_translation = request.POST.get('translate')

        test_word_in_db = UserDict.objects.get(pk=test_word_id, user=user)
        if test_word_in_db.translation == test_translation:
            messages.success(request,
                             f'You are correct. Answer for "{test_word_in_db.word}" is "{test_translation}"')
        else:
            messages.error(request,
                           f'You are incorrect. Answer for "{test_word_in_db.word}" is not "{test_translation}". '
                           f'Should be "{test_word_in_db.translation}"')
    all_user_words = UserDict.objects.filter(user=user).all()
    random_word = random.choice(all_user_words)
    random_id = random_word.pk

    current_word = UserDict.objects.get(pk=word_id)
    return render(request, 'word.html', {'word': current_word, 'random_id': random_id,
                                         'message': message})


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
