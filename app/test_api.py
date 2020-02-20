import unittest

from django.test import Client

from app.models import Domain


class GetProbeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        domain = Domain(name='victim', url='victim.org')
        domain.save()

        domain.username_set.create(username='joseph')
        domain.username_set.create(username='pablo')
        domain.password_set.create(password='coucou')
        domain.password_set.create(password='secret')

    def setUp(self) -> None:
        self.client = Client()

    def test_get_usernames(self):
        response = self.client.get('/app/victim/usernames/')
        self.assertDictEqual(response.json(), {'usernames': [
            {'username': 'joseph'},
            {'username': 'pablo'},
        ]})

    def test_get_passwords(self):
        response = self.client.get('/app/victim/passwords/')
        self.assertDictEqual(response.json(), {'passwords': [
            {'password': 'coucou'},
            {'password': 'secret'},
        ]})
