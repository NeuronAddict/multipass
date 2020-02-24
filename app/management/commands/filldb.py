from django.core.management.base import BaseCommand, CommandError

from app.models import Username, Password, Domain


class Command(BaseCommand):
    help = 'Fill the database with content of files in dict folder'

    def handle(self, *args, **options):
        try:
            fake_probes()
            self.stdout.write(self.style.SUCCESS('Successfully fill database'))
        except Exception as e:
            raise CommandError('Error : {}'.format(e))


def fake_probes():

    Domain(name='victim', chunk_size=256).save()

    with open('dict/top-usernames-shortlist.txt') as file:
        for line in file:
            Username(username=line.rstrip()).save()
    with open('dict/10-million-password-list-top-100.txt') as file:
        for line in file:
            Password(password=line.rstrip()).save()
