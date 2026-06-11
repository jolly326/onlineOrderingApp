"""
购物车信号处理

用户注册后自动创建购物车。
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.apps.users.models import User
from backend.apps.cart.models import Cart


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """
    用户创建时自动创建购物车

    Args:
        sender: 模型类（User）
        instance: 用户实例
        created: 是否新创建
    """
    if created:
        Cart.objects.create(user=instance)
