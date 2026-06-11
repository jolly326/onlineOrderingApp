from django.apps import AppConfig


class DishesConfig(AppConfig):
    """菜品模块应用配置"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.apps.dishes'
    verbose_name = '菜品管理'
