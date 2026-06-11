"""
购物车模块视图

提供购物车查询、添加/删除菜品、修改数量和清空接口。
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from backend.apps.cart.models import Cart, CartItem
from backend.apps.cart.serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from backend.utils import api_response


def _get_cart(user):
    """获取用户购物车，不存在则自动创建"""
    try:
        return user.cart
    except Exception:
        return Cart.objects.create(user=user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    """
    获取当前用户的购物车（自动过滤已下架菜品）

    Args:
        request: GET请求

    Returns:
        Response: 购物车详情（含菜品列表、合计金额）
    """
    cart = _get_cart(request.user)
    # 自动清除已下架菜品
    CartItem.objects.filter(cart=cart, dish__status=False).delete()
    return api_response(data=CartSerializer(cart, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item(request):
    """
    添加菜品到购物车（相同菜品自动合并数量）

    Args:
        request: POST请求，包含dish_id和quantity

    Returns:
        Response: 更新后的购物车
    """
    cart = _get_cart(request.user)
    serializer = AddCartItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(cart=cart)
    return api_response(code=200, message='添加成功', data=CartSerializer(cart, context={'request': request}).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    """
    修改购物车项数量

    Args:
        request: PUT请求，包含quantity
        item_id: 购物车项ID

    Returns:
        Response: 更新后的购物车
    """
    cart = _get_cart(request.user)
    try:
        item = CartItem.objects.get(pk=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return api_response(code=404, message='购物车项不存在', data={})

    serializer = UpdateCartItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    item.quantity = serializer.validated_data['quantity']
    item.save()
    return api_response(code=200, message='修改成功', data=CartSerializer(cart, context={'request': request}).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    """
    删除购物车项

    Args:
        request: DELETE请求
        item_id: 购物车项ID

    Returns:
        Response: 更新后的购物车
    """
    cart = _get_cart(request.user)
    try:
        item = CartItem.objects.get(pk=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return api_response(code=404, message='购物车项不存在', data={})

    item.delete()
    return api_response(code=200, message='删除成功', data=CartSerializer(cart, context={'request': request}).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """
    清空购物车

    Args:
        request: DELETE请求

    Returns:
        Response: 空购物车
    """
    cart = _get_cart(request.user)
    cart.items.all().delete()
    return api_response(code=200, message='已清空', data=CartSerializer(cart, context={'request': request}).data)
