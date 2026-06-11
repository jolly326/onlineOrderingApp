"""
自定义 JWT 认证

解决 SimpleJWT 与自定义 User 模型的集成问题。
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings

from backend.apps.users.models import User


class CustomJWTAuthentication(JWTAuthentication):
    """
    自定义 JWT 认证类

    重写 get_user 方法，使用自定义 User 模型查找用户。
    添加 user 对象所必需的属性兼容。
    """

    def get_user(self, validated_token):
        """
        根据 token 中的 user_id 查找自定义用户

        Args:
            validated_token: 已验证的 JWT token

        Returns:
            User: 自定义用户实例

        Raises:
            AuthenticationFailed: 用户不存在或未激活
        """
        user_id_claim = settings.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')

        try:
            user_id = validated_token[user_id_claim]
        except KeyError:
            raise InvalidToken('Token中未包含用户标识')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('用户不存在', code='user_not_found')

        # 添加 is_active 属性（SimpleJWT 需要）
        user.is_active = True

        return user
