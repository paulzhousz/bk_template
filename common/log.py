# -*- coding: utf-8 -*-

"""
Usage:

    from common.log import logger

    logger.info("test")
    logger.error("wrong1")
    logger.exception("wrong2")

    # with traceback
    try:
        1 / 0
    except Exception:
        logger.exception("wrong3")

    from common.log import LogSignal

    log_si = LogSignal()
    log_si.log('kris', u'无', u'测试', u'测试内容')
"""

import logging
from sysmanage.signals.register import signal_log

logger = logging.getLogger("root")


class LogSignal(object):
    """操作日志处理信号"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """单例实例"""
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.sender = 'root'

    def _log(self, content, level):
        if callable(getattr(logger, level, None)):
            getattr(logger, level)(content)

    def log(self, operator, operated_object, operated_type, content, is_success=True, level='info'):
        """
        发送操作日志信号
        :param operator: 操作者
        :param operated_object: 操作对象
        :param operated_type: 操作类型
        :param content: 操作内容
        :param is_success: 操作是否成功
        :param level 日志级别
        """
        signal_log.send(self.sender, operator=operator, operated_object=operated_object, operated_type=operated_type,
                        content=content, is_success=is_success)
        self._log(content, level)
