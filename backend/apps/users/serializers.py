"""
用户模块序列化器

处理注册、登录和个人信息的序列化与校验。
"""
from rest_framework import serializers

from backend.apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """注册序列化器 - 验证并创建用户"""
    password = serializers.CharField(write_only=True, min_length=6, max_length=128)
    role = serializers.ChoiceField(choices=['user', 'merchant'], default='user', write_only=True)

    class Meta:
        model = User
        fields = ['username', 'phone', 'password', 'role']

    def validate_phone(self, value):
        """校验手机号格式和唯一性"""
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError('手机号必须为11位数字')
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已注册')
        return value

    def create(self, validated_data):
        """创建用户"""
        user = User(
            username=validated_data['username'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user'),
        )
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """登录序列化器 - 验证用户名和密码"""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """校验用户名和密码"""
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名不存在')

        if user.password != password:
            raise serializers.ValidationError('密码错误')

        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """用户信息序列化器 - 查看和修改个人信息"""
    class Meta:
        model = User
        fields = ['user_id', 'username', 'phone', 'avatar', 'role', 'create_time']
        read_only_fields = ['user_id', 'phone', 'role', 'create_time']
