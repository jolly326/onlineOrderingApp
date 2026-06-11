from django.apps import AppConfig


class CartConfig(AppConfig):
    """购物车模块应用配置"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.apps.cart'
    verbose_name = '购物车管理'

    def ready(self):
        """导入信号以注册回调"""
        import backend.apps.cart.signals  # noqa
