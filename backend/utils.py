"""
Django REST Framework 自定义异常处理器与通用工具

统一所有接口的响应和错误格式：{"code": xxx, "message": "xxx", "data": {}}
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def custom_exception_handler(exc, context):
    """
    自定义异常处理器，统一错误响应格式

    Args:
        exc: 异常对象
        context: 异常上下文

    Returns:
        Response: 统一格式的错误响应
    """
    response = exception_handler(exc, context)

    if response is not None:
        detail = response.data
        if isinstance(detail, dict):
            first_error = list(detail.values())[0]
            if isinstance(first_error, list):
                message = str(first_error[0])
            else:
                message = str(first_error)
        elif isinstance(detail, list):
            message = str(detail[0])
        else:
            message = str(detail)

        response.data = {
            'code': response.status_code,
            'message': message,
            'data': {}
        }
    else:
        response = Response({
            'code': 500,
            'message': '服务器内部错误',
            'data': {}
        }, status=500)

    return response


def api_response(code=200, message='success', data=None):
    """
    生成统一格式的成功响应

    Args:
        code: 状态码，默认200
        message: 消息，默认'success'
        data: 返回数据，默认{}

    Returns:
        Response: 统一格式的成功响应
    """
    return Response({
        'code': code,
        'message': message,
        'data': data if data is not None else {}
    })


def get_tokens_for_user(user):
    """
    为指定用户生成JWT令牌对

    Args:
        user: User模型实例

    Returns:
        dict: 包含access和refresh令牌的字典
    """
    refresh = RefreshToken()
    refresh['user_id'] = str(user.user_id)
    refresh['role'] = user.role
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
