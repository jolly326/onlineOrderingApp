from django.contrib import admin

from backend.apps.cart.models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """购物车管理后台"""
    list_display = ['cart_id', 'user']
    readonly_fields = ['cart_id']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """购物车项管理后台"""
    list_display = ['cart', 'dish', 'quantity']
