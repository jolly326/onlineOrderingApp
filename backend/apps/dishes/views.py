"""
菜品模块视图

提供菜品列表、详情和上下架接口。
图片全部存入 dish.images JSON 数组（images[0] 为主图）。
"""
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from backend.apps.dishes.models import Dish
from backend.apps.dishes.serializers import DishSerializer, DishCreateSerializer, DishStatusSerializer, DishUpdateSerializer
from backend.utils import api_response


# ======================== 图片处理工具函数 ========================

def _save_uploaded_image(uploaded_file):
    """保存上传的图片文件到 media/dishes/，返回相对路径"""
    file_name = f"dishes/{get_valid_filename(uploaded_file.name)}"
    return default_storage.save(file_name, uploaded_file)


def _get_uploaded_images(request):
    """从请求中获取上传的图片文件列表（支持 image 和 images 字段）"""
    uploaded_images = request.FILES.getlist('images')
    if not uploaded_images:
        single_image = request.FILES.get('image')
        if single_image is not None:
            uploaded_images = [single_image]
    return uploaded_images


# ======================== 用户端接口 ========================

@api_view(['GET'])
@permission_classes([AllowAny])
def dish_list(request):
    """获取上架菜品列表"""
    category = request.query_params.get('category')
    dishes = Dish.objects.filter(status=True)
    if category:
        dishes = dishes.filter(category=category)
    dishes = dishes.order_by('-month_sales')
    return api_response(data=DishSerializer(dishes, many=True, context={'request': request}).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def dish_detail(request, dish_id):
    """获取菜品详情"""
    try:
        dish = Dish.objects.get(pk=dish_id, status=True)
    except Dish.DoesNotExist:
        return api_response(code=404, message='菜品不存在', data={})
    return api_response(data=DishSerializer(dish, context={'request': request}).data)


# ======================== 商家端接口 ========================

@api_view(['GET'])
@permission_classes([AllowAny])
def dish_all(request):
    """商家获取所有菜品（含下架）"""
    dishes = Dish.objects.all().order_by('-status', 'category')
    return api_response(data=DishSerializer(dishes, many=True, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dish_create(request):
    """新增菜品（仅商家）"""
    if request.user.role != 'merchant':
        return api_response(code=403, message='仅商家可操作', data={})

    serializer = DishCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    dish = serializer.save()

    # 图片存入 images[0]
    uploaded = _get_uploaded_images(request)
    if uploaded:
        dish.images = [_save_uploaded_image(uploaded[0])]
        dish.save()

    return api_response(code=201, message='创建成功', data=DishSerializer(dish, context={'request': request}).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def dish_update(request, dish_id):
    """更新菜品（仅商家）"""
    if request.user.role != 'merchant':
        return api_response(code=403, message='仅商家可操作', data={})

    try:
        dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return api_response(code=404, message='菜品不存在', data={})

    serializer = DishUpdateSerializer(dish, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    # 处理图片删除标记
    if request.data.get('remove_image') == 'true':
        for old_path in (dish.images or []):
            if old_path and default_storage.exists(old_path):
                default_storage.delete(old_path)
        dish.images = []

    # 上传新图则替换
    uploaded = _get_uploaded_images(request)
    if uploaded:
        for old_path in (dish.images or []):
            if old_path and default_storage.exists(old_path):
                default_storage.delete(old_path)
        dish.images = [_save_uploaded_image(uploaded[0])]

    dish.save()

    return api_response(code=200, message='修改成功', data=DishSerializer(dish, context={'request': request}).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def dish_status(request, dish_id):
    """上下架菜品（仅商家）"""
    if request.user.role != 'merchant':
        return api_response(code=403, message='仅商家可操作', data={})

    try:
        dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return api_response(code=404, message='菜品不存在', data={})

    serializer = DishStatusSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    dish.status = serializer.validated_data['status']
    dish.save()
    return api_response(code=200, message='操作成功', data=DishSerializer(dish, context={'request': request}).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def dish_delete(request, dish_id):
    """删除菜品（仅商家）"""
    if request.user.role != 'merchant':
        return api_response(code=403, message='仅商家可操作', data={})

    try:
        dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return api_response(code=404, message='菜品不存在', data={})

    # 清理图片文件
    for image_path in (dish.images or []):
        if image_path and default_storage.exists(image_path):
            default_storage.delete(image_path)

    dish.delete()
    return api_response(code=200, message='删除成功', data={})
