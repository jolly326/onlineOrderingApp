"""
购物车模块序列化器
"""
from rest_framework import serializers

from backend.apps.cart.models import CartItem, Cart
from backend.apps.dishes.models import Dish
from backend.apps.dishes.serializers import DishSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """购物车项序列化器 - 含菜品详情"""
    dish = DishSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['item_id', 'dish', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        """计算小计金额"""
        return float(obj.dish.price) * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    """购物车序列化器 - 含所有项和合计"""
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cart_id', 'items', 'total']

    def get_total(self, obj):
        """计算购物车总金额"""
        return sum(float(item.dish.price) * item.quantity for item in obj.items.all())


class AddCartItemSerializer(serializers.Serializer):
    """添加菜品到购物车序列化器"""
    dish_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1, max_value=99)

    def validate_dish_id(self, value):
        """校验菜品是否存在且已上架"""
        try:
            dish = Dish.objects.get(pk=value, status=True)
        except Dish.DoesNotExist:
            raise serializers.ValidationError('菜品不存在或已下架')
        return dish

    def create(self, validated_data):
        """添加或合并购物车项"""
        cart = validated_data['cart']
        dish = validated_data['dish_id']
        quantity = validated_data['quantity']

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            dish=dish,
            defaults={'quantity': 0}
        )
        item.quantity = min(item.quantity + quantity, 99)
        item.save()
        return item


class UpdateCartItemSerializer(serializers.Serializer):
    """更新购物车项数量序列化器"""
    quantity = serializers.IntegerField(min_value=1, max_value=99)
