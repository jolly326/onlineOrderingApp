"""
订单模块 URL 路由
"""
from django.urls import path

from backend.apps.orders import views

urlpatterns = [
    path('', views.order_list, name='order-list'),
    path('create', views.create_order, name='order-create'),
    path('count', views.order_count, name='order-count'),
    path('merchant', views.merchant_order_list, name='order-merchant-list'),
    path('merchant/stats', views.merchant_stats, name='order-merchant-stats'),
    path('merchant/confirm-pickup/<str:order_id>', views.merchant_confirm_pickup, name='order-merchant-confirm-pickup'),
    path('<str:order_id>', views.order_detail, name='order-detail'),
    path('<str:order_id>/status', views.update_order_status, name='order-status'),
    path('<str:order_id>/confirm-pickup', views.confirm_pickup, name='order-confirm-pickup'),
]
