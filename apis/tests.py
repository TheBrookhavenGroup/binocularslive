from django.test import TestCase, Client
from users.models import Member
from rest_framework.authtoken.models import Token
from apis.models import ApiKey


class TestHelloView(TestCase):
    def setUp(self):
        self.user = Member.objects.create_user(email='foo@foobar.com',
                                               password='12345')
        self.token = Token.objects.create(user=self.user)

    def test_hello(self):
        key = self.token.key
        response = self.client.get('/hello/',
                                   HTTP_AUTHORIZATION=f'Token {key}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})


class TestGoodbyeViewPost(TestCase):
    def setUp(self):
        user = Member.objects.create_user(email='foo@foobar.com',
                                          password='12345')
        a = ApiKey.objects.create(email='goo@goobar.com')
        a.save()
        self.key = a.key

    def test_hello(self):
        key = self.key
        c = Client()
        data = {'text': 'Bye, World!'}
        header = {'Authorization': f'Bearer {key}'}
        response = c.post('/bye/', headers=header, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Bye, World!'})