import uuid
import random
from datetime import timedelta

from django.db import models
from django.utils import timezone

from backend.apps.users.models import User
from backend.apps.dishes.models import Dish


def uuid_hex():
    """生成32位无连字符UUID"""
    return uuid.uuid4().hex


def generate_order_id() -> str:
    """
    生成订单号：年月日 + 8位随机数

    Returns:
        str: 20位订单号
    """
    now = timezone.now()
    date_part = now.strftime('%y%m%d')
    random_part = str(random.randint(10000000, 99999999))
    return date_part + random_part


def default_pay_deadline() -> timezone.datetime:
    """获取默认支付截止时间（当前时间+15分钟）"""
    return timezone.now() + timedelta(minutes=15)


class Order(models.Model):
    """
    订单模型

    记录订单基本信息、状态流转、支付截止时间等。
    订单状态: pending_payment(待支付) -> preparing(备餐中)
              -> waiting_pickup(待取餐) -> completed(已完成)
              -> cancelled(已取消)
    """
    STATUS_CHOICES = [
        ('pending_payment', '待支付'),
        ('preparing', '备餐中'),
        ('waiting_pickup', '待取餐'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    order_id = models.CharField(
        primary_key=True,
        max_length=20,
        default=generate_order_id,
        editable=False,
        verbose_name='订单号'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='关联用户'
    )
    total_money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending_payment',
        verbose_name='订单状态'
    )
    pick_up_code = models.CharField(max_length=6, null=True, blank=True, verbose_name='取餐码')
    pay_deadline = models.DateTimeField(default=default_pay_deadline, verbose_name='支付截止时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return f'订单{self.order_id}({self.get_order_status_display()})'


class OrderItem(models.Model):
    """
    订单项模型

    记录订单中每个菜品的快照信息（名称、价格、数量）。
    采用快照设计，即使菜品信息后续修改，订单记录不受影响。
    """
    order_item_id = models.CharField(
        primary_key=True,
        max_length=32,
        default=uuid_hex,
        editable=False,
        verbose_name='订单项ID'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='关联订单'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name='关联菜品'
    )
    dish_name = models.CharField(max_length=50, verbose_name='菜品名称(快照)')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价(快照)')
    quantity = models.IntegerField(default=1, verbose_name='数量')

    class Meta:
        db_table = 'order_item'
        verbose_name = '订单项'
        verbose_name_plural = '订单项'

    def __str__(self):
        return f'{self.dish_name} x {self.quantity}'


class DailyStats(models.Model):
    """
    每日经营统计（持久化存储，避免每次实时计算）

    每当订单状态变更时自动更新。
    """
    date = models.DateField(unique=True, verbose_name='日期')
    total_orders = models.IntegerField(default=0, verbose_name='总订单数')
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='总收入')
    preparing_count = models.IntegerField(default=0, verbose_name='备餐中')
    waiting_pickup_count = models.IntegerField(default=0, verbose_name='待取餐')
    completed_count = models.IntegerField(default=0, verbose_name='已完成')
    cancelled_count = models.IntegerField(default=0, verbose_name='已取消')

    class Meta:
        db_table = 'daily_stats'
        verbose_name = '每日统计'
        verbose_name_plural = '每日统计'

    def __str__(self):
        return f'{self.date} 统计'
