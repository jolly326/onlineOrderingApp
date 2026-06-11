from django.contrib import admin

from backend.apps.dishes.models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """菜品管理后台"""
    list_display = ['dish_name', 'category', 'price', 'month_sales', 'status']
    list_filter = ['category', 'status']
    search_fields = ['dish_name']
    readonly_fields = ['dish_id']
