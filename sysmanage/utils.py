# -*- coding: utf-8 -*-
"""
系统管理工具包
"""
from .serializers import PermissionSerializer
from django.contrib.auth.models import Permission, ContentType
from django.contrib.auth import get_user_model
from guardian.shortcuts import get_groups_with_perms
from guardian.models import GroupObjectPermission, UserObjectPermission
from collections import defaultdict


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


def get_perms_by_content_type(obj):
    """
    通过obj获取对应权限列表
    """
    ret = []
    content_type = ContentType.objects.get_for_model(obj)
    permissions = Permission.objects.filter(content_type=content_type, permissionprofile__isnull=False,
                                            permissionprofile__is_enable=True)
    for permission in permissions:
        ret.append({
            'display_name': permission.permissionprofile.display_name,
            'name': '.'.join([permission.content_type.app_label, permission.codename])
        })
    return ret


def get_perms_with_groups(obj):
    """获取obj对应的权限以及具有对应权限角色列表"""
    perms = get_perms_by_content_type(obj)
    groups_with_perms = get_groups_with_perms(obj, attach_perms=True)
    perms_dict = defaultdict(list)
    for k, v in groups_with_perms.iteritems():
        for p in v:
            perms_dict[p].append(k.id)
    for perm in perms:
        code_name = perm['name'].split('.')[1]
        perm['groups'] = perms_dict.get(code_name, [])
    return perms


def clear_perms_obj(obj, perms):
    """
    清空obj指定permission列表
    :param obj 权限应用实例
    :param perms codename组成的列表
    """
    content_type = ContentType.objects.get_for_model(obj)
    condename_list = [i.split('.')[-1] for i in perms]
    filters = {
        'object_pk': obj.pk,
        'content_type_id': content_type.id,
        'permission__codename__in': condename_list
    }
    GroupObjectPermission.objects.filter(**filters).delete()
    UserObjectPermission.objects.filter(**filters).delete()


def set_perms_obj(obj, perms, data):
    """
    设置obj指定permission列表
    :param obj 权限应用实例
    :param perms codename组成的列表
    :param data request的body参数
    """
    # 清空关联权限
    clear_perms_obj(obj, perms)
    content_type = ContentType.objects.get_for_model(obj)
    bulk_list = []
    # 设置关联权限
    for perm_groups in data:
        permission = Permission.objects.get(content_type_id=content_type.id,
                                            codename=perm_groups['name'].split('.')[-1])
        for group_id in perm_groups['groups']:
            bulk_list.append(GroupObjectPermission(object_pk=obj.pk, content_type_id=content_type.pk,
                                                   permission_id=permission.pk, group_id=group_id))
    GroupObjectPermission.objects.bulk_create(bulk_list)