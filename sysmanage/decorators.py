# -*- coding: utf-8 -*-

"""
装饰器
"""

from functools import wraps
from django.utils.decorators import available_attrs
from rest_framework.exceptions import PermissionDenied


def surperuser_required(view_func):
    """
    装饰器检查当前用户是不是超级管理员
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied(detail=u'该用户没有该权限功能')
    return wrapper
