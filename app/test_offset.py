from datetime import datetime

from django.test import TestCase

from app.models import Client, Domain, Offset
from app.offset import OffsetUtils


class OffsetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.domain = Domain(name='victim')
        cls.domain.save()
        cls.first_client = Client(ip='129.168.0.1', user_agent='tester', domain=cls.domain)
        cls.first_client.save()

        cls.bogged_client = Client(ip='129.168.0.2', user_agent='bogged tester', domain=cls.domain)
        cls.bogged_client.save()

    def test_bogged_offset(self):
        first_offset = OffsetUtils.next_username_offset(self.first_client, datetime(2020, 2, 20, 1, 15, 1))
        self.assertEqual(first_offset.value, 0)

        first_offset.ack = True
        first_offset.save()

        second_offset = Offset(value=256, type=0, client=self.bogged_client, last_send=datetime(2020, 2, 20, 0, 0, 0))
        second_offset.save()

        third_offset = Offset(value=256*2, type=0, client=self.first_client, ack=True)
        third_offset.save()

        last = OffsetUtils.next_username_offset(self.first_client, datetime(2020, 2, 20, 1, 15, 1))
        self.assertEqual(last.value, 256)


