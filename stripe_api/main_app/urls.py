from django.urls import path
from .views import ItemView, BuyItemAPIView, success, OrderView, BuyOrderAPIView

urlpatterns = [
    path('buy/<int:pk>', BuyItemAPIView.as_view(), name='buy_item'),
    path('item/<int:pk>', ItemView.as_view(), name='get_item'),

    # Urls для бонусных заданий
    path('order/<int:order_pk>', OrderView.as_view(), name='get_order'),
    path('order/<int:order_pk>/buy/', BuyOrderAPIView.as_view(), name='buy_order'),

    path('success', success, name='success')
]
