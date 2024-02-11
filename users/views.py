from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def register_handler(request):
    return HttpResponse('Hello, world. You are at the register page.')


def login_handler(request):
    return HttpResponse('Hello, world. You are at the login page.')


def logout_handler(request):
    return HttpResponse('Hello, world. You are at the logout page.')


def user_profile_handler(request):
    return HttpResponse('Hello, world. You are at the user profile page.')


def user_delete_handler(request):
    return HttpResponse('Hello, world. You are at the user delete page.')
