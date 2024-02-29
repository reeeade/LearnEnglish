import re

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse

from users.models import Score
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


class TestRandomWordView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test', email='test@example.com')
        self.user.save()
        self.word1 = UserDict(user=self.user, word='test', translation='test', transcription='test',
                              transliteration='test', audio='test')
        self.word1.save()
        self.word2 = UserDict(user=self.user, word='test2', translation='test2', transcription='test2',
                              transliteration='test2', audio='test2')
        self.word2.save()

    def test_random_word_view_get(self):
        c = Client()
        c.login(username='test', password='test')
        for _ in range(100):
            response = c.get(reverse('random_word'), follow=True)
            self.assertEqual(response.status_code, 200)
            r_chain = response.redirect_chain
            redirect_path, redirect_code = r_chain[0]
            words_ids = [str(self.word1.id), str(self.word2.id)]
            clear_path = redirect_path.replace('/words/', '')
            self.assertIn(clear_path, words_ids)


class TestWordCheckerView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test', email='test@example.com')
        self.user.save()
        self.word1 = UserDict(user=self.user, word='test', translation='test', transcription='test',
                              transliteration='test', audio='test')
        self.word1.save()
        self.word2 = UserDict(user=self.user, word='test2', translation='test2', transcription='test2',
                              transliteration='test2', audio='test2')
        self.word2.save()

    def test_word_checker_view_get(self):
        c = Client()
        c.login(username='test', password='wrong')
        response = c.get(reverse('word_checker', kwargs={'word_id': str(self.word1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'You must be logged in to access this page.')

    def test_word_checker_view_post(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.post(reverse('word_checker', kwargs={'word_id': str(self.word1.id)}),
                          {'word_id': str(self.word1.id), 'translate': 'test'})
        html = response.content.decode('utf-8')
        results = re.findall(r'<form method="post" action="/words/\d+/">', html)
        results_str = results[0].replace('<form method="post" action="/words/', '')
        results_str = results_str.replace('/">', '')
        self.assertEqual(results_str, str(self.word2.id))

    def test_word_checker_view_post_correct_answer(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.post(reverse('word_checker', kwargs={'word_id': str(self.word1.id)}),
                          {'word_id': str(self.word1.id), 'translate': 'test'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('You are correct.', str(messages[0]))
        user_score = Score.objects.get(user=self.user)
        self.assertEqual(user_score.score, 1)

    def test_word_checker_view_post_incorrect_answer(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.post(reverse('word_checker', kwargs={'word_id': str(self.word1.id)}),
                          {'word_id': str(self.word1.id), 'translate': 'test2'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('You are incorrect.', str(messages[0]))
        user_score = Score.objects.get(user=self.user)
        self.assertEqual(user_score.score, -1)


class TestWordDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test', email='test@example.com')
        self.user.save()
        self.word1 = UserDict(user=self.user, word='test', translation='test', transcription='test',
                              transliteration='test', audio='test')
        self.word1.save()
        self.word2 = UserDict(user=self.user, word='test2', translation='test2', transcription='test2',
                              transliteration='test2', audio='test2')
        self.word2.save()

    def test_word_delete_view(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.post(reverse('word_delete'), {'word': str(self.word1.word)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('all_words'))
        deleted_word = UserDict.objects.filter(word='test', user=self.user).first()
        self.assertIsNone(deleted_word)

    def test_word_delete_view_not_login_user(self):
        c = Client()
        c.login(username='test', password='<PASSWORD>')
        response = c.post(reverse('word_delete'), {'word': str(self.word1.word)})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'You must be logged in to access this page.')
