from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """订单模块应用配置"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.apps.orders'
    verbose_name = '订单管理'
