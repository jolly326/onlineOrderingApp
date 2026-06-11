"""
菜品模块序列化器
"""
from rest_framework import serializers
from django.core.files.storage import default_storage

from backend.apps.dishes.models import Dish


def _build_image_url(image_path, request=None):
    """将存储路径转为完整 URL"""
    if not image_path:
        return None
    media_url = default_storage.url(image_path)
    if request is not None:
        return request.build_absolute_uri(media_url)
    return media_url


class DishSerializer(serializers.ModelSerializer):
    """菜品序列化器 - image 从 images[0] 派生"""
    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ['dish_id', 'dish_name', 'price', 'category', 'image', 'images', 'month_sales', 'status']

    def get_images(self, obj):
        request = self.context.get('request')
        return [_build_image_url(p, request) for p in (obj.images or []) if p]

    def get_image(self, obj):
        """主图取 images[0]"""
        if not obj.images or not obj.images[0]:
            return None
        return _build_image_url(obj.images[0], self.context.get('request'))


class DishCreateSerializer(serializers.ModelSerializer):
    """创建菜品序列化器（图片在视图中手动处理）"""

    class Meta:
        model = Dish
        fields = ['dish_name', 'price', 'category']


class DishUpdateSerializer(serializers.ModelSerializer):
    """更新菜品序列化器（图片在视图中手动处理）"""

    class Meta:
        model = Dish
        fields = ['dish_name', 'price', 'category']


class DishStatusSerializer(serializers.Serializer):
    """菜品上下架序列化器"""
    status = serializers.BooleanField()
