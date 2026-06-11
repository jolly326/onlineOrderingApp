"""
菜品模块 URL 路由
"""
from django.urls import path

from backend.apps.dishes import views

urlpatterns = [
    path('', views.dish_list, name='dish-list'),
    path('all', views.dish_all, name='dish-all'),
    path('create', views.dish_create, name='dish-create'),
    path('<str:dish_id>', views.dish_detail, name='dish-detail'),
    path('<str:dish_id>/status', views.dish_status, name='dish-status'),
    path('<str:dish_id>/update', views.dish_update, name='dish-update'),
    path('<str:dish_id>/delete', views.dish_delete, name='dish-delete'),
]
