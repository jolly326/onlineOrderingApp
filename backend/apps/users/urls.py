"""
用户模块 URL 路由

/users/ 前缀下的所有接口
"""
from django.urls import path

from backend.apps.users import views

urlpatterns = [
    path('register', views.register, name='user-register'),
    path('login', views.login, name='user-login'),
    path('profile', views.profile, name='user-profile'),
]
