"""
Django settings for backend project.
"""
import json
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# 从 config.json 读取敏感配置
_config_path = BASE_DIR / 'backend' / 'config.json'
if _config_path.exists():
    with open(_config_path) as _f:
        _config = json.load(_f)
else:
    _config = {}

SECRET_KEY = _config.get('SECRET_KEY', 'fallback-dev-key-change-in-production')

DEBUG = True

ALLOWED_HOSTS = ['*']

# ------------------------------------------------
# 应用注册
# ------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方库
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    # 业务模块
    'backend.apps.users',
    'backend.apps.dishes',
    'backend.apps.cart',
    'backend.apps.orders',
    'backend.apps.payments',
]

# ------------------------------------------------
# 中间件
# ------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# ------------------------------------------------
# 数据库（MySQL 8.0）
# ------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'onlineOrder',
        'USER': 'root',
        'PASSWORD': _config.get('DB_PASSWORD', ''),
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ------------------------------------------------
# 密码校验
# ------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------
# 国际化 - 中国时区
# ------------------------------------------------
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------
# 静态文件 & 媒体文件
# ------------------------------------------------
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------
# CORS 跨域配置（开发环境允许前端localhost:5173）
# ------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'x-requested-with',
]

# ------------------------------------------------
# Django REST Framework 配置
# ------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'backend.auth.CustomJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'EXCEPTION_HANDLER': 'backend.utils.custom_exception_handler',
}

# ------------------------------------------------
# SimpleJWT 配置
# ------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),           # 7天过期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),         # 30天刷新
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'user_id',                           # 使用自定义user_id字段
}
