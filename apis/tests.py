from datetime import date, timedelta
from django.test import TestCase, Client
from users.models import Member
from apis.models import ApiKey


class TestSplitPost(TestCase):
    def setUp(self):
        Member.objects.create_user(email='foo@foobar.com', password='12345')
        a = ApiKey.objects.create(email='goo@goobar.com')
        a.start_date = date.today()
        a.end_date = a.start_date + timedelta(days=1)
        a.save()

        self.key_obj = a

        self.client = Client()
        self.header = {'Authorization': f'Bearer {a.key}'}


    def post_it(self, data):
        return self.client.post('/split/', headers=self.header, data=data)

    def test_split(self):
        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})

    def test_n(self):
        self.key_obj.n_requests = self.key_obj.n_allowed_requests
        self.key_obj.save()

        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 401)

    def test_date(self):
        ko = self.key_obj
        ko.start_date = self.key_obj.end_date
        ko.n_requests = 0
        ko.save()

        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 401)

        ko.start_date = None
        ko.end_date = None
        ko.save()
        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 200)

        ko.start_date = date.today()
        ko.end_date = date.today() + timedelta(days=1)
        ko.save()

        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 200)

    def test_nolimit(self):
        ko = self.key_obj
        ko.n_allowed_requests = None
        ko.n_requests = 10
        ko.start_date = None
        ko.end_date = None
        ko.save()

        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 200)
