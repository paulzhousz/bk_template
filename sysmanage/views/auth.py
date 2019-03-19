# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from component.drf.viewsets import ModelViewSet
from sysmanage.serializers import (UserSerializer, BasicGroupSerializer, GroupSerializer, MenuSerializer)
from sysmanage.models import Menu, Permission
from sysmanage.filters import GroupFilter


class UserViewSet(ModelViewSet):
    """用户相关操作"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

    @list_route(methods=['get'])
    def current_permission(self, request, *args, **kwargs):
        """获取当前用户权限"""
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
                                                   permissionprofile__is_enable=True).first()
            if permission:
                user_permissions.append({'id': permission.id, 'codename': codename, 'name': permission.name,
                                         'permissionprofile__display_name': permission.permissionprofile.display_name})
        return Response({'menus': user_menus, 'permissions': user_permissions})


class GroupViewSet(ModelViewSet):
    """角色基础操作"""
    queryset = Group.objects.filter(groupprofile__isnull=False)
    serializer_class = GroupSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_class = GroupFilter

    @detail_route(methods=['post'])
    def update_perm(self, request, *args, **kwargs):
        """更新角色权限"""
        pass