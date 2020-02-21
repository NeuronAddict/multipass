from django.test import TestCase
from django.utils import timezone

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
        """
        Test with:
          - first offset ack
          - second on timeout
          - third nack, notimeout
          - 4th must be second
        :return:
        """

        first_date = timezone.datetime(2020, 2, 20, 0, 0, 0)
        second_date = timezone.datetime(2020, 2, 20, 2, 0, 0)

        first_offset = OffsetUtils.next_username_offset(self.first_client, first_date)
        self.assertEqual(first_offset.value, 0)
        self.assertEqual(first_offset.client, self.first_client)

        first_offset.ack = True
        first_offset.save()

        second_offset = OffsetUtils.next_username_offset(self.bogged_client, first_date)
        second_offset.save()
        self.assertEqual(second_offset.value, 256)
        self.assertEqual(second_offset.client, self.bogged_client)

        third_offset = OffsetUtils.next_username_offset(self.first_client, first_date)
        third_offset.save()
        self.assertEqual(third_offset.value, 512)
        self.assertEqual(third_offset.client, self.first_client)

        last = OffsetUtils.next_username_offset(self.first_client, second_date)
        self.assertEqual(last.value, 256)
        self.assertEqual(last.client, self.first_client)
