# -*- coding: utf-8 -*-
"""
系统管理工具包
"""
from .models import Log, GroupToMenu, Menu
from .serializers import MenuSerializer, PermissionSerializer
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from datetime import datetime
from common.log import logger


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


def log_to_db(request, operated_object, operated_type, content, is_success=True):
    """
    操作日志入库
    :param request:
    :param operated_object:操作对象
    :param operated_type:操作类型 删除、新增、修改
    :param content: 操作内容
    :return:
    """
    try:
        now = datetime.now()
        kwargs_log = {
            'operator_date': now,
            'operator': request.user.username,
            'operated_object': operated_object,
            'operated_type': operated_type,
            'content': content,
            'ip_addr': get_ip_addr(request),
            'is_success': is_success,
        }
        Log.objects.create(**kwargs_log)
    except Exception as e:
        logger.exception(e)


def get_filter(source, add_mappings=[], or_mappings=[]):
    """
    通过对应条件获取Q
    :param source: 源数据
    :param add_mappings: 且条件，Ex: [{'url': 'operator', 'db': ['operator__icontains']}]
    :param or_mappings: 或条件，Ex: [{'url': 'operator', 'db': ['operator__icontains']}]
    """
    conn = Q()
    q1 = Q()
    q2 = Q()
    q1.connector = 'AND'
    q2.connector = 'OR'
    # 生成组合查询条件Q
    for add_map in add_mappings:
        if add_map['url'] in source:
            for i in add_map['db']:
                q1.children.append((i, source.get(add_map['url'])))
    for or_map in or_mappings:
        if or_map['url'] in source:
            for j in or_map['db']:
                q2.children.append((j, source.get(or_map['url'])))
    conn.add(q1, 'AND')
    conn.add(q2, 'AND')
    return conn


def get_menu_list_by_groups(group_id_list):
    """
    通过角色获取菜单列表
    :param group_id_list: 组ID列表
    """
    ret = []
    parent_menus_id = set(
        GroupToMenu.objects.filter(group_id__in=group_id_list, menu__parent__isnull=True,
                                   menu__is_menu=True).values_list("menu_id", flat=True)
    )
    child_menus_id = set(
        GroupToMenu.objects.filter(group_id__in=group_id_list, menu__parent__isnull=False,
                                   menu__is_menu=True).values_list("menu_id", flat=True)
    )
    child_menus = Menu.objects.filter(id__in=child_menus_id)
    child_menus_serializer = MenuSerializer(child_menus, many=True)
    child_menus_data = child_menus_serializer.data
    parent_menus = Menu.objects.filter(id__in=parent_menus_id).order_by("id")
    for parent_menu in parent_menus:
        parent_menu_serializer = MenuSerializer(instance=parent_menu)
        parent_menu_data = parent_menu_serializer.data
        parent_menu_data['children'] = [i for i in child_menus_data if i['parent'] == parent_menu.id]
        parent_menu_data['children'].sort(lambda x, y: cmp(x['id'], y['id']))
        ret.append(parent_menu_data)
    return ret


def get_menu_ids_by_groups(group_id_list):
    """
    通过角色获取菜单id列表
    :param group_id_list:
    :return:
    """
    menus_id = set(
        GroupToMenu.objects.filter(group_id__in=group_id_list, menu__is_menu=True).values_list('menu_id', flat=True)
    )
    return menus_id


def get_all_menus():
    """
    获取所有菜单列表
    """
    ret = []
    parent_menus = Menu.objects.filter(parent__isnull=True, is_menu=True).order_by('id')
    child_menus = Menu.objects.filter(parent__isnull=False, is_menu=True).order_by('id')
    child_menus_data = MenuSerializer(instance=child_menus, many=True).data
    for parent_menu in parent_menus:
        parent_menu_serializer = MenuSerializer(instance=parent_menu)
        parent_menu_data = parent_menu_serializer.data
        parent_menu_data['children'] = [i for i in child_menus_data if i['parent'] == parent_menu.id]
        parent_menu_data['children'].sort(lambda x, y: cmp(x['id'], y['id']))
        ret.append(parent_menu_data)
    return ret


def get_all_permissions():
    """
    获取所有权限列表
    """
    permissions = Permission.objects.filter(permissionprofile__is_show=True)
    permissions_serializers = PermissionSerializer(instance=permissions, many=True)
    return permissions_serializers.data


def get_group_ids_by_user(username):
    """
    通过用户名获取角色id列表
    :param username: 用户名称
    :return: group_ids
    """
    user_model = get_user_model()
    user = user_model.objects.get(username=username)
    # 判断该用户是否为超级用户
    if user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = user.groups.all()
    group_ids = groups.values_list('id', flat=True)
    return group_ids


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
