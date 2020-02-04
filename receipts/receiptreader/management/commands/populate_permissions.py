from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import  IntegrityError

class Command(BaseCommand):
    help = 'Create Permissons'

    def handle(self, *args, **options):
        print('create permissons')
