from django.test import Client, TestCase

from app.models import Domain, Client


class GetProbeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.domain = Domain(name='victim', url='victim.org')
        cls.domain.save()

        cls.domain.username_set.create(username='joseph')
        cls.domain.username_set.create(username='pablo')
        cls.domain.password_set.create(password='coucou')
        cls.domain.password_set.create(password='secret')

        cls.first_client = Client(ip='192.168.0.1', user_agent='tester 1')
        cls.first_client.save()

    def test_get_probes(self):
        response = self.client.get('/app/victim/probes/', HTTP_X_CLIENT_UUID=self.first_client.uuid)
        self.assertDictEqual(response.json(), {'probes': [
            {'username': 'joseph', 'password': 'coucou'},
            {'username': 'pablo', 'password': 'coucou'},
            {'username': 'joseph', 'password': 'secret'},
            {'username': 'pablo', 'password': 'secret'},
        ]})

    def test_get_exfiltrate(self):
        response = self.client.post('/app/victim/exfiltrate/', content_type='application/json',
                                    data={'username': 'pablo', 'password': 'coucou'})
        self.assertIs(response.status_code, 204)
        creds = Domain.objects.get(name='victim').credential_set.all()
        self.assertIs(len(creds), 1)
        self.assertEqual(creds[0].username, 'pablo')
        self.assertEqual(creds[0].password, 'coucou')
