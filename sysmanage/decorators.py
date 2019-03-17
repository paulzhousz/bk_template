# -*- coding: utf-8 -*-

from common.log import logger
from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponseForbidden
from conf.default import IS_CHECK_PERM


def perm_required(permission):
    """
    @summary: Model权限装饰器
    @Example: perm_required("home_application.add_company")
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def wrapper(request, *args, **kwargs):
            if IS_CHECK_PERM:
                user = request.user
                if user.has_perm(permission):
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            else:
                return view_func(request, *args, **kwargs)
        return wrapper
    return decorator