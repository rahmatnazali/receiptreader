from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Populate database'

    def handle(self, *args, **options):
        print('populating database')
        call_command('populate_permissions')
