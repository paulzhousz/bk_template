# -*- coding: utf-8 -*-

from django.db.models import F
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission, ContentType
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from guardian.decorators import permission_required_or_403
from blueking.component.shortcuts import get_client_by_user
from component.drf.viewsets import ModelViewSet
from component.drf.serializer import CustomSerializer
from component.drf.generics import validate_fields
from sysmanage.serializers import (BasicUserSerializer, UserSerializer, PermissionSerializer, GroupSerializer,
                                   MenuSerializer, PermissionGroupSerializer)
from sysmanage.models import Menu, PermissionGroup, GroupProfile
from sysmanage.filters import GroupFilter, UserFilter
from sysmanage.utils import (get_mapping, get_perms_with_groups, set_perms_obj)
from sysmanage.decorators import surperuser_required


class UserViewSet(ModelViewSet):
    """用户相关操作"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_class = UserFilter

    def retrieve(self, request, *args, **kwargs):
        """获取指定用户的详情"""
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        获取所有APP用户

            /api/sysmanage/users/?username=kris&is_in_app=true&is_enable=true&email=kris@canway.net&chname=kris
            -username 用户名 String【选填】
            -chname 中文名 String【选填】
            -is_in_app 是否该APP用户 Bollean【选填】
            -is_enable 是否启用 Bollean【选填】
            -email 邮箱 String【选填】
        """
        queryset = self.filter_queryset(self.get_queryset().filter(is_in_app=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(
        permission_required_or_403('account.delete_bkuser', (get_user_model(), 'pk', 'pk'), accept_global_perms=True)
    )
    def destroy(self, request, *args, **kwargs):
        """删除指定APP用户"""
        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """重写删除用户方法"""
        instance.is_in_app = False
        instance.is_enable = True
        instance.groups.clear()
        instance.save()

    @method_decorator(permission_required_or_403('account.add_bkuser'))
    def create(self, request, *args, **kwargs):
        """
        添加APP用户

            {
                "id": 1, "groups": [1, 2]
            }
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

    @method_decorator(
        permission_required_or_403('account.change_bkuser', (get_user_model(), 'pk', 'pk'), accept_global_perms=True)
    )
    def update(self, request, *args, **kwargs):
        """
        编辑APP用户

            {"groups": [1, 2]}
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
        """获取所有APP用户的下拉框数据"""
        ret = self.queryset.filter(is_enable=True, is_in_app=True).annotate(label=F('chname'),
                                                                            value=F('id')).values('label', 'value')
        return Response(list(ret))

    @list_route(methods=['get'], url_path='all')
    def get_all_users(self, request, *args, **kwargs):
        """
        获取所有APP用户

            /api/sysmanage/users/all/?username=kris&is_in_app=true&is_enable=true&email=kris@canway.net&chname=kris
            -username 用户名 String【选填】
            -chname 中文名 String【选填】
            -is_in_app 是否该APP用户 Bollean【选填】
            -is_enable 是否启用 Bollean【选填】
            -email 邮箱 String【选填】
        """
        queryset = self.filter_queryset(self.get_queryset().filter(is_in_app=True))
        serializer_class = BasicUserSerializer
        kwargs['context'] = self.get_serializer_context()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='add/select')
    def get_add_select(self, request, *args, **kwargs):
        """获取新增用户的下拉框数据"""
        ret = self.queryset.filter(is_enable=True, is_in_app=False).annotate(label=F('chname'),
                                                                             value=F('id')).values('label', 'value')
        return Response(list(ret))

    @method_decorator(permission_required_or_403('account.change_bkuser'))
    @list_route(methods=['put'], url_path='status')
    def change_status(self, request, *args, **kwargs):
        """
        批量启用或者禁用用户

            {"users": [1], "enable": true}
            - users: 由id组成的用户列表【必填】
            - enable: true表示开启，false表示禁用【必填】
        """
        validate_fields(request.data, 'users', 'enable')
        user_ids = request.data['users']
        enable = request.data['enable']
        self.queryset.filter(id__in=user_ids).update(is_enable=enable)
        return Response()

    @method_decorator(permission_required_or_403('account.sync_bkuser'))
    @list_route(methods=['post'], url_path='sync')
    def sync_user(self, request, *args, **kwargs):
        """
        同步蓝鲸用户

            {}
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

    @detail_route(methods=['get'], url_path='search/perm')
    def get_perms(self, request, *args, **kwargs):
        """获取对象关联权限"""
        instance = self.get_object()
        perms = get_perms_with_groups(instance)
        return Response(perms)

    @method_decorator(surperuser_required)
    @detail_route(methods=['post'], url_path='set/perm')
    def set_perms(self, request, *args, **kwargs):
        """
        设置对象关联权限

            [
                {"name": "account.add_bkuser", "groups": [1, 2]},
                {"name": "account.change_bkuser", "groups": [1, 3]},
                {"name": "account.delete_bkuser", "groups": []}
            ]
        """
        instance = self.get_object()
        codename_list = [i['name'] for i in request.data]
        set_perms_obj(instance, codename_list, request.data)
        return Response()


class GroupViewSet(ModelViewSet):
    """角色相关操作"""
    queryset = Group.objects.filter(groupprofile__isnull=False)
    serializer_class = GroupSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_class = GroupFilter

    def list(self, request, *args, **kwargs):
        """
        获取所有角色

            /api/sysmanage/groups/?page=1&page_size=10&is_built_in=true&is_enable=true&display_name=管理&omit=menus,permissions
            - page: 当前页面【可选】
            - page_size: 每页条数【可选】
            - is_built_in: 是否为内置角色【可选】
            - is_enable: 是否启用【可选】
            - display_name: 显示名称, 支持模糊匹配【可选】
            - omit: 屏蔽字段名, 多个用英文逗号隔开【可选】
            - fields: 显示字段名, 多个英文用逗号【可选】
        """
        return super(GroupViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """获取单个角色详情"""
        return super(GroupViewSet, self).retrieve(request, *args, **kwargs)

    @method_decorator(permission_required_or_403('account.add_group'))
    def create(self, request, *args, **kwargs):
        """
        添加角色

            {
                "name": "测试角色一",
                "description": "测试角色一的描述信息",
                "users": [1]
            }
                - name: 角色名称【必选】
                - description: 角色描述信息【可选】
                - users: 由id组成的用户列表【可选】
        """
        return super(GroupViewSet, self).create(request, *args, **kwargs)

    @method_decorator(
        permission_required_or_403('auth.change_group', (Group, 'pk', 'pk'), accept_global_perms=True)
    )
    def update(self, request, *args, **kwargs):
        """
        更新指定角色

            {
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

    @method_decorator(
        permission_required_or_403('auth.delete_group', (Group, 'pk', 'pk'), accept_global_perms=True)
    )
    def destroy(self, request, *args, **kwargs):
        """删除指定角色"""
        return super(GroupViewSet, self).destroy(request, *args, **kwargs)

    @list_route(methods=['get'], url_path='select')
    def get_select(self, request, *args, **kwargs):
        """获取所有角色的下拉框数据"""
        ret = Group.objects.filter(groupprofile__is_enable=True).annotate(label=F('groupprofile__display_name'),
                                                                          value=F('id')).values('label', 'value')
        return Response(list(ret))

    @method_decorator(permission_required_or_403('auth.delete_group'))
    @list_route(methods=['put'], url_path='status')
    def change_status(self, request, *args, **kwargs):
        """
        批量启用或者禁用角色

            {"groups": [1], "enable": true}
            - groups: 由id组成的角色列表【必选】
            - enable: true表示开启，false表示禁用【必选】
        """
        validate_fields(request.data, 'groups', 'enable')
        groups_ids = request.data['groups']
        enable = request.data['enable']
        GroupProfile.objects.filter(group_id__in=groups_ids).update(is_enable=enable)
        return Response()

    @detail_route(methods=['get'], url_path='perm_tree')
    def get_perm_tree(self, request, *args, **kwargs):
        """获取指定角色功能权限树状数据"""
        ret = []
        instance = self.get_object()
        perm_ids = instance.permissions.filter(permissionprofile__is_enable=True).values_list('id', flat=True)
        per_groups = PermissionGroup.objects.filter(is_enable=True)
        for per_group in per_groups:
            perms = Permission.objects.filter(permissionprofile__is_enable=True,
                                              permissionprofile__permission_group=per_group)
            per_group_data = PermissionGroupSerializer(instance=per_group).data
            perm_datas = PermissionSerializer(instance=perms, many=True).data
            for perm_data in perm_datas:
                if perm_data['id'] in perm_ids:
                    perm_data['has_perms'] = True
                else:
                    perm_data['has_perms'] = False
            per_group_data['children'] = perm_datas
            ret.append(per_group_data)
        return Response(ret)

    @detail_route(methods=['get'], url_path='search/perm')
    def get_perms(self, request, *args, **kwargs):
        """获取对象关联权限"""
        instance = self.get_object()
        perms = get_perms_with_groups(instance)
        return Response(perms)

    @method_decorator(surperuser_required)
    @detail_route(methods=['post'], url_path='set/perm')
    def set_perms(self, request, *args, **kwargs):
        """
        设置对象关联权限

            [
                {"name": "account.add_group", "groups": [1, 2]},
                {"name": "account.change_group", "groups": [1, 3]},
                {"name": "account.delete_group", "groups": []}
            ]
        """
        instance = self.get_object()
        codename_list = [i['name'] for i in request.data]
        set_perms_obj(instance, codename_list, request.data)
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
        """获取功能权限树状数据"""
        ret = []
        app_codename_list = request.user.get_all_permissions()
        filters = [{'codename': codename.split('.')[1], 'content_type__app_label': codename.split('.')[0]} for codename
                   in app_codename_list]
        # 获取当前用户的具有的功能权限列表
        perm_ids = []
        for filter in filters:
            if Permission.objects.filter(permissionprofile__is_enable=True, **filter).exists():
                permission = Permission.objects.get(permissionprofile__is_enable=True, **filter)
                perm_ids.append(permission.id)
        per_groups = PermissionGroup.objects.filter(is_enable=True)
        for per_group in per_groups:
            perms = self.get_queryset().filter(permissionprofile__is_enable=True,
                                               permissionprofile__permission_group=per_group)
            per_group_data = PermissionGroupSerializer(instance=per_group).data
            perm_datas = self.serializer_class(instance=perms, many=True).data
            for perm_data in perm_datas:
                if perm_data['id'] in perm_ids:
                    perm_data['has_perms'] = True
                else:
                    perm_data['has_perms'] = False
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
