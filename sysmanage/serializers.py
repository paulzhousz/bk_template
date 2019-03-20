# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Log, Menu, GroupProfile, GroupToMenu, PermissionGroup, PermissionProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from component.drf.serializer import CustomSerializer, ModelSerializer


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = (
            'id', 'operator_date', 'operator', 'operated_object', 'operated_type', 'content', 'ip_addr', 'is_success')


class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'parent', 'display_name', 'is_menu', 'path', 'icon', 'image_url', 'image_h_url')


class PermissionGroupSerializer(ModelSerializer):
    class Meta:
        model = PermissionGroup
        fields = ('id', 'display_name', 'is_enable')


class PermissionSerializer(ModelSerializer):
    is_enable = serializers.SerializerMethodField(read_only=True)
    display_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Permission
        fields = ('id', 'codename', 'display_name', 'is_enable')

    def get_is_enable(self, obj):
        if hasattr(obj, 'permissionprofile'):
            return obj.permissionprofile.is_enable
        else:
            return False

    def get_display_name(self, obj):
        if hasattr(obj, 'permissionprofile'):
            return obj.permissionprofile.display_name
        else:
            return ''


class BasicGroupSerializer(ModelSerializer):
    display_name = serializers.SerializerMethodField()
    is_enable = serializers.SerializerMethodField()
    is_built_in = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'display_name', 'is_enable', 'description', 'is_built_in')
        extra_fields = ('display_name', 'is_enable', 'description', 'is_built_in')

    def get_display_name(self, obj):
        """
        获取当前角色的显示名
        """
        if hasattr(obj, 'groupprofile'):
            return obj.groupprofile.display_name
        else:
            return ''

    def get_is_enable(self, obj):
        """
        获取当前角色是否启用
        """
        if hasattr(obj, 'groupprofile'):
            return obj.groupprofile.is_enable
        else:
            return False

    def get_description(self, obj):
        """
        获取当前角色描述信息
        """
        if hasattr(obj, 'groupprofile'):
            return obj.groupprofile.description
        else:
            return ''

    def get_is_built_in(self, obj):
        """
        获取当前角色是否内置角色
        """
        if hasattr(obj, 'groupprofile'):
            return obj.groupprofile.is_built_in
        else:
            return False

    def to_internal_value(self, data):
        """传入参数格式化校验数据"""
        data, no_validated_fields = CustomSerializer.to_internal_value(self, data)
        validated_data = super(BasicGroupSerializer, self).to_internal_value(data)
        # 添加多对多关系
        validated_data.update(**no_validated_fields)
        return validated_data

    def create(self, validated_data):
        """重写创建数据方法"""
        group = Group.objects.create(name=validated_data['name'])
        validated_data.pop('name')
        for (k, v) in validated_data.items():
            setattr(group, k, v)
        group.save()
        return group


class UserSerializer(ModelSerializer):
    groups = BasicGroupSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'chname', 'email', 'phone', 'is_in_app', 'is_enable', 'groups')

    def update(self, instance, validated_data):
        """反序列化更新对象"""
        instance.username = validated_data.get('username', instance.username)
        instance.chname = validated_data.get('chname', instance.chname)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class GroupSerializer(BasicGroupSerializer):
    menus = serializers.SerializerMethodField(read_only=True)
    permissions = PermissionSerializer(many=True, read_only=True)
    users = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = (
            'id', 'name', 'display_name', 'is_enable', 'is_built_in', 'description', 'menus', 'permissions', 'users'
        )
        extra_fields = ('display_name', 'is_enable', 'description', 'is_built_in', 'menus', 'users')

    def get_menus(self, obj):
        """
        获取当前角色关联的菜单列表
        """
        menus = obj.menu_set.all()
        return MenuSerializer(instance=menus, many=True).data

    def get_users(self, obj):
        """
        获取当前角色关联的用户
        """
        users = obj.user_set.all()
        return UserSerializer(instance=users, many=True).data

    def to_internal_value(self, data):
        """传入参数格式化校验数据"""
        data, no_validated_fields = CustomSerializer.to_internal_value(self, data)
        validated_data = super(BasicGroupSerializer, self).to_internal_value(data)
        # 添加多对多关系
        validated_data.update(**no_validated_fields)
        return validated_data

    def create(self, validated_data):
        """重写创建数据方法"""
        group = Group.objects.create(name=validated_data['name'])
        validated_data.pop('name')
        # 用户ID列表
        user_ids = validated_data.pop('users', [])
        for (k, v) in validated_data.items():
            setattr(group, k, v)
        group.save()
        users = CustomSerializer.get_instances(get_user_model(), user_ids)
        group.user_set.add(*users)
        return group

    def update(self, instance, validated_data):
        """重写更新数据方法"""
        # users和menus数据单独处理
        if 'users' in validated_data:
            user_ids = validated_data.pop('users')
            users = CustomSerializer.get_instances(get_user_model(), user_ids)
            instance.user_set.clear()
            instance.user_set.add(*users)
        if 'menus' in validated_data:
            menu_ids = validated_data.pop('menus')
            bulk_list = [GroupToMenu(group=instance, menu_id=menu_id) for menu_id in menu_ids]
            # 先清空多对多关系
            GroupToMenu.objects.filter(group=instance).delete()
            GroupToMenu.objects.bulk_create(bulk_list)
        return super(GroupSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        """序列化数据格式"""
        ret = super(GroupSerializer, self).to_representation(instance)
        # 去除用户关联的角色数据
        for user in ret['users']:
            user.pop('groups', None)
        return ret


class GroupProfileSerializer(ModelSerializer):
    class Meta:
        model = GroupProfile
        fields = ('group', 'display_name')
