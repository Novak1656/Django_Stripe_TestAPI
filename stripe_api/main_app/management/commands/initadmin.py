from django.contrib.auth.models import User
from django.core.management import BaseCommand
from decouple import config


class Command(BaseCommand):
    help = 'Команда для создания/инициализации суперпользователя'

    def handle(self, *args, **options):
        username = config('DJANGO_SUPERUSER_USERNAME')
        password = config('DJANGO_SUPERUSER_PASSWORD')
        email = config('DJANGO_SUPERUSER_EMAIL')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            print('Admin has been created.')
        else:
            print('Admin has been initialized.')
