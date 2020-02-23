from django.test import TestCase

from app.offset import *

CHUNK_SIZE = 256


class OffsetTests(TestCase):

    # noinspection PyAttributeOutsideInit
    def setUp(self):
        self.domain = Domain(name='victim', chunk_size=CHUNK_SIZE)
        self.domain.save()
        self.first_client = Client(ip='129.168.0.1', user_agent='tester')
        self.first_client.save()

        self.second_client = Client(ip='129.168.0.1', user_agent='tester')
        self.second_client.save()

        self.bogged_client = Client(ip='129.168.0.2', user_agent='bogged tester')
        self.bogged_client.save()

    def test_bogged_offset(self):
        """
        Test with:
          - first offset ack
          - second on timeout
          - third nack, notimeout
          - 4th must be second
        :return:
        """

        date1 = timezone.datetime(2020, 2, 20, 0, 0, 0)
        date2 = timezone.datetime(2020, 2, 20, 2, 0, 0)
        date3 = timezone.datetime(2020, 2, 20, 3, 0, 0)

        self.request_offset(self.first_client, date1, 0)

        ack(self.first_client)

        self.request_offset(self.bogged_client, date1, 1)

        self.request_offset(self.first_client, date1, 2)

        ack(self.first_client)

        self.request_offset(self.second_client, date2, 1)

        ack(self.second_client)

        self.request_offset(self.first_client, date2, 3)

        self.request_offset(self.second_client, date2, 4)

        self.request_offset(self.second_client, date2, 4)

        ack(self.first_client)

        ack(self.second_client)

        self.request_offset(self.second_client, date3, 5)

    def request_offset(self, client: Client, date: timezone.datetime, assert_chunk_number):
        offset = next_username_offset(self.domain, client, date)
        self.assertEqual(offset.value, CHUNK_SIZE * assert_chunk_number)
        self.assertEqual(client.current_offset, offset)
