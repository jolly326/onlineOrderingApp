"""
支付模块视图

提供模拟支付和支付状态查询接口。
"""
import random
from datetime import timedelta

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from backend.apps.orders.models import Order
from backend.apps.payments.models import Payment
from backend.utils import api_response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay(request):
    """
    发起支付

    返回90%概率的模拟支付结果。
    支付成功时：更新订单为备餐中，记录支付时间。
    支付失败时：订单状态不变，可重试。

    Args:
        request: POST请求，包含order_id和pay_type

    Returns:
        Response: 支付结果
    """
    order_id = request.data.get('order_id')
    pay_type = request.data.get('pay_type')

    if pay_type not in ['wechat', 'alipay']:
        return api_response(code=400, message='不支持的支付方式', data={})

    try:
        order = Order.objects.get(pk=order_id, user=request.user)
    except Order.DoesNotExist:
        return api_response(code=404, message='订单不存在', data={})

    if order.order_status != 'pending_payment':
        return api_response(code=400, message='订单状态不允许支付', data={})

    if timezone.now() > order.pay_deadline:
        order.order_status = 'cancelled'
        order.save()
        return api_response(code=400, message='支付超时，订单已取消', data={})

    try:
        payment = Payment.objects.get(order=order)
    except Payment.DoesNotExist:
        return api_response(code=400, message='支付记录不存在', data={})

    # 更新支付方式
    payment.pay_type = pay_type

    # 模拟支付：90%概率成功
    success = random.random() < 0.9

    if success:
        payment.pay_status = 'success'
        payment.pay_time = timezone.now()
        order.order_status = 'preparing'
        order.save()
        payment.save()
        return api_response(code=200, message='支付成功', data={
            'pay_id': payment.pay_id,
            'pay_status': 'success',
            'order_status': 'preparing',
        })
    else:
        payment.pay_status = 'failed'
        payment.save()
        return api_response(code=200, message='支付失败，请重试', data={
            'pay_id': payment.pay_id,
            'pay_status': 'failed',
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pay_status(request, pay_id):
    """
    查询支付状态

    Args:
        request: GET请求
        pay_id: 支付ID

    Returns:
        Response: 支付状态信息
    """
    try:
        payment = Payment.objects.get(pk=pay_id, order__user=request.user)
    except Payment.DoesNotExist:
        return api_response(code=404, message='支付记录不存在', data={})

    return api_response(data={
        'pay_id': payment.pay_id,
        'order_id': payment.order.order_id,
        'pay_type': payment.pay_type,
        'pay_status': payment.pay_status,
        'pay_time': payment.pay_time,
        'order_status': payment.order.order_status,
    })
