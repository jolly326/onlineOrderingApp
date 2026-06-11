from django.contrib import admin

from backend.apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """用户管理后台"""
    list_display = ['username', 'phone', 'role', 'create_time']
    list_filter = ['role']
    search_fields = ['username', 'phone']
    readonly_fields = ['user_id', 'create_time']
