from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    """支付模块应用配置"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.apps.payments'
    verbose_name = '支付管理'
