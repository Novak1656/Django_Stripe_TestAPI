from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена'
    )

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['-price']

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    items = models.ManyToManyField(
        verbose_name='Предметы',
        to=Item,
        related_name='order'
    )
    discount = models.ForeignKey(
        verbose_name='Скидка в %',
        to='Discount',
        on_delete=models.PROTECT,
        related_name='order',
        null=True,
        blank=True
    )
    tax = models.ForeignKey(
        verbose_name='Налог',
        to='Tax',
        on_delete=models.PROTECT,
        related_name='order',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    discount_value = models.PositiveSmallIntegerField(
        verbose_name='Скидка в %',
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
        ordering = ['-discount_value']

    def __str__(self):
        return f'{self.name}: {self.discount_value}%'


class Tax(models.Model):
    TAX_TYPES = [('SALE', 'Sales Tax'), ('VAT', 'VAT Tax'), ('GST', 'GST Tax')]

    tax_type = models.CharField(
        verbose_name='Тип налога',
        choices=TAX_TYPES,
        max_length=255
    )
    percentage = models.DecimalField(
        verbose_name='Процент налога',
        max_digits=7,
        decimal_places=4
    )
    """
    Поле is_inclusive хранит значение о том включается ли налог в сумму покупки
    """
    is_inclusive = models.BooleanField(
        verbose_name='Включается',
        default=False
    )

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return f'Tax #{self.pk}: {self.percentage}'
