# -*- coding: utf-8 -*-
"""
用于SAAS环境的全局配置
"""
import os
from settings import MIDDLEWARE_CLASSES


# ===============================================================================
# 数据库设置, 正式环境数据库设置
# ===============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',      # 默认用mysql
        'NAME': os.environ.get('DB_NAME'),         # 数据库名 (默认与APP_ID相同)
        'USER': os.environ.get('DB_USERNAME'),     # 你的数据库user
        'PASSWORD': os.environ.get('DB_PASSWORD'), # 你的数据库password
        'HOST': os.environ.get('DB_HOST'),         # 数据库HOST
        'PORT': os.environ.get('DB_PORT'),         # 默认3306
    },
}

# ==============================================================================
# Middleware and apps
# ==============================================================================
MIDDLEWARE_CLASSES += (
    'corsheaders.middleware.CorsMiddleware',
    'account.middlewares.DisableCSRFCheck',  # 本地不需要校验CSRF
)