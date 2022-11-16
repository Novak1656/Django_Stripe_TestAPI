from django.contrib import admin
from .models import Item, Discount, Order, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = ['id', 'name']
    list_filter = ['name', 'price']
    search_fields = ['name']
    save_on_top = True
    save_as = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'discount', 'tax', 'created_at']
    list_display_links = ['id', 'name']
    list_filter = ['created_at']
    search_fields = ['name']
    save_on_top = True
    save_as = True


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'discount_value']
    list_display_links = ['id', 'name']
    list_filter = ['discount_value']
    search_fields = ['name']
    save_on_top = True
    save_as = True


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['id', 'tax_type', 'percentage', 'is_inclusive']
    list_display_links = ['id']
    list_filter = ['tax_type']
    save_on_top = True
    save_as = True
