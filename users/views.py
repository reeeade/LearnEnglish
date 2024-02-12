from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from users.models import Score, UserProgress


# Create your views here.

def register_handler(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username already exists.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'Email already exists.'})
        user = User.objects.create_user(username=username, password=password, email=email,
                                        first_name=first_name, last_name=last_name)
        user.save()
        return render(request, 'login.html', {'success_message': 'You have successfully registered.'})
    else:
        return render(request, 'register.html')


def login_handler(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    else:
        if request.user.is_authenticated:
            return redirect('/user')
        return render(request, 'login.html')


def logout_handler(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def user_profile_handler(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if email != user.email and User.objects.filter(email=email).exists():
            return render(request, 'user_profile.html', {'error_message': 'Email already exists.'})
        if password != confirm_password:
            return render(request, 'user_profile.html', {'error_message': 'Passwords do not match.'})
        else:
            user.set_password(password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
    user = User.objects.get(username=request.user.username)

    user_scores = Score.objects.filter(user=user)
    if not user_scores:
        user_scores = Score(user=user, score=0)
        user_scores.save()
    return render(request, 'user_profile.html', {'user': user, 'user_scores': user_scores})


def user_delete_handler(request):
    return HttpResponse('Hello, world. You are at the user delete page.')
