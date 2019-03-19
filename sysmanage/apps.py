# -*- coding: utf-8 -*-

"""
初始化内置APP数据
"""

from django.apps import AppConfig
from django.contrib.auth.models import Group
from sysmanage.signals.dispatch import (dispatch_init_data, dispatch_create_group)


class SysmanageConfig(AppConfig):
    name = 'sysmanage'
    verbose_name = 'Sysmanage'

    def ready(self):
        dispatch_create_group(Group)
        dispatch_init_data(self)

