from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse

from words.models import UserDict


class TestWordView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test', email='test@example.com')
        self.user.save()

    def test_word_view_get(self):
        c = Client()
        c.login(username='test', password='<PASSWORD>')
        response = c.get(reverse('all_words'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'You must be logged in to access this page.')

    def test_word_view_post(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.post(reverse('all_words'),
                          {'word': 'test', 'translation': 'test', 'transcription': 'test', 'transliteration': 'test',
                           'audio': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('all_words'))
        saved_word = UserDict.objects.get(word='test', user=self.user)
        self.assertEqual(saved_word.word, 'test')
        self.assertEqual(saved_word.translation, 'test')
        self.assertEqual(saved_word.transcription, 'test')
        self.assertEqual(saved_word.transliteration, 'test')
        self.assertEqual(saved_word.audio, 'test')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Word added successfully.')

    def test_word_view_post_not_login_user(self):
        c = Client()
        c.login(username='test', password='<PASSWORD>')
        response = c.post(reverse('all_words'),
                          {'word': 'test', 'translation': 'test', 'transcription': 'test', 'transliteration': 'test',
                           'audio': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'You must be logged in to access this page.')

    def test_word_view_post_invalid_word(self):
        c = Client()
        c.login(username='test', password='test')
        user = User.objects.get(username=self.user.username)
        d_word = UserDict(user=user, word='test', translation='test', transcription='test',
                          transliteration='test', audio='test')
        d_word.save()
        response = c.post(reverse('all_words'),
                          {'word': 'test', 'translation': 'test', 'transcription': 'test', 'transliteration': 'test',
                           'audio': 'test'})
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Word already exists.')
        self.assertEqual(response.url, reverse('all_words'))
