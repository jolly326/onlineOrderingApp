"""
支付模块 URL 路由
"""
from django.urls import path

from backend.apps.payments import views

urlpatterns = [
    path('pay', views.pay, name='payment-pay'),
    path('<str:pay_id>/status', views.pay_status, name='payment-status'),
]
