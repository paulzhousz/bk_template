# -*- coding: utf-8 -*-
__author__ = 'Austin'
# @Time    : 2019/1/15 15:28
# @Email   : austin@canway.net
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()
from account.models import BkUser
from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupPerSerializer(serializers.ModelSerializer):
    system_permission = serializers.SerializerMethodField(read_only=True)
    agent_permission = serializers.SerializerMethodField(read_only=True)
    monitor_permission = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'system_permission', 'agent_permission', 'monitor_permission')

    def get_system_permission(self, obj):
        """
        获取当前组已拥有应用系统的权限
        :param obj:
        :return:
        """
        system_permission_data = obj.applicationsystem_set.all()
        return [i.app_sys_id for i in system_permission_data]

    def get_agent_permission(self, obj):
        """
        获取当前组已拥有设备组的权限
        :param obj:
        :return:
        """
        agent_permission_data = obj.agent_set.all()
        return [i.id for i in agent_permission_data]

    def get_monitor_permission(self, obj):
        """
        获取当前组已拥有监控对象的权限
        :param obj:
        :return:
        """
        monitor_permission_data = obj.monitorobject_set.all()
        return [i.id for i in monitor_permission_data]


def get_user_per_all(user_id):
    current_user_set = BkUser.objects.filter(id=user_id)
    current_group_set = Group.objects.filter(user=current_user_set)
    group_detail = [row.id for row in current_group_set]  # 获取当前用户有哪些组， 返回组ID
    # 获取组有哪些应用系统、设备组、监控对象
    permission_data = []
    user_permission = {}
    for i in group_detail:
        group_serializer_data = GroupPerSerializer(instance=Group.objects.get(id=i)).data
        permission_data.append(group_serializer_data)
    # 进行去重操作
    system_permission = list(set([j for i in permission_data for j in i['system_permission']]))   # 应用系统
    agent_permission = list(set([j for i in permission_data for j in i['agent_permission']]))  # 设备组
    monitor_permission = list(set([j for i in permission_data for j in i['monitor_permission']]))  # 监控对象
    user_permission['system_permission'] = system_permission
    user_permission['agent_permission'] = agent_permission
    user_permission['monitor_permission'] = monitor_permission
    return user_permission


if __name__ == '__main__':
    user_id = 1
    print get_user_per_all(user_id)
