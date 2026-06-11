"""
用户模块视图

提供注册、登录和个人信息管理接口。
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from backend.apps.users.serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from backend.utils import api_response, get_tokens_for_user


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    用户注册

    接收手机号、昵称、密码，注册成功后返回用户信息和JWT令牌。

    Args:
        request: POST请求，包含username, phone, password

    Returns:
        Response: 用户信息 + JWT令牌
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    tokens = get_tokens_for_user(user)
    return api_response(code=200, message='注册成功', data={
        'user': UserProfileSerializer(user).data,
        'tokens': tokens,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    用户登录

    接收手机号和密码，校验成功后返回JWT令牌。

    Args:
        request: POST请求，包含phone, password

    Returns:
        Response: 用户信息 + JWT令牌
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    tokens = get_tokens_for_user(user)
    return api_response(code=200, message='登录成功', data={
        'user': UserProfileSerializer(user).data,
        'tokens': tokens,
    })


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    获取/修改个人信息

    GET: 返回当前用户信息
    PUT: 修改昵称或头像

    Args:
        request: GET或PUT请求

    Returns:
        Response: 用户信息
    """
    user = request.user

    if request.method == 'GET':
        return api_response(data=UserProfileSerializer(user).data)

    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return api_response(code=200, message='更新成功', data=serializer.data)
