# -*- coding: utf-8 -*-
"""
错误类
"""
from django.utils.translation import ugettext_lazy as _


class ServerError(Exception):
    """
    后台错误类
    """
    MESSAGE = _(u'系统异常')
    ERROR_CODE = 'FATAL_ERROR'

    def __init__(self, *args):
        self.code = self.ERROR_CODE
        self.message = u"%s: %s" % (self.MESSAGE, args[0]) if args else self.MESSAGE
        super(ServerError, self).__init__(*args)

    def __str__(self):
        return "<AppError %s:(%s)>" % (self.code, self.message)
