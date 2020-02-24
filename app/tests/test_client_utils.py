from django.http import HttpRequest
from django.test import TestCase

from app.models import Domain, Client
from client_utils import get_client


class Test(TestCase):

    # noinspection PyAttributeOutsideInit
    def setUp(self):
        self.domain = Domain(name='victim', chunk_size=256)
        self.domain.save()

        self.first_client = Client(ip='129.168.0.1', user_agent='tester')
        self.first_client.save()

        self.second_client = Client(ip='129.168.0.1', user_agent='tester')
        self.second_client.save()

        self.bogged_client = Client(ip='129.168.0.2', user_agent='bogged tester')
        self.bogged_client.save()

    def test_create_client_without_uuid_client(self):
        client = Client(ip='129.168.0.1', user_agent='tester', uuid=None)
        client.save()

    def test_create_client_without_useragent_client(self):
        client = Client(ip='129.168.0.1', user_agent=None)
        client.save()

    def test_create_client(self):
        uuid = 'da8e4c40-8c10-4f97-b109-d17ec8ad9960'
        user_agent = 'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile ' \
                     'Safari/533.1 '
        ip = '192.168.2.3'
        request = HttpRequest()
        # noinspection PyPropertyAccess
        request.headers = {
            'User-Agent': user_agent,
            'X-CLIENT-UUID': uuid
        }
        request.META = {
            'REMOTE_ADDR': ip
        }
        client = get_client(request)
        self.assertEquals(client.ip, ip)
        self.assertEquals(client.user_agent, user_agent)
        self.assertEquals(client.uuid, uuid)

    def test_create_client_without_uuid(self):
        request = HttpRequest()
        # noinspection PyPropertyAccess
        request.headers = {
            'User-Agent': 'nouuid'
        }
        request.META = {
            'REMOTE_ADDR': '192.168.2.3'
        }
        client = get_client(request)
        self.assertEquals(client.ip, '192.168.2.3')
        self.assertEquals(client.user_agent, 'nouuid')
        self.assertIsNone(client.uuid)

    def test_create_client_without_user_agent(self):
        request = HttpRequest()
        # noinspection PyPropertyAccess
        request.headers = {
        }
        request.META = {
            'REMOTE_ADDR': '192.168.2.3'
        }
        client = get_client(request)
        self.assertEquals(client.ip, '192.168.2.3')
        self.assertIsNone(client.user_agent)

    def test_get_existing_client_without_uuid(self):
        ip = '192.168.2.3'
        client = Client(ip=ip, user_agent='tester_existing', uuid=None)
        client.save()

        other = Client(ip=ip, user_agent='tester_existing 2', uuid=None)
        other.save()

        request = HttpRequest()
        # noinspection PyPropertyAccess
        request.headers = {
            'User-Agent': 'tester_existing'
        }
        request.META = {
            'REMOTE_ADDR': ip
        }
        self.assertEquals(client, get_client(request))
