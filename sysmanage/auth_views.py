# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from blueking.component.shortcuts import get_client_by_user
from django.utils import timezone
from sysmanage.utils import get_mapping, get_filter
from sysmanage.models import GroupToMenu, Menu, GroupProfile
from common.mymako import render_json, render_mako_context
from common.log import logger
from .serializers import UserSerializer, GroupSerializer, GroupProfileSerializer, UserInfoSerializer, MenuSerializer
from rest_framework.parsers import JSONParser
from .utils import get_all_menus, get_all_permissions, log_to_db
from sysmanage.decorators import perm_required
from django.core import serializers
import json
import requests
from django.db.models import Q
from django.http import JsonResponse
from account.models import BkUser
from django.db import models
from monitor.application_object.models import GroupToPerApplication
from monitor.os_object.models import GroupToPerAgent, GroupToPerMonitorObject


@perm_required('account.sync_bkuser')
def sync_user(request):
    """
    同步用户
    """
    try:
        # bk用户和app用户字段映射
        user_maps = [
            {'from': 'bk_username', 'to': 'username'},
            {'from': 'chname', 'to': 'chname'},
            {'from': 'phone', 'to': 'phone'},
            {'from': 'email', 'to': 'email'},
        ]
        user_model = get_user_model()
        client = get_client_by_user(request.user.username)
        result = client.bk_login.get_all_users()
        username_list = []
        if result['result']:
            user_list = result['data']
            for user in user_list:
                to_user = get_mapping(user, user_maps)
                username_list.append(to_user['username'])
                user_model.objects.update_or_create(defaults=to_user, username=to_user['username'])
            user_model.objects.exclude(username__in=username_list).delete()
            response = render_json({'result': True, 'message': u'立即同步成功'})
            operated_object = u'用户'
            operated_type = u'同步'
            content = u'同步用户成功'
            log_to_db(request, operated_object, operated_type, content)
        else:
            response = render_json({'result': False, 'message': u'同步失败，请联系管理员'})
            operated_object = u'用户'
            operated_type = u'同步'
            content = u'同步用户失败'
            log_to_db(request, operated_object, operated_type, content)
        return response
    except Exception as e:
        logger.exception('%s' % e)
        # log
        operated_object = u'用户'
        operated_type = u'同步'
        content = u'同步用户失败'
        log_to_db(request, operated_object, operated_type, content)
        return render_json({'result': False, 'message': u'立即同步失败', 'error': '%s' % e})


def get_user_list(request):
    """
    获取用户列表
    """
    try:
        params_dict = request.GET
        or_mappings = [
            {'url': 'keyword',
             'db': ['username__icontains', 'chname__icontains', 'phone__icontains', 'email__icontains']}
        ]
        q = get_filter(params_dict, or_mappings=or_mappings)
        user_model = get_user_model()
        users = user_model.objects.filter(q & Q(is_in_app=1))
        # 每页多少条数据
        per_page = params_dict.get('pageCount', 10)
        paginator = Paginator(users, per_page)
        try:
            user_page = paginator.page(params_dict.get('currentPage', 1))
        except PageNotAnInteger:
            user_page = paginator.page(1)
        except EmptyPage:
            # 指定页码超出范围
            user_page = paginator.page(paginator.num_pages)
        user_serializer = UserSerializer(user_page, many=True)
        # 该用户是否能被删除  超级管理员不可进行删除
        username_list = list(get_user_model().objects.filter(is_staff=True).values_list('username', flat=True))
        username_list.append(request.user.username)
        for user_data in user_serializer.data:
            if user_data['username'] in username_list:
                user_data.update(can_delete=False)
            else:
                user_data.update(can_delete=True)
        return render_json(
            {'result': True, 'code': 0, 'message': u'获取用户列表成功',
             'data': {'user': user_serializer.data, 'count': paginator.count}}
        )
    except Exception as e:
        logger.exception('%s' % e)
        return render_json({'result': False, 'message': u'获取用户列表失败', 'error': '%s' % e})


