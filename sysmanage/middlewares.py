# -*- coding: utf-8 -*-

from common.log import LogSignal


class LogMiddleware(object):
    """操作日志中间件"""

    def process_response(self, request, response):
        if request.META.get('LOG_NEED', False):
            log_info = request.META['LOG_INFO']
            data = response.data
            if data['result']:
                result = u'成功'
                is_success = True
            else:
                result = u'失败'
                is_success = False
            object_name = u''
            if log_info['attr'] and isinstance(data['data'], dict):
                object_name = u'【%s】' % data['data'].get(log_info['attr'], u'')
            content = u'%s%s%s' % (log_info['content'], object_name, result)
            si = LogSignal()
            si.log(log_info['operator'], log_info['operated_object'], log_info['operated_type'], content, is_success,
                   log_info['level'])
        return response
