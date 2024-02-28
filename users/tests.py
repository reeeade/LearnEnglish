from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, Client

from users.forms import UserRegisterForm


class TestUserRegistration(TestCase):

    def test_register_handler(self):
        c = Client()
        response = c.post('/register/', {'username': 'test', 'password': 'test', 'confirm_password': 'test',
                                         'email': 'test@example.com', 'first_name': 'test', 'last_name': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='test').exists())

    def test_register_handler_invalid_form(self):
        c = Client()
        response = c.post('/register/',
                          {'username': 'testuser', 'password': 'testpassword', 'confirm_password': 'wrongpassword',
                           'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'})

        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertFalse(User.objects.filter(email='test@example.com').exists())
        self.assertContains(response, 'Passwords do not match.')
        self.assertIsInstance(response.context['form_template'], UserRegisterForm)

    def test_register_handler_get(self):
        c = Client()
        response = c.get('/register/')
        self.assertEqual(response.status_code, 200)


class TestUserLogin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.user.save()

    def test_login_handler(self):
        c = Client()
        response = c.post('/login/', {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(authenticate(username='test', password='test'))
        self.assertEqual(response.url, '/user')

    def test_login_handler_invalid_credentials(self):
        c = Client()
        response = c.post('/login/', {'username': 'test', 'password': '<PASSWORD>'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(authenticate(username='test', password='<PASSWORD>'))
        self.assertEqual(response.request['PATH_INFO'], '/login/')

    def test_login_handler_get(self):
        c = Client()
        response = c.get('/login/')
        self.assertEqual(response.status_code, 200)


class TestUserLogout(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.user.save()

    def test_logout_handler(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(c.logout())
        self.assertEqual(response.url, '/login')


class TestUserProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.user2 = User.objects.create_user('test2', 'test2@example.com', 'test2')
        self.user.save()
        self.user2.save()

    def test_user_profile_handler(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.post('/user/',
                          {'password': 'test1', 'confirm_password': 'test1',
                           'email': 'test1@example.com', 'first_name': 'test1', 'last_name': 'test1'})
        self.assertEqual(response.status_code, 200)
        saved_user = User.objects.get(username='test')
        self.assertEqual(saved_user.email, 'test1@example.com')
        self.assertEqual(saved_user.first_name, 'test1')
        self.assertEqual(saved_user.last_name, 'test1')

    def test_user_profile_handler_invalid_email(self):
        c = Client()
        c.login(username='test2', password='test2')
        response = c.post('/user/',
                          {'password': '123', 'confirm_password': '123',
                           'email': 'test@example.com', 'first_name': 'test2', 'last_name': 'test2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already exists.')

    def test_user_profile_handler_invalid_password(self):
        c = Client()
        c.login(username='test2', password='test2')
        response = c.post('/user/',
                          {'password': '123', 'confirm_password': '321',
                           'email': 'test2@example.com', 'first_name': 'test2', 'last_name': 'test2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match.')

    def test_user_profile_handler_get(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.get('/user/')
        self.assertEqual(response.status_code, 200)


class TestUserLeaderboard(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.user.save()

    def test_user_leaderboard_handler(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.get('/leaderboard/')
        self.assertEqual(response.status_code, 200)
