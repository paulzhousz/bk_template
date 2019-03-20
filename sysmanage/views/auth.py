# -*- coding: utf-8 -*-

from django.db.models import F
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from blueking.component.shortcuts import get_client_by_user
from component.drf.viewsets import ModelViewSet
from component.drf.serializer import CustomSerializer
from component.drf.generics import validate_fields
from sysmanage.serializers import (UserSerializer, PermissionSerializer, GroupSerializer, MenuSerializer,
                                   PermissionGroupSerializer)
from sysmanage.models import Menu, Permission, PermissionGroup, PermissionProfile, GroupProfile
from sysmanage.filters import GroupFilter
from sysmanage.utils import get_mapping


class UserViewSet(ModelViewSet):
    """用户相关操作"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def retrieve(self, request, *args, **kwargs):
        """获取指定用户的详情"""
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """获取所有APP用户"""
        queryset = self.filter_queryset(self.get_queryset().filter(is_in_app=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除指定APP用户"""
        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """重写删除用户方法"""
        instance.is_in_app = False
        instance.is_enable = True
        instance.groups.clear()
        instance.save()

    def create(self, request, *args, **kwargs):
        """
        添加APP用户
        :param
        body: {"id": 1, "groups": [1, 2]}
            - id: user的id【必填】
            - groups: 由角色id组成的列表【可选】
        """
        # id必传
        validate_fields(request.data, 'id')
        id = request.data['id']
        group_ids = request.data.get('groups', [])
        user_model = get_user_model()
        user = user_model.objects.get(id=id)
        # 添加用户、角色关联关系
        groups = CustomSerializer.get_instances(Group, group_ids)
        user.groups.clear()
        user.groups.add(*groups)
        # 初始化用户属性
        user.is_in_app = True
        user.is_enable = True
        user.save()
        serializer = self.serializer_class(instance=user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        编辑APP用户
        :param
        body: {"groups": [1, 2]}
            - groups: 由id组成的角色列表【可选】
        """
        instance = self.get_object()
        # 判断是否传入groups
        if 'groups' in request.data:
            # 添加用户、角色关联关系
            group_ids = request.data['groups']
            groups = CustomSerializer.get_instances(Group, group_ids)
            instance.groups.clear()
            instance.groups.add(*groups)
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data)

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
                                         'display_name': permission.permissionprofile.display_name})
        return Response({'menus': user_menus, 'permissions': user_permissions})

    @list_route(methods=['get'], url_path='select')
    def get_select(self, request, *args, **kwargs):
        """获取所有用户的下拉框数据"""
        ret = self.queryset.filter(is_enable=True, is_in_app=True).annotate(label=F('chname'),
                                                                            value=F('id')).values('label', 'value')
        return Response(ret)

    @list_route(methods=['get'], url_path='add/select')
    def get_add_select(self, request, *args, **kwargs):
        """获取新增用户的下拉框数据"""
        ret = self.queryset.filter(is_enable=True, is_in_app=False).annotate(label=F('chname'),
                                                                             value=F('id')).values('label', 'value')
        return Response(ret)

    @list_route(methods=['put'], url_path='status')
    def change_status(self, request, *args, **kwargs):
        """
        批量启用或者禁用用户
        :param
        body: {"users": [1], "enable": true}
            - users: 由id组成的用户列表【必填】
            - enable: true表示开启，false表示禁用【必填】
        """
        validate_fields(request.data, 'users', 'enable')
        user_ids = request.data['users']
        enable = request.data['enable']
        self.queryset.filter(id__in=user_ids).update(is_enable=enable)
        return Response()

    @list_route(methods=['post'], url_path='sync')
    def sync_user(self, request, *args, **kwargs):
        """
        同步蓝鲸用户
        body: {}
        """
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
            return Response()
        else:
            raise ValueError(result['message'])


class GroupViewSet(ModelViewSet):
    """角色相关操作"""
    queryset = Group.objects.filter(groupprofile__isnull=False)
    serializer_class = GroupSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_class = GroupFilter

    def list(self, request, *args, **kwargs):
        """获取所有角色"""
        return super(GroupViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """获取单个角色详情"""
        return super(GroupViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        添加角色
        :param
        body: {
            "name": "测试角色一",
            "description": "测试角色一的描述信息",
            "users": [1]
        }
            - name: 角色名称【必填】
            - description: 角色描述信息【可选】
            - users: 由id组成的用户列表【可选】
        """
        return super(GroupViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        更新指定角色
        :param
        body {
            "name": "测试角色一",
            "description": "测试角色一的描述信息",
            "users": [1],
            "menus": [1, 2, 3],
            "permissions": [4, 5, 6]
        }
            - name: 角色名称【可选】
            - description: 角色描述信息【可选】
            - users: 由id组成的用户列表【可选】
            - menus: 由id组成的菜单列表【可选】
            - permissions: 由id组成的权限列表【可选】
        """
        return super(GroupViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """删除指定角色"""
        return super(GroupViewSet, self).destroy(request, *args, **kwargs)

    @list_route(methods=['get'], url_path='select')
    def get_select(self, request, *args, **kwargs):
        """获取所有角色的下拉框数据"""
        ret = Group.objects.filter(groupprofile__is_enable=True).annotate(label=F('groupprofile__display_name'),
                                                                          value=F('id')).values('label', 'value')
        return Response(ret)

    @list_route(methods=['put'], url_path='status')
    def change_status(self, request, *args, **kwargs):
        """
        批量启用或者禁用角色
        :param
        body: {"groups": [1], "enable": true}
            - groups: 由id组成的角色列表【必填】
            - enable: true表示开启，false表示禁用【必填】
        """
        validate_fields(request.data, 'groups', 'enable')
        groups_ids = request.data['groups']
        enable = request.data['enable']
        GroupProfile.objects.filter(group_id__in=groups_ids).update(is_enable=enable)
        return Response()


class PermViewSet(ModelViewSet):
    """权限相关操作"""
    queryset = Permission.objects.filter(permissionprofile__isnull=False)
    serializer_class = PermissionSerializer
    http_method_names = ['get']
    paginator = None

    def list(self, request, *args, **kwargs):
        """获取所有权限"""
        return super(PermViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """获取指定权限详情"""
        return super(PermViewSet, self).retrieve(request, *args, **kwargs)

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
    paginator = None

    def list(self, request, *args, **kwargs):
        """获取所有菜单"""
        return super(MenuViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """获取指定菜单详情"""
        return super(MenuViewSet, self).retrieve(request, *args, **kwargs)

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
