# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from component.drf.viewsets import ModelViewSet
from sysmanage.serializers import (UserSerializer, PermissionSerializer, GroupSerializer, MenuSerializer,
                                   PermissionGroupSerializer)
from sysmanage.models import Menu, Permission, PermissionGroup, PermissionProfile
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
    """角色相关操作"""
    queryset = Group.objects.filter(groupprofile__isnull=False)
    serializer_class = GroupSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_class = GroupFilter


class PermViewSet(ModelViewSet):
    """权限相关操作"""
    queryset = Permission.objects.filter(permissionprofile__isnull=False)
    serializer_class = PermissionSerializer
    http_method_names = ['get']

    @list_route(methods=['get'], url_path='tree')
    def get_perm_tree(self, request, *args, **kwargs):
        """获取权限树状数据"""
        ret = []
        per_groups = PermissionGroup.objects.filter(is_enable=True)
        for per_group in per_groups:
            perms = self.get_queryset().filter(permissionprofile__is_enable=True,
                                               permissionprofile__permission_group=per_group)
            per_group_data = PermissionGroupSerializer(instance=per_group).data
            perm_datas = self.serializer_class(instance=perms, many=True).data
            per_group_data['children'] = perm_datas
            ret.append(per_group_data)
        return Response(ret)


class MenuViewSet(ModelViewSet):
    """菜单以及路由的相关操作"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    http_method_names = ['get']

    def _recur_menu(self, menu_data):
        menu_id = menu_data['id']
        childs = Menu.objects.filter(parent=menu_id)
        child_datas = MenuSerializer(instance=childs, many=True).data
        menu_data['children'] = child_datas
        for menu_child_data in menu_data['children']:
            self._recur_menu(menu_child_data)
        return menu_data

    def _menu_tree(self, id):
        menu = Menu.objects.get(id=id)
        menu_data = MenuSerializer(instance=menu).data
        self._recur_menu(menu_data)
        return menu_data

    @detail_route(methods=['get'], url_path='tree')
    def get_memu_tree(self, request, *args, **kwargs):
        """获取指定菜单或者路由的树状数据"""
        id = kwargs['pk']
        return Response(self._menu_tree(id))

    @list_route(methods=['get'], url_path='tree')
    def get_menus_tree(self, request):
        """获取菜单以及路由的树状数据"""
        # 获取所有一级菜单
        menus = Menu.objects.filter(parent__isnull=True)
        ret = [self._menu_tree(id=menu.id) for menu in menus]
        return Response(ret)
