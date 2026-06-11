import uuid

from django.db import models

from backend.apps.orders.models import Order


def uuid_hex():
    """生成32位无连字符UUID"""
    return uuid.uuid4().hex


class Payment(models.Model):
    """
    支付模型

    记录订单的支付信息，支持微信和支付宝两种模拟支付方式。
    与订单为一对一关系。
    """
    PAY_TYPE_CHOICES = [
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
    ]
    PAY_STATUS_CHOICES = [
        ('pending', '待支付'),
        ('success', '支付成功'),
        ('failed', '支付失败'),
    ]

    pay_id = models.CharField(
        primary_key=True,
        max_length=32,
        default=uuid_hex,
        editable=False,
        verbose_name='支付ID'
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='关联订单'
    )
    pay_type = models.CharField(max_length=20, choices=PAY_TYPE_CHOICES, verbose_name='支付方式')
    pay_status = models.CharField(
        max_length=20,
        choices=PAY_STATUS_CHOICES,
        default='pending',
        verbose_name='支付状态'
    )
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    class Meta:
        db_table = 'payment'
        verbose_name = '支付'
        verbose_name_plural = '支付'

    def __str__(self):
        return f'支付{self.pay_id}({self.get_pay_status_display()})'
