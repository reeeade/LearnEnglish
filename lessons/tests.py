from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from lessons.models import Lesson, Question
from users.models import UserProgress


class LessonTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='<PASSWORD>', email='test@example.com')
        self.user.save()
        self.lesson = Lesson.objects.create(title='test', body='test')
        self.question1 = Question.objects.create(lesson=self.lesson, question='Question 1', correct_answer='Correct 1',
                                                 wrong_answers='Wrong 1|Wrong 2|Wrong 3')
        self.question2 = Question.objects.create(lesson=self.lesson, question='Question 2', correct_answer='Correct 2',
                                                 wrong_answers='Wrong 4|Wrong 5|Wrong 6')

    def test_all_lessons_handler_get(self):
        response = self.client.get(reverse('all_lessons'))
        self.assertEqual(response.status_code, 200)

    def test_lesson_details_handler_not_login_user(self):
        response = self.client.get(reverse('lesson_details', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'You must be logged in to access this page.')

    def test_lesson_details_handler_get(self):
        c = Client()
        c.login(username='test', password='<PASSWORD>')
        response = c.get(reverse('lesson_details', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson.html')
        self.assertContains(response, self.lesson.title)
        self.assertContains(response, self.question1.question)
        self.assertContains(response, self.question2.question)

    def test_lesson_details_handler_post(self):
        c = Client()
        c.login(username='test', password='<PASSWORD>')
        post_data = {f'question_{self.question1.id}': 'Correct 1',
                     f'question_{self.question2.id}': 'Correct 2'}
        response = c.post(reverse('lesson_details', args=[1]), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Question 1')
        self.assertContains(response, 'Correct 1')
        self.assertContains(response, 'Question 2')
        self.assertContains(response, 'Correct 2')
        user_progress = UserProgress.objects.filter(user=self.user, lesson=self.lesson).first()
        self.assertEqual(user_progress.score, 100)

    def test_lesson_details_handler_post_not_login_user(self):
        c = Client()
        post_data = {f'question_{self.question1.id}': 'Correct 1',
                     f'question_{self.question2.id}': 'Correct 2'}
        response = c.post(reverse('lesson_details', args=[1]), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'You must be logged in to access this page.')