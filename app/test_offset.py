from django.test import TestCase
from django.utils import timezone

from app.models import Client, Domain
from app.offset import OffsetUtils


class OffsetTests(TestCase):

    # noinspection PyAttributeOutsideInit
    def setUp(self):
        self.domain = Domain(name='victim')
        self.domain.save()
        self.first_client = Client(ip='129.168.0.1', user_agent='tester', domain=self.domain)
        self.first_client.save()

        self.second_client = Client(ip='129.168.0.1', user_agent='tester', domain=self.domain)
        self.second_client.save()

        self.bogged_client = Client(ip='129.168.0.2', user_agent='bogged tester', domain=self.domain)
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

        offset1 = OffsetUtils.next_username_offset(self.first_client, date1)
        self.assertEqual(offset1.value, 0)
        self.assertEqual(offset1.client, self.first_client)

        OffsetUtils.ack(offset1)

        offset2 = OffsetUtils.next_username_offset(self.bogged_client, date1)
        offset2.save()
        self.assertEqual(offset2.value, 256)
        self.assertEqual(offset2.client, self.bogged_client)

        offset3 = OffsetUtils.next_username_offset(self.first_client, date1)
        offset3.save()
        self.assertEqual(offset3.value, 256*2)
        self.assertEqual(offset3.client, self.first_client)

        offset2_2 = OffsetUtils.next_username_offset(self.second_client, date2)
        self.assertEqual(offset2_2.value, 256)
        self.assertEqual(offset2_2.client, self.second_client)

        OffsetUtils.ack(offset3)

        OffsetUtils.ack(offset2_2)

        offset4 = OffsetUtils.next_username_offset(self.first_client, date2)
        self.assertEqual(offset4.value, 256*3)
        self.assertEqual(offset4.client, self.first_client)

        offset5 = OffsetUtils.next_username_offset(self.second_client, date2)
        self.assertEqual(offset5.value, 256 * 4)
        self.assertEqual(offset5.client, self.second_client)

        offset6 = OffsetUtils.next_username_offset(self.bogged_client, date2)
        self.assertEqual(offset6.value, 256 * 5)
        self.assertEqual(offset6.client, self.bogged_client)

        OffsetUtils.ack(offset4)

        OffsetUtils.ack(offset5)

        offset6_2 = OffsetUtils.next_username_offset(self.second_client, date3)
        self.assertEqual(offset6_2.value, 256 * 5)
        self.assertEqual(offset6_2.client, self.second_client)
