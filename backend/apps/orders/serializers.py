"""
订单模块序列化器
"""
from rest_framework import serializers

from backend.apps.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """订单项序列化器"""
    class Meta:
        model = OrderItem
        fields = ['order_item_id', 'dish_name', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器 - 含订单项"""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'total_money', 'order_status',
            'pick_up_code', 'pay_deadline', 'create_time', 'items'
        ]


class OrderStatusSerializer(serializers.Serializer):
    """订单状态更新序列化器"""
    order_status = serializers.ChoiceField(choices=[
        'preparing', 'waiting_pickup', 'completed', 'cancelled'
    ])

    def validate_order_status(self, value):
        """校验状态更新的合法性（商家前端控制）"""
        valid_transitions = {
            'pending_payment': ['cancelled'],
            'preparing': ['waiting_pickup'],
            'waiting_pickup': ['completed'],
        }
        return value
