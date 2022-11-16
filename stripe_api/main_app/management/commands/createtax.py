from random import randint, uniform

from django.core.management import BaseCommand
from main_app.models import Tax


class Command(BaseCommand):
    help = 'Команда для создания тестовых записей в модели Tax'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Кол-во создаваемых записей')

    def handle(self, *args, **kwargs):
        tax_count = kwargs.get('count')
        tax_types = Tax.TAX_TYPES
        try:
            tax_list = [
                Tax(
                   tax_type=tax_types[randint(0, 2)][0],
                   percentage=uniform(1.0, 99.99),
                   is_inclusive=randint(0, 1)
                ) for _ in range(tax_count)
            ]
            Tax.objects.bulk_create(tax_list)
            print('Записи в таблице Tax были успешно созданы')
        except Exception as error:
            print(f'При создании записей произошла ошибка: {error}')
