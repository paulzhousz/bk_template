# -*- coding: utf-8 -*-

"""
信号注册
"""
import django.dispatch

signal_log = django.dispatch.Signal(
    providing_args=['operator', 'operated_object', 'operated_type', 'content', 'is_success']
)
