"""
订单模块工具函数
"""
import datetime

from django.db.models import Sum
from django.utils import timezone

from backend.apps.orders.models import Order, DailyStats


def _day_range(date):
    """获取指定日期在本地时区的起止时间（aware datetime）"""
    start = timezone.make_aware(datetime.datetime.combine(date, datetime.time.min))
    end = timezone.make_aware(datetime.datetime.combine(date, datetime.time.max))
    return start, end


def refresh_daily_stats(target_date=None):
    """
    重新计算并持久化指定日期的经营统计数据

    使用 __range 替代 __date 避免 MySQL 时区转换问题。
    订单创建或状态变更后调用，确保 DailyStats 与 Order 表一致。
    """
    date = target_date or timezone.now().date()
    day_start, day_end = _day_range(date)
    orders = Order.objects.filter(create_time__range=(day_start, day_end))

    stats, _ = DailyStats.objects.get_or_create(date=date)
    stats.total_orders = orders.count()
    stats.total_revenue = orders.filter(
        order_status__in=['preparing', 'waiting_pickup', 'completed']
    ).aggregate(total=Sum('total_money'))['total'] or 0
    stats.preparing_count = orders.filter(order_status='preparing').count()
    stats.waiting_pickup_count = orders.filter(order_status='waiting_pickup').count()
    stats.completed_count = orders.filter(order_status='completed').count()
    stats.cancelled_count = orders.filter(order_status='cancelled').count()
    stats.save()
    return stats
