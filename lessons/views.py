from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def all_lessons_handler(request):
    return HttpResponse('All lessons')


def lesson_details_handler(request, lesson_id):
    return HttpResponse(f'Lesson {lesson_id}')
