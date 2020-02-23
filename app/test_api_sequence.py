from unittest.mock import patch

from django.test import Client, TestCase
from django.utils import timezone

from app.models import Domain, Client

CHUNK_SIZE = 4
PROBES_COUNT = 5


class SequenceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.domain = Domain(name='victim', url='victim.org', chunk_size=CHUNK_SIZE)
        cls.domain.save()

        for i in range(0, PROBES_COUNT):
            cls.domain.username_set.create(username='username{}'.format(i))

        for i in range(0, PROBES_COUNT):
            cls.domain.password_set.create(password='password{}'.format(i))

        cls.first_client = Client(ip='192.168.0.1', user_agent='tester 1')
        cls.first_client.save()

        cls.second_client = Client(ip='192.168.0.1', user_agent='tester 1')
        cls.second_client.save()

        cls.date1 = timezone.datetime(2020, 2, 20, 0, 0, 0)
        cls.date2 = timezone.datetime(2020, 2, 20, 2, 0, 0)
        cls.date3 = timezone.datetime(2020, 2, 20, 3, 0, 0)

    def test_sequence(self):

        with patch.object(timezone, 'now', return_value=self.date1):
            self.request_probes(self.first_client, 0)

            self.ack(self.first_client)

            self.request_probes(self.second_client, 1)

            self.request_probes(self.second_client, 1)

        with patch.object(timezone, 'now', return_value=self.date2):
            self.request_probes(self.first_client, 1)

            self.ack(self.first_client)

            # ack must not have effects
            self.ack(self.second_client)

        with patch.object(timezone, 'now', return_value=self.date3):
            self.request_probes(self.first_client, 2)

            self.request_probes(self.second_client, 3)

            self.ack(self.first_client)
            self.ack(self.second_client)

            for i in range(4, 9):
                self.request_probes(self.first_client, i)
                self.ack(self.first_client)

            response = self.client.get('/app/victim/probes/', HTTP_X_CLIENT_UUID=self.first_client.uuid)
            self.assertDictEqual(response.json(), {'probes': []})

    def request_probes(self, client: Client, expected_chunk_number):
        response = self.client.get('/app/victim/probes/', HTTP_X_CLIENT_UUID=client.uuid)
        self.assert_response_range(response, expected_chunk_number * CHUNK_SIZE)

    def ack(self, client):
        response = self.client.get('/app/victim/ack/', HTTP_X_CLIENT_UUID=client.uuid)
        self.assertEquals(response.status_code, 204)

    def assert_response_range(self, response, offset):
        probes = []
        for i in range(0, PROBES_COUNT - 1):
            if offset + i >= PROBES_COUNT * PROBES_COUNT:
                break
            password = 'password{}'.format(int((offset + i) / PROBES_COUNT))
            username = 'username{}'.format((offset + i) % PROBES_COUNT)
            probes.append({'username': username, 'password': password})
        self.assertDictEqual(response.json(), {'probes': probes})