def get_not_added_user_list(request):
    """
    待添加的用户
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_list = BkUser.objects.filter(is_in_app=0, is_able=0)
        json_data = serializers.serialize('json', user_list, fields=('username', 'chname', 'email',
                                                                     'phone'))
        json_data = json.loads(json_data)
        return JsonResponse({"result": True, "data": json_data, "message": "获取数据成功"}, safe=False)
    else:
        result = {'result': False, "data": "", "message": "请求错误"}
        logger.exception('request error')
        return JsonResponse(result)


@perm_required('account.add_bkuser')
def add_user(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_id = json.loads(request.body).get('user_id', '')
        group_id_list = json.loads(request.body).get('group_id_list', '')
        BkUser.objects.filter(id=user_id).update(is_in_app=1, is_able=1, date_joined=timezone.now())
        for group_id in group_id_list:
            group = Group.objects.get(id=group_id)
            with transaction.atomic():
                group.user_set.clear()
                user_info = BkUser.objects.get(id=user_id)
                group.user_set.add(user_info)
        # log
        operated_object = u'用户'
        operated_type = u'添加'
        username = BkUser.objects.get(id=user_id).username
        content = u'添加{}用户成功'.format(username)
        log_to_db(request, operated_object, operated_type, content)

        result = {"result": True, "data": '', "message": "添加用户成功"}
        return JsonResponse(result)
    else:
        result = {"result": False, "data": '', "message": "请求错误"}
        logger.exception('request error')
        return JsonResponse(result)


@perm_required('account.change_bkuser')
def edit_user(request):
    """
    编辑用户  修改用户角色
    :param user_id  用户id
    :param group_id  角色ID
    :param request:
            eg:{"kpi_id_id","1","display_name":"显示名称"}
    """
    if request.method == 'POST':
        try:
            user_id = json.loads(request.body).get("user_id", "")
            group_id_list = json.loads(request.body).get("group_id_list", "")
            BkUser.objects.get(id=user_id).groups.clear()
            for group_info in group_id_list:
                group_info = Group.objects.get(id=group_info)
                BkUser.objects.get(id=user_id).groups.add(group_info)
            # log
            operated_object = u'用户'
            operated_type = u'修改'
            username = BkUser.objects.get(id=user_id).username
            content = u'修改{}用户角色成功'.format(username)
            log_to_db(request, operated_object, operated_type, content)

        except Exception as e:
            # log
            operated_object = u'用户'
            operated_type = u'修改'
            content = u'修改用户角色成功失败'
            log_to_db(request, operated_object, operated_type, content)

            result = {'result': False, "data": "", "message": "修改失败"}
            logger.exception(e)
            return JsonResponse(result)
        result = {'result': True, "data": "", "message": "修改成功"}
        return JsonResponse(result)
    else:
        result = {'result': False, "data": "", "message": "请求错误"}
        logger.exception('request error')
        return JsonResponse(result)


@perm_required('account.down_bkuser')
def disable_user(request):
    """
    禁用账号
    """
    try:
        data = JSONParser().parse(request)
        id_list = data['id_list']
        user_model = get_user_model()
        # 用户是否存在
        for user_info in id_list:
            if user_model.objects.filter(id=user_info).exists():
                # 用户不能删除自己
                if request.user.id in id_list:
                    # log
                    operated_object = u'用户'
                    operated_type = u'禁用'
                    content = u'禁用用户失败，不能禁用自身账号'
                    log_to_db(request, operated_object, operated_type, content)
                    return render_json({'result': False, 'message': u'禁用用户失败，不能禁用自身账号'})
                else:
                    BkUser.objects.filter(id=user_info).update(is_able=0)
                    # log
                    operated_object = u'用户'
                    operated_type = u'禁用'
                    username = BkUser.objects.get(id=user_info)
                    content = u'禁用{}用户成功'.format(username)
                    log_to_db(request, operated_object, operated_type, content)
            else:
                # log
                operated_object = u'用户'
                operated_type = u'禁用'
                content = u'禁用用户失败，该用户不存在'
                log_to_db(request, operated_object, operated_type, content)
                return render_json({'result': False, 'message': u'禁用用户失败，该用户不存在'})
        return render_json({'result': True, 'message': u'禁用用户成功'})
    except Exception as e:
        logger.exception('%s' % e)
        return render_json({'result': False, 'message': u'操作失败', 'error': '%s' % e})


@perm_required('account.up_bkuser')
def able_user(request):
    """
    启用账号
    """
    try:
        data = JSONParser().parse(request)
        id_list = data['id_list']
        user_model = get_user_model()
        # 用户是否存在
        for user_info in id_list:
            if user_model.objects.filter(id=user_info).exists():
                if request.user.id in id_list:
                    # log
                    operated_object = u'用户'
                    operated_type = u'启用'
                    content = u'启用用户失败，不能启用自身账号'
                    log_to_db(request, operated_object, operated_type, content)
                    return render_json({'result': False, 'message': u'启用用户失败，不能启用自身账号'})
                else:
                    BkUser.objects.filter(id=user_info).update(is_able=1)
                    # 权限变更

                    # log
                    operated_object = u'用户'
                    operated_type = u'启用'
                    username = BkUser.objects.get(id=user_info)
                    content = u'启用{}用户成功'.format(username)
                    log_to_db(request, operated_object, operated_type, content)
                    return render_json({'result': True, 'message': u'启用用户成功'})
            else:
                # log
                operated_object = u'用户'
                operated_type = u'启用'
                content = u'启用用户失败，该用户不存在'
                log_to_db(request, operated_object, operated_type, content)
                return render_json({'result': False, 'message': u'启用用户失败，该用户不存在'})
    except Exception as e:
        logger.exception('%s' % e)
        return render_json({'result': False, 'message': u'操作失败', 'error': '%s' % e})


@perm_required('account.delete_bkuser')
def delete_user(request):
    """
    删除账号
    """
    try:
        data = JSONParser().parse(request)
        id_list = data['id_list']
        user_model = get_user_model()
        # 用户是否存在
        for user_info in id_list:
            if user_model.objects.filter(id=user_info).exists():
                # 用户不能删除自己
                if request.user.id in id_list:
                    # log
                    operated_object = u'用户'
                    operated_type = u'删除'
                    content = u'删除用户失败，不能删除自身账号'
                    log_to_db(request, operated_object, operated_type, content)
                    return render_json({'result': False, 'message': u'删除用户失败，不能删除自身账号'})
                else:
                    BkUser.objects.filter(id=user_info).update(is_able=0, is_in_app=0)
                    # log
                    operated_object = u'用户'
                    operated_type = u'删除'
                    username = BkUser.objects.get(id=user_info).username
                    content = u'删除{}用户成功'.format(username)
                    log_to_db(request, operated_object, operated_type, content)
                    return render_json({'result': True, 'message': u'删除用户成功'})
            else:
                # log
                operated_object = u'用户'
                operated_type = u'删除'
                content = u'删除用户失败，该用户不存在'
                log_to_db(request, operated_object, operated_type, content)
                return render_json({'result': False, 'message': u'删除用户失败，该用户不存在'})
    except Exception as e:
        logger.exception('%s' % e)
        return render_json({'result': False, 'message': u'操作失败', 'error': '%s' % e})


def get_group_list(request):
    """
    获取角色列表
    """
    try:
        params_dict = request.GET
        or_mappings = [
            {'url': 'keyword', 'db': ['name__icontains', 'groupprofile__display_name__icontains']}
        ]
        q = get_filter(params_dict, or_mappings=or_mappings)
        groups = Group.objects.filter(q)
        # 每页多少条数据
        per_page = params_dict.get('pageCount', 10)
        paginator = Paginator(groups, per_page)
        try:
            group_page = paginator.page(params_dict.get('currentPage', 1))
        except PageNotAnInteger:
            group_page = paginator.page(1)
        except EmptyPage:
            # 指定页码超出范围
            group_page = paginator.page(paginator.num_pages)
        group_serializer = GroupSerializer(group_page, many=True)
        return render_json(
            {'result': True, 'code': 0, 'message': u'获取角色列表成功',
             'data': {'group': group_serializer.data, 'count': paginator.count}}
        )
    except Exception as e:
        logger.exception('%s' % e)
        return render_json({'result': False, 'message': u'获取角色列表失败', 'error': '%s' % e})


def get_all_group_list(request):
    """
    组列表，添加用户的时候用到
    :param request:
    :return:
    """
    if request.method == 'GET':
        group_profile_list = GroupProfile.objects.all()
        serializer = GroupProfileSerializer(group_profile_list, many=True)
        return render_json(
            {'result': True, 'message': u'获取角色列表成功', 'data': {'groups': serializer.data}}
        )


def get_all_user_list(request):
    """
    组列表，添加用户的时候用到
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_list = BkUser.objects.filter(is_in_app=1, is_able=1)
        serializer = UserInfoSerializer(user_list, many=True)
        return render_json(
            {'result': True, 'message': u'获取用户列表成功', 'data': serializer.data}
        )


