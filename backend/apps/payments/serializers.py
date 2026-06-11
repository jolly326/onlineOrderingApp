"""
支付模块序列化器
"""
from rest_framework import serializers


class CreatePaymentSerializer(serializers.Serializer):
    """发起支付序列化器"""
    order_id = serializers.CharField()
    pay_type = serializers.ChoiceField(choices=['wechat', 'alipay'])
