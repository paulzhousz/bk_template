# -*- coding: utf-8 -*-
"""
用于本地开发环境的全局配置
"""
from settings import APP_ID, MIDDLEWARE_CLASSES


# ===============================================================================
# 数据库设置, 本地开发数据库设置
# ===============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': APP_ID,                        # 数据库名 (默认与APP_ID相同)
    },
}

# ==============================================================================
# Middleware and apps
# ==============================================================================
CELERY_ALWAYS_EAGER = True
MIDDLEWARE_CLASSES += (
    'corsheaders.middleware.CorsMiddleware',
    'account.middlewares.DisableCSRFCheck',  # 本地不需要校验CSRF
)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True