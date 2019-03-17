# -*- coding: utf-8 -*-

from component.utils.basic import (tuple_choices, choices_to_namedtuple)

CODE_STATUS_TUPLE = (
    'OK', 'UNAUTHORIZED', 'VALIDATE_ERROR', 'METHOD_NOT_ALLOWED',
    'PERMISSION_DENIED', 'SERVER_500_ERROR', 'OBJECT_NOT_EXIST')
CODE_STATUS_CHOICES = tuple_choices(CODE_STATUS_TUPLE)
ResponseCodeStatus = choices_to_namedtuple(CODE_STATUS_CHOICES)