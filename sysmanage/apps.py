# -*- coding: utf-8 -*-

"""
初始化内置APP数据
"""

from django.apps import AppConfig
from sysmanage.signals.dispatch import (dispatch_init_data)


class SysmanageConfig(AppConfig):
    name = 'sysmanage'
    verbose_name = 'Sysmanage'

    def ready(self):
        dispatch_init_data(self)

