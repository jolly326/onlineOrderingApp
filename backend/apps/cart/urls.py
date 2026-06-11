"""
购物车模块 URL 路由
"""
from django.urls import path

from backend.apps.cart import views

urlpatterns = [
    path('', views.cart_detail, name='cart-detail'),
    path('items', views.add_item, name='cart-add-item'),
    path('items/<str:item_id>', views.update_item, name='cart-update-item'),
    path('items/<str:item_id>/delete', views.delete_item, name='cart-delete-item'),
    path('clear', views.clear_cart, name='cart-clear'),
]
