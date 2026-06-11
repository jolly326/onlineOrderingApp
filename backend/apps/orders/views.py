"""
订单模块视图

提供订单提交、列表、详情、状态更新和商家统计接口。
"""
import random

from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from backend.apps.cart.models import CartItem
from backend.apps.orders.models import Order, OrderItem, DailyStats
from backend.apps.orders.serializers import OrderSerializer, OrderStatusSerializer
from backend.apps.orders.utils import refresh_daily_stats
from backend.apps.payments.models import Payment
from backend.utils import api_response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """提交订单：购物车 → 订单 + 支付记录"""
    user = request.user
    cart = user.cart
    items = CartItem.objects.filter(cart=cart, dish__status=True)
    if not items.exists():
        return api_response(code=400, message='购物车为空或菜品已下架', data={})

    total_money = sum(float(item.dish.price) * item.quantity for item in items)
    order = Order.objects.create(user=user, total_money=total_money)
    OrderItem.objects.bulk_create([
        OrderItem(order=order, dish=item.dish, dish_name=item.dish.dish_name,
                  price=item.dish.price, quantity=item.quantity)
        for item in items
    ])
    payment = Payment.objects.create(order=order, pay_type='wechat')
    items.delete()
    refresh_daily_stats()
    return api_response(code=200, message='下单成功', data={
        'order': OrderSerializer(order).data, 'pay_id': payment.pay_id,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    """用户获取自己的订单列表"""
    status = request.query_params.get('status')
    orders = Order.objects.filter(user=request.user).order_by('-create_time')
    if status:
        orders = orders.filter(order_status=status)
    return api_response(data=OrderSerializer(orders, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    """获取订单详情"""
    try:
        order = Order.objects.get(pk=order_id, user=request.user)
    except Order.DoesNotExist:
        return api_response(code=404, message='订单不存在', data={})
    return api_response(data=OrderSerializer(order).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_count(request):
    """获取当前用户的各状态订单数量统计"""
    user_orders = Order.objects.filter(user=request.user)
    counts = user_orders.values('order_status').annotate(count=Count('order_status'))
    result = {item['order_status']: item['count'] for item in counts}
    return api_response(data=result)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    """商家更新订单状态（备餐中→待取餐）"""
    if request.user.role != 'merchant':
        return api_response(code=403, message='仅商家可操作', data={})
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return api_response(code=404, message='订单不存在', data={})

    serializer = OrderStatusSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    new_status = serializer.validated_data['order_status']

    valid_transitions = {'preparing': ['waiting_pickup']}
    if order.order_status in valid_transitions:
        if new_status not in valid_transitions[order.order_status]:
            return api_response(code=400, message=f'当前状态不能直接变更为{new_status}', data={})
    elif order.order_status == 'pending_payment':
        return api_response(code=400, message='订单尚未支付', data={})
    else:
        return api_response(code=400, message='当前状态不可操作', data={})

    order.order_status = new_status
    if new_status == 'waiting_pickup':
        order.pick_up_code = str(random.randint(100000, 999999))
    order.save()
    refresh_daily_stats()
    return api_response(code=200, message='状态更新成功', data=OrderSerializer(order).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def confirm_pickup(request, order_id):
    """用户确认取餐（待取餐→已完成）"""
    try:
        order = Order.objects.get(pk=order_id, user=request.user)
    except Order.DoesNotExist:
        return api_response(code=404, message='订单不存在', data={})
    if order.order_status != 'waiting_pickup':
        return api_response(code=400, message='当前订单状态不可确认取餐', data={})
    order.order_status = 'completed'
    order.save()
    refresh_daily_stats()
    return api_response(code=200, message='取餐确认成功', data=OrderSerializer(order).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def merchant_order_list(request):
    """商家获取所有订单列表"""
    if request.user.role != 'merchant':
        return api_response(code=403, message='仅商家可操作', data={})
    status = request.query_params.get('status')
    orders = Order.objects.all().order_by('-create_time')
    if status:
        orders = orders.filter(order_status=status)
    return api_response(data=OrderSerializer(orders, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def merchant_stats(request):
    """获取商家经营统计数据（从 DailyStats 持久化表读取）"""
    if request.user.role != 'merchant':
        return api_response(code=403, message='仅商家可操作', data={})

    refresh_daily_stats()
    today = timezone.now().date()
    try:
        stats = DailyStats.objects.get(date=today)
    except DailyStats.DoesNotExist:
        return api_response(data={
            'today_orders': 0, 'today_revenue': 0.0,
            'preparing': 0, 'waiting_pickup': 0, 'completed': 0, 'cancelled': 0,
        })
    return api_response(data={
        'today_orders': stats.total_orders,
        'today_revenue': float(stats.total_revenue),
        'preparing': stats.preparing_count,
        'waiting_pickup': stats.waiting_pickup_count,
        'completed': stats.completed_count,
        'cancelled': stats.cancelled_count,
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def merchant_confirm_pickup(request, order_id):
    """商家确认取餐（输入取餐码验证，待取餐→已完成）"""
    if request.user.role != 'merchant':
        return api_response(code=403, message='仅商家可操作', data={})
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return api_response(code=404, message='订单不存在', data={})
    if order.order_status != 'waiting_pickup':
        return api_response(code=400, message='当前订单状态不可确认取餐', data={})
    code = request.data.get('pick_up_code')
    if not code or code != order.pick_up_code:
        return api_response(code=400, message='取餐码错误', data={})
    order.order_status = 'completed'
    order.save()
    refresh_daily_stats()
    return api_response(code=200, message='取餐确认成功', data=OrderSerializer(order).data)
