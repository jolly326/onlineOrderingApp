import uuid

from django.db import models


def uuid_hex():
    """生成32位无连字符UUID"""
    return uuid.uuid4().hex


class Dish(models.Model):
    """
    菜品模型

    管理菜品的名称、价格、分类、上下架状态等信息。
    """
    CATEGORY_CHOICES = [
        ('recommended', '推荐'),
        ('signature', '招牌'),
        ('drinks', '饮品'),
        ('snacks', '小吃'),
    ]

    dish_id = models.CharField(
        primary_key=True,
        max_length=32,
        default=uuid_hex,
        editable=False,
        verbose_name='菜品ID'
    )
    dish_name = models.CharField(max_length=50, verbose_name='菜品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='分类')
    images = models.JSONField(default=list, blank=True, null=True, verbose_name='菜品图片列表(images[0]为主图)')
    month_sales = models.IntegerField(default=0, verbose_name='月销量')
    status = models.BooleanField(default=True, verbose_name='状态(1上架/0下架)')

    class Meta:
        db_table = 'dish'
        verbose_name = '菜品'
        verbose_name_plural = '菜品'

    def __str__(self):
        return f'{self.dish_name} - ¥{self.price}'