@perm_required('auth.add_group')
def add_group(request):
    """新增角色"""
    if request.method == "POST":
        group_name = json.loads(request.body).get('display_name', '')  # 组名
        display_name = json.loads(request.body).get('display_name', '')  # 展示名称
        description = json.loads(request.body).get('description', '')  # 展示名称
        user_list = json.loads(request.body).get('user_list', '')
        try:
            group_info = Group.objects.create(name=group_name)
            GroupProfile.objects.create(group=group_info, display_name=display_name, description=description)
            users = [BkUser.objects.get(id=i) for i in user_list]
            group_info.user_set.add(*users)
            # log
            operated_object = u'角色'
            operated_type = u'添加'
            role_name = GroupProfile.objects.get(display_name=display_name).display_name
            content = u'添加{}角色成功'.format(role_name)
            log_to_db(request, operated_object, operated_type, content)
            result = {"result": True, "data": '', "message": "添加角色成功"}
            return JsonResponse(result)
        except Exception, e:
            # log
            operated_object = u'角色'
            operated_type = u'添加'
            content = u'添加角色失败'
            log_to_db(request, operated_object, operated_type, content)
            result = {'result': False, "data": "", "message": "添加角色失败"}
            logger.exception(e)
            return JsonResponse(result)
    else:
        result = {'result': False, "data": "", "message": "请求错误"}
        logger.exception('request error')
        return JsonResponse(result)


