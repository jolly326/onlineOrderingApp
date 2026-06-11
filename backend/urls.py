"""
URL configuration for backend project.

API 基础路径：/api/v1/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    # ========== API v1 ==========
    path('api/v1/users/', include('backend.apps.users.urls')),
    path('api/v1/dishes/', include('backend.apps.dishes.urls')),
    path('api/v1/cart/', include('backend.apps.cart.urls')),
    path('api/v1/orders/', include('backend.apps.orders.urls')),
    path('api/v1/payments/', include('backend.apps.payments.urls')),
]

# 开发环境提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
