from django.contrib import admin

from backend.apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """支付管理后台"""
    list_display = ['pay_id', 'order', 'pay_type', 'pay_status', 'pay_time']
    list_filter = ['pay_type', 'pay_status']
    readonly_fields = ['pay_id', 'pay_time']
