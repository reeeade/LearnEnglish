import copy
import random

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from lessons.models import Lesson, Question
from users.score_utils import update_score


# Create your views here.

def all_lessons_handler(request):
    all_lessons = Lesson.objects.all()
    return render(request, 'all_lessons.html', {'all_lessons': all_lessons})


class LessonDetails(View):
    def get(self, request, lesson_id):
        if not request.user.is_authenticated:
            return render(request, 'login.html', {'error_message': 'You must be logged in to access this page.'})
        lesson = Lesson.objects.get(pk=lesson_id)
        questions = Question.objects.filter(lesson=lesson).all()
        adjusted_questions = []
        for question in questions:
            current_question = {'question': question.question, 'id': question.id}
            all_answers = [question.correct_answer] + question.wrong_answers.split('|')
            random.shuffle(all_answers)
            current_question['answers'] = all_answers
            adjusted_questions.append(copy.deepcopy(current_question))
        lesson_content = {'lesson': lesson, 'questions': adjusted_questions}
        return render(request, 'lesson.html', lesson_content)

    def post(self, request, lesson_id):
        if not request.user.is_authenticated:
            return render(request, 'login.html', {'error_message': 'You must be logged in to access this page.'})
        lesson = Lesson.objects.get(pk=lesson_id)
        questions = Question.objects.filter(lesson=lesson)
        results = {}
        total_questions = len(questions)
        correct_answer = 0
        for question in questions:
            is_correct = True if request.POST[f'question_{question.id}'] == question.correct_answer else False
            if is_correct:
                correct_answer += 1
            result_text = (f'{question.question} , you answered is {request.POST[f'question_{question.id}']}.'
                           f' The correct answer is {question.correct_answer}.')
            results[question.id] = {'is_correct': is_correct, 'text': result_text}
        result_score = correct_answer / total_questions * 100
        update_score(request.user.username, result_score, lesson_id)
        return render(request, 'lesson_answers.html', {'results': results.values(), 'result_score': result_score})
