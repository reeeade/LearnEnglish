"""
URL configuration for LearnEnglish project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from words import views

urlpatterns = [
    path('', views.Words.as_view(), name='all_words'),
    path('<int:word_id>/', views.word_checker, name='word_checker'),
    path('delete/', views.word_delete, name='word_delete'),
    path('random/', views.random_word, name='random_word')
]
