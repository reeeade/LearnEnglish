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

from users import views

urlpatterns = [
    path('login/', views.login_handler, name='login'),
    path('register/', views.register_handler, name='register'),
    path('logout/', views.logout_handler, name='logout'),
    path('user/', views.user_profile_handler, name='user_profile'),
    path('user/delete', views.user_delete_handler, name='user_delete'),
]