@perm_required('auth.change_group')
def edit_group_info(request):
    """
    编辑角色相关信息
    :param request:
    :return:
    """
    if request.method == "POST":
        group_id = json.loads(request.body).get('group_id', '')
        display_name = json.loads(request.body).get('display_name', '')
        description = json.loads(request.body).get('description', '')
        user_list = json.loads(request.body).get('user_list', '')
        try:
            GroupProfile.objects.filter(group_id=group_id).update(display_name=display_name,
                                                                  description=description)
            group = Group.objects.get(id=group_id)
            group.user_set.clear()
            users = [BkUser.objects.get(id=i) for i in user_list]
            group.user_set.add(*users)
            # log
            operated_object = u'角色'
            operated_type = u'修改'
            content = u'修改角色成功'
            log_to_db(request, operated_object, operated_type, content)

            result = {"result": True, "data": '', "message": "修改角色成功"}
            return JsonResponse(result)
        except Exception, e:
            # log
            operated_object = u'角色'
            operated_type = u'修改'
            content = u'修改角色失败'
            log_to_db(request, operated_object, operated_type, content)

            result = {'result': False, "data": "", "message": "修改角色失败"}
            logger.exception(e)
            return JsonResponse(result)
    else:
        result = {'result': False, "data": "", "message": "请求错误"}
        logger.exception('request error')
        return JsonResponse(result)


