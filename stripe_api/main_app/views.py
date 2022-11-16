import stripe

from django.db.models import Sum
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from .models import Item, Order


class ItemView(TemplateView):
    """
    Представление для отображения страницы предмета
    """
    template_name = 'main_app/item_page.html'
    extra_context = {'api_key': settings.STRIPE_PUBLIC_KEY}

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context.update(dict(item=get_object_or_404(Item, pk=kwargs.get('pk'))))
        return context


class BuyItemAPIView(APIView):
    """
    Представление для получения id сессии stripe при покупке предмета
    """
    http_method_names = ['get', ]

    def get(self, request, **kwargs):
        item = get_object_or_404(Item, pk=kwargs.get('pk'))
        stripe.api_key = settings.STRIPE_SECRET_KEY
        domain = f'http://{request.get_host()}'
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{domain}/success',
            cancel_url=f"{domain}{reverse('get_item', kwargs={'pk': kwargs.get('pk')})}",
        )
        return JsonResponse({'session_id': session.id})


def success(request):
    return render(request, 'payment_app/success.html')


# Views для бонусных заданий
class OrderView(TemplateView):
    """
    Представление для отображения страницы заказа
    """
    template_name = 'main_app/order_page.html'
    extra_context = {'api_key': settings.STRIPE_PUBLIC_KEY}

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        order = Order.objects.filter(pk=kwargs.get('order_pk'))\
            .select_related('discount', 'tax').prefetch_related('items').first()
        items = order.items.all()
        unit_amount = items.aggregate(unit_amount=Sum('price'))['unit_amount']
        context.update({'order': order, 'items': items, 'unit_amount': unit_amount})
        return context


class BuyOrderAPIView(APIView):
    """
    Представление для получения id сессии stripe при покупке заказа
    """
    http_method_names = ['get', ]

    def get(self, request, **kwargs):
        order = Order.objects.filter(pk=kwargs.get('order_pk'))\
            .select_related('discount', 'tax').prefetch_related('items').first()
        items = order.items.all()
        stripe.api_key = settings.STRIPE_SECRET_KEY
        discounts = []
        if order.discount:
            coupon = stripe.Coupon.create(percent_off=order.discount.discount_value)
            discounts = [{'coupon': f'{coupon.id}', }]
        domain = f'http://{request.get_host()}'
        tax = stripe.TaxRate.create(
            display_name=order.tax.tax_type,
            inclusive=order.tax.is_inclusive,
            percentage=order.tax.percentage,
        )
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                    },
                'quantity': 1,
                'tax_rates': [tax['id']]
                }for item in items],
            mode='payment',
            discounts=discounts,
            success_url=f'{domain}/success',
            cancel_url=f"{domain}{reverse('get_order', kwargs={'order_pk': kwargs.get('order_pk')})}",
        )
        return JsonResponse({'session_id': session.id})
