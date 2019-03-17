# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Log, Menu, GroupProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = (
            'id', 'operator_date', 'operator', 'operated_object', 'operated_type', 'content', 'ip_addr', 'is_success')


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ('id', 'name', 'parent', 'display_name', 'is_menu', 'path', 'icon')


class PermissionSerializer(serializers.ModelSerializer):
    is_enable = serializers.SerializerMethodField(read_only=True)
    display_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Permission
        fields = ('id', 'codename', 'display_name', 'is_enable')

    def get_is_enable(self, obj):
        if hasattr(Permission, 'is_enable'):
            return obj.permissionprofile.is_enable
        else:
            return False

    def get_display_name(self, obj):
        if hasattr(Permission, 'display_name'):
            return obj.permissionprofile.display_name
        else:
            return ''


class BasicGroupSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField(read_only=True)
    is_enable = serializers.SerializerMethodField(read_only=True)
    is_built_in = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'display_name', 'is_enable', 'description', 'is_built_in')

    def get_display_name(self, obj):
        """
        获取当前角色的显示名
        """
        if hasattr(Group, 'groupprofile'):
            return obj.groupprofile.display_name
        else:
            return ''

    def get_is_enable(self, obj):
        """
        获取当前角色是否启用
        """
        if hasattr(Group, 'groupprofile'):
            return obj.groupprofile.is_enable
        else:
            return False

    def get_description(self, obj):
        """
        获取当前角色描述信息
        """
        if hasattr(Group, 'groupprofile'):
            return obj.groupprofile.description
        else:
            return ''

    def get_is_built_in(self, obj):
        """
        获取当前角色是否内置角色
        """
        if hasattr(Group, 'groupprofile'):
            return obj.groupprofile.is_built_in
        else:
            return False

class UserSerializer(serializers.ModelSerializer):
    groups = BasicGroupSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'chname', 'email', 'phone', 'groups')

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

    def create(self, validated_data, **kwargs):
        """反序列化新增对象"""
        instance = Group.objects.create(**validated_data)
        instance.display_name = self.initial_data.get('display_name', '')
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # 获取修改前显示名
        instance.name = validated_data.get('name', instance.name)
        instance.display_name = self.initial_data.get('display_name', self.get_display_name(instance))
        instance.save()
        return instance


class GroupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProfile
        fields = ('group', 'display_name')
