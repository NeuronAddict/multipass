import json

from django.test import TestCase
from django.utils import timezone

from .models import Domain, Username


class QuestionModelTests(TestCase):

    def test_usernames_to_json(self):
        usernames = [
            'charlie', 'joseph', 'igor'
        ]

        passwords = [
            'secret', 'checkpoint', 'bravo'
        ]

        domain = Domain(name='victim', url='victim.org')
        domain.save()

        for username in usernames:
            domain.username_set.create(username=username)

        for password in passwords:
            domain.password_set.create(password=password)

        usernames_from_db = domain.username_set.all().values('username')
        usernames_dict = {'usernames': list(usernames_from_db)}
        self.assertListEqual(usernames, list(map(lambda x: x['username'], usernames_from_db)))
        self.assertDictEqual(json.loads(json.dumps(usernames_dict)), usernames_dict)

        passwords_from_db = domain.password_set.all().values('password')
        passwords_dict = {'passwords': list(passwords_from_db)}
        self.assertListEqual(passwords, list(map(lambda x: x['password'], passwords_from_db)))
        self.assertDictEqual(json.loads(json.dumps(passwords_dict)), passwords_dict)
