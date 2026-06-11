import uuid

from django.db import models

from backend.apps.users.models import User
from backend.apps.dishes.models import Dish


def uuid_hex():
    """生成32位无连字符UUID"""
    return uuid.uuid4().hex


class Cart(models.Model):
    """
    购物车模型

    每个用户有且仅有一个购物车（一对一关系）。
    用户注册时自动创建。
    """
    cart_id = models.CharField(
        primary_key=True,
        max_length=32,
        default=uuid_hex,
        editable=False,
        verbose_name='购物车ID'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='关联用户'
    )

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车'
        verbose_name_plural = '购物车'

    def __str__(self):
        return f'购物车({self.user.username})'


class CartItem(models.Model):
    """
    购物车项模型

    记录购物车中每个菜品的数量和关联信息。
    相同菜品添加时会合并数量。
    """
    item_id = models.CharField(
        primary_key=True,
        max_length=32,
        default=uuid_hex,
        editable=False,
        verbose_name='购物车项ID'
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='关联购物车'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='关联菜品'
    )
    quantity = models.IntegerField(default=1, verbose_name='数量')

    class Meta:
        db_table = 'cart_item'
        verbose_name = '购物车项'
        verbose_name_plural = '购物车项'
        unique_together = ('cart', 'dish')

    def __str__(self):
        return f'{self.dish.dish_name} x {self.quantity}'
