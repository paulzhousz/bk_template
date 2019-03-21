# -*- coding: utf-8 -*-
"""
系统管理工具包
"""
from .serializers import PermissionSerializer
from django.contrib.auth.models import Permission, ContentType
from django.contrib.auth import get_user_model


def get_mapping(from_data, mappings, is_abandon=True):
    """
    通过映射关系获取映射后数据
    :param from_data: 映射前数据
    :param mappings: 映射关系
    :param is_abandon: 未匹配是否舍弃
    """
    to_data = {}
    for key, value in from_data.items():
        # 是否匹配
        is_match = False
        for map in mappings:
            if key == map['from']:
                to_data.update(**{map['to']: value})
                is_match = True
                break
        if not (is_abandon or is_match):
            to_data.update(**{key: value})
    return to_data


def get_ip_addr(request):
    """
    通过request获取对象IP
    :param request:
    :return:
    """
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']


def get_all_permissions():
    """
    获取所有权限列表
    """
    permissions = Permission.objects.filter(permissionprofile__is_show=True)
    permissions_serializers = PermissionSerializer(instance=permissions, many=True)
    return permissions_serializers.data


def get_permissions_by_user(username):
    """
    通过用户名获取所有权限列表
    :param username: 用户名称
    :return:
    """
    user_model = get_user_model()
    user = user_model.objects.get(username=username)
    permissions = user.get_all_permissions()
    return permissions


def get_permissions_by_instance(instance):
    """
    通过instance获取对应权限列表
    """
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
    permissions = Permission.objects.filter(content_type=content_type, permissionprofile__isnull=False,
                                            permissionprofile__is_enable=True)
    return ['.'.join([permission.content_type.app_label, permission.codename]) for permission in permissions]
