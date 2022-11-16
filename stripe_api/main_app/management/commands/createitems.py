from random import randint

from django.core.management import BaseCommand
from main_app.models import Item


class Command(BaseCommand):
    help = 'Команда для создания тестовых записей в модели Item'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Кол-во создаваемых записей')

    def handle(self, *args, **kwargs):
        item_count = kwargs.get('count')
        try:
            items = [
                Item(name=f'Item #{i}', description='Some test description ' * i, price=randint(1, 100_000))
                for i in range(item_count)
            ]
            Item.objects.bulk_create(items)
            print('Записи в таблице Item были успешно созданы')
        except Exception as error:
            print(f'При создании записей произошла ошибка: {error}')
