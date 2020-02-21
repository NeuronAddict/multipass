from django.test import Client, TestCase

from app.models import Domain, Client


class SequenceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.domain = Domain(name='victim', url='victim.org', chunk_size=2)
        cls.domain.save()

        for i in range(1, 6):
            cls.domain.username_set.create(username='username{}'.format(i))

        for i in range(1, 6):
            cls.domain.password_set.create(password='password{}'.format(i))

        cls.first_client = Client(ip='192.168.0.1', user_agent='tester 1')
        cls.first_client.save()

        cls.second_client = Client(ip='192.168.0.1', user_agent='tester 1')
        cls.second_client.save()

    def test_sequence(self):
        response = self.client.get('/app/victim/usernames/', HTTP_X_CLIENT_UUID=self.first_client.uuid)
        self.assert_response_range(response, 'username', 1, 2)

        response = self.client.get('/app/victim/passwords/', HTTP_X_CLIENT_UUID=self.second_client.uuid)
        self.assert_response_range(response, 'password', 1, 2)

        response = self.client.get('/app/victim/usernames/', HTTP_X_CLIENT_UUID=self.second_client.uuid)
        self.assert_response_range(response, 'username', 3, 4)

        response = self.client.get('/app/victim/passwords/', HTTP_X_CLIENT_UUID=self.first_client.uuid)
        self.assert_response_range(response, 'password', 3, 4)

        response = self.client.get('/app/victim/passwords/', HTTP_X_CLIENT_UUID=self.first_client.uuid)
        self.assert_response_range(response, 'password', 5, 5)

        response = self.client.get('/app/victim/usernames/', HTTP_X_CLIENT_UUID=self.second_client.uuid)
        self.assert_response_range(response, 'username', 5, 5)

    def assert_response_range(self, response, keyword, begin, end):
        lst = []
        for i in range(begin, end + 1):
            lst.append({keyword: '{}{}'.format(keyword, i)})
        self.assertDictEqual(response.json(), {'{}s'.format(keyword): lst})
