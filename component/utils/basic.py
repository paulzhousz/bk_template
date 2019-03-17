# -*- coding: utf-8 -*-

import datetime
from collections import namedtuple


def now():
    """获取当前时间"""
    return datetime.datetime.now()


def tuple_choices(tupl):
    """从django-model的choices转换到namedtuple"""
    return [(t, t) for t in tupl]


def dict_to_namedtuple(dic):
    """从dict转换成namedtuple"""
    return namedtuple('AttrStore', dic.keys())(**dic)


def choices_to_namedtuple(choices):
    """从django-model的choices转换到namedtuple"""
    return dict_to_namedtuple(dict(choices))