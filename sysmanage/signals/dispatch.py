# -*- coding: utf-8 -*-

"""
信号触发
"""

from django.db.models.signals import post_migrate, post_save
from sysmanage.signals.handlers import init_data_handler, save_group_handler


def dispatch_init_data(sender):
    post_migrate.connect(init_data_handler, sender=sender)


def dispatch_create_group(sender):
    post_save.connect(save_group_handler, sender=sender)
