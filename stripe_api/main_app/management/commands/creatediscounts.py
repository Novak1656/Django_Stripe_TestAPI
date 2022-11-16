from random import randint

from django.core.management import BaseCommand
from main_app.models import Discount


class Command(BaseCommand):
    help = 'Команда для создания тестовых записей в модели Discount'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Кол-во создаваемых записей')

    def handle(self, *args, **kwargs):
        discount_count = kwargs.get('count')
        try:
            discount_list = [Discount(name=f'Sale #{i}', discount_value=randint(1, 100)) for i in range(discount_count)]
            Discount.objects.bulk_create(discount_list)
            print('Записи в таблице Discount были успешно созданы')
        except Exception as error:
            print(f'При создании записей произошла ошибка: {error}')
