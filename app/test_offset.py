from datetime import datetime

from django.test import TestCase

from app.models import Client, Domain, Offset
from app.offset import OffsetUtils


class OffsetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        domain = Domain(name='victim')
        domain.save()
        client = Client(ip='129.168.0.1', user_agent='test', domain=domain)
        client.save()

    def test_offset(self):
        last = OffsetUtils.next_username_offset(datetime(2020, 2, 20))
        self.assertEqual(last, 0)
