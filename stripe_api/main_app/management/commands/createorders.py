from random import randint

from django.core.management import BaseCommand
from main_app.models import Order, Discount, Tax, Item


class Command(BaseCommand):
    help = 'Команда для создания тестовых записей в модели Order'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Кол-во создаваемых записей')

    def handle(self, *args, **kwargs):
        order_count = kwargs.get('count')
        discounts = Discount.objects.all()
        discounts_count = discounts.count()
        tax = Tax.objects.all()
        tax_count = tax.count()
        try:
            order_list = [
                Order(
                    name=f'Order #{i}',
                    discount=discounts[randint(0, discounts_count-1)],
                    tax=tax[randint(0, tax_count-1)]
                ) for i in range(order_count)
            ]
            orders = Order.objects.bulk_create(order_list)
            items = Item.objects.all().values_list('id', flat=True)
            items_count = items.count()
            for order in orders:
                order.items.add(*items[0:randint(1, items_count-1)])
                order.save()
            print('Записи в таблице Order были успешно созданы')
        except Exception as error:
            print(f'При создании записей произошла ошибка: {error}')
