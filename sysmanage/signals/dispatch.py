# -*- coding: utf-8 -*-

"""
信号触发
"""
import register
from django.db.models.signals import post_migrate, post_save
from sysmanage.signals.handlers import (init_data_handler, save_group_handler, save_permission_handler, log_handler)


def dispatch_init_data(sender):
    post_migrate.connect(init_data_handler, sender=sender)


def dispatch_save_group(sender):
    post_save.connect(save_group_handler, sender=sender)


def dispatch_save_perm(sender):
    post_save.connect(save_permission_handler, sender=sender)


def dispath_log():
    register.signal_log.connect(log_handler, dispatch_uid='sysmanage.handler.log_handler')
