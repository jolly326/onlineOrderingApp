import uuid

from django.db import models


def uuid_hex():
    """生成32位无连字符UUID"""
    return uuid.uuid4().hex


class User(models.Model):
    """
    用户模型

    支持普通用户（user）和商家（merchant）两种角色。
    """
    ROLE_CHOICES = [
        ('user', '普通用户'),
        ('merchant', '商家'),
    ]

    user_id = models.CharField(
        primary_key=True,
        max_length=32,
        default=uuid_hex,
        editable=False,
        verbose_name='用户ID'
    )
    username = models.CharField(max_length=20, verbose_name='昵称')
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    password = models.CharField(max_length=128, verbose_name='密码')
    avatar = models.CharField(max_length=255, null=True, blank=True, verbose_name='头像URL')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='角色')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return f'{self.username}({self.phone})'

    @property
    def is_authenticated(self):
        """满足 DRF IsAuthenticated 权限检查"""
        return True