@perm_required('auth.down_group')
def disable_group(request):
    """
    禁用组
    """
    try:
        group_id = json.loads(request.body).get('group_id', '')
        GroupProfile.objects.filter(group_id=group_id).update(is_able=0)
        # log
        operated_object = u'组'
        operated_type = u'禁用'
        content = u'禁用组成功'
        log_to_db(request, operated_object, operated_type, content)

        return render_json({"result": True, "message": u"禁用组成功", "data": ""})
    except Exception as e:
        logger.exception('%s' % e)
        # log
        operated_object = u'组'
        operated_type = u'禁用'
        content = u'禁用组失败'
        log_to_db(request, operated_object, operated_type, content)
        return render_json({"result": False, "message": u"禁用组失败", "data": ""})


@perm_required('auth.up_group')
def able_group(request):
    """
    启用组
    """
    try:
        group_id = json.loads(request.body).get('group_id', '')
        GroupProfile.objects.filter(group_id=group_id).update(is_able=1)
        # log
        operated_object = u'组'
        operated_type = u'启用'
        content = u'启用组成功'
        log_to_db(request, operated_object, operated_type, content)

        return render_json({'result': True, 'message': u'启用组成功', 'data': ''})
    except Exception as e:
        logger.exception('%s' % e)
        # log
        operated_object = u'组'
        operated_type = u'启用'
        content = u'启用组失败'
        log_to_db(request, operated_object, operated_type, content)

        return render_json({'result': False, 'message': u'启用组失败', 'error': '%s' % e})


@perm_required('auth.delete_group')
def delete_group(request):
    """
    删除组
    """
    try:
        group_id = json.loads(request.body).get('group_id', '')
        colors_obj = Group.objects.get(id=group_id)
        colors_obj.user_set.all().delete()
        Group.objects.filter(id=group_id).delete()
        # log
        operated_object = u'组'
        operated_type = u'删除'
        content = u'删除组成功'
        log_to_db(request, operated_object, operated_type, content)

        return render_json({'result': True, 'message': u'删除组成功', 'data': ''})
    except Exception as e:
        logger.exception('%s' % e)
        # log
        operated_object = u'组'
        operated_type = u'删除'
        content = u'删除组失败'
        log_to_db(request, operated_object, operated_type, content)

        return render_json({'result': False, 'message': u'删除组失败', 'error': '%s' % e})


def get_all_perms(request):
    """
    获取所有权限
    """
    try:
        ret = {}
        ret.update(menus=get_all_menus(), permission=get_all_permissions())
        return render_json({'result': True, 'message': u'获取所有权限成功', 'data': ret})
    except Exception as e:
        logger.exception('%s' % e)
        return render_json({'result': False, 'message': u'获取所有权限失败', 'error': '%s' % e})


def get_group_detail(request):
    """
    获取组详情
    """
    try:
        params_dict = request.GET
        group_id = params_dict['group_id']
        group = Group.objects.get(id=group_id)
        group_serializer_data = GroupSerializer(instance=group).data
        return render_json({'result': True, 'message': u'获取组详情成功', 'data': group_serializer_data})
    except Exception as e:
        logger.exception('%s' % e)
        return render_json({'result': False, 'message': u'获取组详情失败', 'error': '%s' % e})


