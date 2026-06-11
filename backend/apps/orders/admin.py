from django.contrib import admin

from backend.apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """订单项内联展示"""
    model = OrderItem
    extra = 0
    readonly_fields = ['dish_name', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """订单管理后台"""
    list_display = ['order_id', 'user', 'total_money', 'order_status', 'pick_up_code', 'create_time']
    list_filter = ['order_status']
    search_fields = ['order_id', 'user__username']
    readonly_fields = ['order_id', 'total_money', 'pay_deadline', 'create_time', 'update_time']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """订单项管理后台"""
    list_display = ['order', 'dish_name', 'price', 'quantity']
    readonly_fields = ['order_item_id']
