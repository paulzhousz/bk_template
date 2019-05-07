# -*- coding: utf-8 -*-

"""
初始化内置APP数据
"""

from django.apps import AppConfig
from django.contrib.auth.models import Group, Permission
from sysmanage.signals.dispatch import (dispatch_init_data, dispatch_save_group, dispatch_save_perm, dispath_log)


class SysmanageConfig(AppConfig):
    name = 'sysmanage'
    verbose_name = 'Sysmanage'

    def ready(self):
        dispatch_save_group(Group)
        dispatch_save_perm(Permission)
        dispatch_init_data(self)
        dispath_log()