def get_user_permission(request):
    """获取用户的菜单权限和功能权限"""
    try:
        user = request.user
        groups = user.groups.all()
        group_serializer_data = GroupSerializer(instance=groups, many=True).data
        menus = []
        menus_id_list = []
        user_menus = []
        user_permissions = []
        # 该用户为超级管理员
        if user.is_superuser:
            user_menus = MenuSerializer(instance=Menu.objects.all(), many=True).data
        else:
            for i in group_serializer_data:
                menus += i['menus']
            for menu in menus:
                if menu['id'] not in menus_id_list:
                    menus_id_list.append(menu['id'])
                    user_menus.append(menu)
        app_label_codenames = user.get_all_permissions()
        for app_label_codename in app_label_codenames:
            app_label = app_label_codename.split('.')[0]
            codename = app_label_codename.split('.')[1]
            permission = Permission.objects.filter(codename=codename, content_type__app_label=app_label,
                                                   permissionprofile__is_show=True).first()
            if permission:
                user_permissions.append({'id': permission.id, 'codename': codename, 'name': permission.name,
                                         'permissionprofile__display_name': permission.permissionprofile.display_name})
        return render_json({'result': True, 'message': u'获取用户的菜单权限和功能权限成功',
                            'data': {'menus': user_menus, 'permissions': user_permissions}})
    except Exception as e:
        logger.exception('%s' % e)
        return render_json({'result': False, 'message': u'获取用户的菜单权限和功能权限失败', 'error': '%s' % e})


@perm_required('auth.change_permission')
def edit_group_permission(request):
    """
    编辑角色相关权限信息
    """
    try:
        data = JSONParser().parse(request)
        group_id = data['group_id']
        group_data = data['data']
        group = Group.objects.get(id=group_id)
        # 菜单ID列表
        menus = group_data['menu']
        with transaction.atomic():
            GroupToMenu.objects.filter(group_id=group_id).delete()
            group_to_menu_list = [GroupToMenu(menu_id=menu_id, group_id=group_id) for menu_id in menus]
            GroupToMenu.objects.bulk_create(group_to_menu_list)
        # 权限ID列表
        permissions = group_data['permission']
        with transaction.atomic():
            group.permissions.clear()
            permission_objs = [Permission.objects.get(id=perm_id) for perm_id in permissions]
            group.permissions.add(*permission_objs)
        # 应用系统ID
        applications = group_data['system']
        with transaction.atomic():
            GroupToPerApplication.objects.filter(group_id=group_id).delete()
            group_to_application_list = [GroupToPerApplication(per_application_id=app_sys_id, group_id=group_id) for
                                         app_sys_id in applications]
            GroupToPerApplication.objects.bulk_create(group_to_application_list)
        # 设备组
        agents = group_data['agent']
        with transaction.atomic():
            GroupToPerAgent.objects.filter(group_id=group_id).delete()
            group_to_agent_list = [GroupToPerAgent(per_agent_id=agent_id, group_id=group_id) for
                                   agent_id in agents]
            GroupToPerAgent.objects.bulk_create(group_to_agent_list)
        # 监控对象ID
        monitor_object = group_data['monitor']
        with transaction.atomic():
            GroupToPerMonitorObject.objects.filter(group_id=group_id).delete()
            group_to_monitor_object_list = [GroupToPerMonitorObject(per_monitor_object_id=monitor_id, group_id=group_id)
                                            for monitor_id in monitor_object]
            GroupToPerMonitorObject.objects.bulk_create(group_to_monitor_object_list)
        # log
        operated_object = u'角色'
        operated_type = u'修改'
        content = u'编辑角色权限成功'
        log_to_db(request, operated_object, operated_type, content)

        return render_json({'result': True, 'message': u'编辑角色权限成功', 'data': ''})
    except Exception as e:
        logger.exception('%s' % e)
        # log
        operated_object = u'角色'
        operated_type = u'修改'
        content = u'编辑角色权限失败'
        log_to_db(request, operated_object, operated_type, content)
        return render_json({'result': False, 'message': u'编辑角色权限失败', 'data': ''})
