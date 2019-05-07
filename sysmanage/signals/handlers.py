# -*- coding: utf-8 -*-

"""
信号处理
"""

import traceback
import os
import json
from django.db import transaction
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from common.log import logger
from component.utils.basic import now

GROUP_JSON = os.path.join(settings.PROJECT_ROOT, 'sysmanage/fixtures/group_data.json')
PERMISSION_JSON = os.path.join(settings.PROJECT_ROOT, 'sysmanage/fixtures/permission_data.json')
PERMISSION_GROUP_JSON = os.path.join(settings.PROJECT_ROOT, 'sysmanage/fixtures/permission_group_permission.json')
MENU_DATA_JSON = os.path.join(settings.PROJECT_ROOT, 'sysmanage/fixtures/menu_data.json')
GROUP_MENU_JSON = os.path.join(settings.PROJECT_ROOT, 'sysmanage/fixtures/group_menu.json')
GROUP_USER_JSON = os.path.join(settings.PROJECT_ROOT, 'sysmanage/fixtures/group_user.json')
SETTING_JSON = os.path.join(settings.PROJECT_ROOT, 'sysmanage/fixtures/setting.json')


def save_permission_handler(sender, instance, **kwargs):
    """创建/更新权限"""
    from sysmanage.models import PermissionProfile
    # 获取profile字段
    profile_fields = [f.name for f in PermissionProfile._meta.fields if f.name != 'id']
    profile_instance_value = {}
    for profile_field in profile_fields:
        if hasattr(instance, profile_field):
            attr_value = getattr(instance, profile_field)
            profile_instance_value.update(**{profile_field: attr_value})
    PermissionProfile.objects.update_or_create(defaults=profile_instance_value, permission_id=instance.id)


def save_group_handler(sender, instance, **kwargs):
    """创建/更新组"""
    from sysmanage.models import GroupProfile
    # 获取profile字段
    profile_fields = [f.name for f in GroupProfile._meta.fields if f.name != 'id']
    profile_instance_value = {}
    for profile_field in profile_fields:
        if hasattr(instance, profile_field):
            attr_value = getattr(instance, profile_field)
            profile_instance_value.update(**{profile_field: attr_value})
    GroupProfile.objects.update_or_create(defaults=profile_instance_value, group_id=instance.id)


def init_group(group_model):
    """初始化角色数据"""
    with open(GROUP_JSON) as f:
        group_data = json.load(f)
    with transaction.atomic():
        # 首先清空数据
        group_model.objects.all().delete()
        for i in group_data:
            group = group_model.objects.create(id=i['id'], name=i['name'])
            group.display_name = i['display_name']
            group.is_built_in = i['is_built_in']
            group.save()


def init_permission(permission_model, permission_profile_model):
    """初始化权限数据"""
    with open(PERMISSION_JSON) as f:
        permission_data = json.load(f)
    permission_profile_model.objects.all().delete()
    for j in permission_data:
        try:
            permission = permission_model.objects.filter(codename=j["codename"])
            if permission:
                permission_profile_model.objects.create(display_name=j['display_name'],
                                                        permission=permission_model.objects.get(codename=j["codename"]))
            else:
                permission_info = permission_model.objects.create(name=j["codename"],
                                                                  content_type=ContentType.objects.get(
                                                                      model=j['model_name']),
                                                                  codename=j["codename"])
                permission_info.display_name = j['display_name']
                permission_info.save()
        except Exception as e:
            print traceback.format_exc()


def init_permission_group(permission_group_model, permission_profile_model):
    """初始化权限分组数据和分组与权限的对应关系"""
    with open(PERMISSION_GROUP_JSON) as f:
        permission_groups = json.load(f)
    permission_group_model.objects.all().delete()
    bulk_list = [permission_group_model(id=i['id'], display_name=i['display_name']) for i in permission_groups]
    permission_group_model.objects.bulk_create(bulk_list)
    # 绑定分组和权限的对应关系
    for permission_group in permission_groups:
        permission_profile_model.objects.filter(
            permission__codename__in=permission_group.get('codename_list', [])).update(
            permission_group_id=permission_group['id']
        )


def init_menu(menu_data_model):
    """初始化菜单数据"""
    with open(MENU_DATA_JSON) as f:
        menu_data = json.load(f)
    menu_data_model.objects.all().delete()
    for j in menu_data:
        try:
            menu_data_model.objects.create(**j)
        except Exception as e:
            print traceback.format_exc()


def init_group_to_menu(group_to_menu_model):
    """初始化角色和菜单多对多数据"""
    with open(GROUP_MENU_JSON) as f:
        group_menus = json.load(f)
    group_to_menu_model.objects.all().delete()
    bulk_list = []
    for group_menu in group_menus:
        for i in group_menu['menu_id_list']:
            bulk_list.append(group_to_menu_model(group_id=group_menu['group_id'], menu_id=i))
    group_to_menu_model.objects.bulk_create(bulk_list)


def init_group_to_user(group_model, user_model):
    """初始化角色和用户的多对多关系"""
    with open(GROUP_USER_JSON) as f:
        group_users = json.load(f)
    for group_user_names in group_users:
        group = group_model.objects.get(id=group_user_names['group_id'])
        group.user_set.clear()
        users = [user_model.objects.get(username=i) for i in group_user_names['username_list']]
        group.user_set.add(*users)


def init_setting(setting_model):
    """初始化设置项数据"""
    with open(SETTING_JSON) as f:
        settings = json.load(f)
    setting_model.objects.all().delete()
    bulk_list = [setting_model(name=i['name'], value=i['value'], type=i.get('type', 'str')) for i in settings]
    setting_model.objects.bulk_create(bulk_list)


def init_data_handler(sender, **kwargs):
    """初始化auth数据"""
    setting_model = sender.get_model('Setting')
    settings_infos = setting_model.objects.filter(name='sysmanage_init_data')
    # 判断是否需要初始化数据
    if not settings_infos:
        is_init_data = True
    elif settings_infos.first().get_value():
        is_init_data = True
    else:
        is_init_data = False
    if is_init_data:
        print 'init system data...'
        from account.models import BkUser
        from django.contrib.auth.models import Group, Permission
        init_setting(setting_model)
        # 初始化超级管理员
        BkUser.objects.update_or_create(defaults={'is_staff': True, 'is_superuser': True}, username='admin')
        init_group(Group)
        permission_profile_model = sender.get_model('PermissionProfile')
        init_permission(Permission, permission_profile_model)
        permission_group_model = sender.get_model('PermissionGroup')
        init_permission_group(permission_group_model, permission_profile_model)
        menu_data_model = sender.get_model('Menu')
        init_menu(menu_data_model)
        group_to_menu_model = sender.get_model('GroupToMenu')
        init_group_to_menu(group_to_menu_model)
        init_group_to_user(Group, BkUser)
        # 绑定超级管理员默认成员和对应权限
        if Group.objects.filter(id=1).exists():
            group = Group.objects.get(id=1)
            # 组与权限的关系
            permissions = [per_info.permission_id for per_info in permission_profile_model.objects.all()]
            with transaction.atomic():
                group.permissions.clear()
                permission_objs = [Permission.objects.get(id=perm_id) for perm_id in permissions]
                group.permissions.add(*permission_objs)


def log_handler(sender, operator, operated_object, operated_type, content, is_success, **kwargs):
    """操作日志信号处理"""
    from sysmanage.models import Log
    try:
        Log.objects.create(
            operator=operator, operated_object=operated_object, operated_type=operated_type, operator_date=now(),
            content=content, is_success=is_success
        )
    except Exception as e:
        logger.exception(e)
